"""
Reclassify existing GhostLayer documents with updated keywords
"""
import sqlite3
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def classify_document(document_text: str, config: dict) -> dict:
    """Classify document type based on keywords found in the text."""
    document_types = config.get('document_types', {})
    settings = config.get('classification_settings', {})
    
    case_sensitive = settings.get('case_sensitive', False)
    partial_match = settings.get('partial_match', True)
    fallback_type = settings.get('fallback_document_type', 'unknown')
    
    # Prepare text for matching
    search_text = document_text if case_sensitive else document_text.lower()
    
    classification_results = []
    
    for doc_type, doc_config in document_types.items():
        keywords = doc_config.get('keywords', [])
        confidence_threshold = doc_config.get('confidence_threshold', 0.3)
        
        matches = []
        for keyword in keywords:
            try:
                search_keyword = keyword if case_sensitive else keyword.lower()
                
                if partial_match:
                    if search_keyword in search_text:
                        matches.append(keyword)
            except Exception as e:
                # Skip keywords that cause encoding issues
                logging.error(f"Error processing keyword '{keyword}': {e}")
                continue
        
        if matches:
            confidence = len(matches) / len(keywords) if keywords else 0
            classification_results.append({
                'type': doc_type,
                'name': doc_config.get('name', doc_type),
                'confidence': confidence,
                'matched_keywords': matches,
                'total_keywords': len(keywords)
            })
        
        # Debug for voter_id
        if doc_type == 'voter_id':
            logging.info(f"voter_id: {len(matches)} matches out of {len(keywords)} keywords")
    
    # Sort by confidence
    classification_results.sort(key=lambda x: x['confidence'], reverse=True)
    
    # Return best match if confidence threshold is met
    if classification_results:
        best_match = classification_results[0]
        threshold = document_types[best_match['type']].get('confidence_threshold', 0.3)
        
        if best_match['confidence'] >= threshold:
            return {
                'document_type': best_match['name'],
                'confidence': best_match['confidence'],
                'matched_keywords': best_match['matched_keywords'],
                'all_results': classification_results
            }
    
    # Fallback
    return {
        'document_type': f"{fallback_type.title()} Document",
        'confidence': 0.0,
        'matched_keywords': [],
        'all_results': classification_results
    }

def reclassify_documents():
    """Reclassify all GhostLayer documents with updated keywords"""
    
    # Load classification config
    config_path = os.path.join('app', 'document_identification.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    logger.info("Loaded classification config")
    
    # Connect to database
    db_path = os.path.join('app', 'idms.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all GhostLayer documents
    cursor.execute("""
        SELECT id, document_name, document_type, coordinates_json_path
        FROM user_ghostlayer_documents
        WHERE processing_status = 'completed'
    """)
    
    documents = cursor.fetchall()
    logger.info(f"Found {len(documents)} documents to reclassify")
    
    updated_count = 0
    
    for doc in documents:
        doc_id = doc['id']
        doc_name = doc['document_name']
        old_type = doc['document_type']
        json_path = doc['coordinates_json_path']
        
        logger.info(f"\nProcessing: {doc_name} (ID: {doc_id})")
        logger.info(f"  Current type: {old_type}")
        
        # Read coordinates JSON to get full_text
        if not json_path:
            logger.warning(f"  No JSON path stored in database")
            continue
        
        # Convert path separators for Windows
        json_path = json_path.replace('/', os.sep).replace('\\', os.sep)
        
        # Try both with and without app/ prefix
        if not os.path.exists(json_path):
            # Try with app/ prefix
            alt_json_path = os.path.join('app', json_path)
            if os.path.exists(alt_json_path):
                json_path = alt_json_path
            else:
                logger.warning(f"  No JSON file found: {json_path}")
                logger.warning(f"  Also tried: {alt_json_path}")
                continue
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                ocr_data = json.load(f)
            
            full_text = ocr_data.get('full_text', '')
            
            if not full_text:
                logger.warning(f"  No text found in JSON")
                continue
            
            # Debug: show text preview
            logger.info(f"  Text length: {len(full_text)} characters")
            logger.info(f"  Text preview: {full_text[:100]}...")
            
            # Classify with updated keywords
            result = classify_document(full_text, config)
            
            new_type = result['document_type']
            confidence = result['confidence']
            matched_keywords = result['matched_keywords']
            
            logger.info(f"  New classification: {new_type} (confidence: {confidence:.2f})")
            logger.info(f"  Matched keywords: {matched_keywords}")
            
            # Update database if classification changed
            if new_type != old_type:
                cursor.execute("""
                    UPDATE user_ghostlayer_documents
                    SET document_type = ?
                    WHERE id = ?
                """, (new_type, doc_id))
                
                updated_count += 1
                logger.info(f"  ✅ Updated: {old_type} → {new_type}")
            else:
                logger.info(f"  ℹ️  No change needed")
                
        except Exception as e:
            logger.error(f"  ❌ Error processing document: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Reclassification complete!")
    logger.info(f"Total documents processed: {len(documents)}")
    logger.info(f"Documents updated: {updated_count}")
    logger.info(f"{'='*60}")

if __name__ == "__main__":
    reclassify_documents()
