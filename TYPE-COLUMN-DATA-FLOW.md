# GhostLayer AI - Type Column Data Flow

## 📊 Where "Type" Column Gets Its Data

### **Complete Flow:**

```
Database Table
    ↓
API Endpoint
    ↓
Frontend Display
    ↓
User Sees "Type" Column
```

---

## 1️⃣ **Database Source**

### **Table**: `user_ghostlayer_documents`

**Location**: `app/idms.db`

**Column**: `document_type TEXT NOT NULL`

**Sample Data**:
```sql
id | user_id | document_name | document_type    | upload_timestamp
---|---------|---------------|------------------|------------------
12 | 1       | aadhaar1.png  | Aadhaar Card     | 2025-09-30 10:12:39
13 | 1       | vot1.png      | Voter ID Card    | 2025-09-30 11:54:34
14 | 1       | vot2.png      | Voter ID Card    | 2025-09-30 11:59:54
```

---

## 2️⃣ **API Endpoint**

### **Endpoint**: `GET /api/ghostlayer/documents`

**File**: `app/main.py` (line 1371)

**Code**:
```python
@app.get("/api/ghostlayer/documents")
async def get_ghostlayer_documents(
    request: Request,
    page: int = 1, 
    limit: int = 10, 
    search: str = "", 
    status: str = ""
):
    """Get user-specific GhostLayer documents with pagination"""
    user_data = require_auth(request)
    user_id = user_data['id']
    
    # Fetch documents from database
    documents = db.get_user_ghostlayer_documents(
        user_id=user_id, 
        limit=limit, 
        offset=offset
    )
    
    return {"documents": documents, ...}
```

**What it returns**:
```json
{
  "documents": [
    {
      "id": 13,
      "document_name": "vot1.png",
      "document_type": "Voter ID Card",  ← This field!
      "document_format": "PNG",
      "document_size": 245678,
      "processing_status": "completed",
      ...
    }
  ]
}
```

---

## 3️⃣ **Database Query**

### **Function**: `get_user_ghostlayer_documents()`

**File**: `app/database.py`

**Code**:
```python
def get_user_ghostlayer_documents(self, user_id: int = None, limit: int = 10, offset: int = 0):
    """Get user's GhostLayer documents (admin sees all)"""
    conn = sqlite3.connect(self.db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if user_id:
        # Regular user - only their documents
        cursor.execute("""
            SELECT 
                id, user_id, uploaded_by, 
                document_name, 
                document_type,          ← Selected here!
                document_format,
                document_size,
                upload_timestamp,
                processing_status
            FROM user_ghostlayer_documents 
            WHERE user_id = ?
            ORDER BY upload_timestamp DESC
            LIMIT ? OFFSET ?
        """, (user_id, limit, offset))
    else:
        # Admin - all documents
        cursor.execute("""
            SELECT * 
            FROM user_ghostlayer_documents 
            ORDER BY upload_timestamp DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
    
    rows = cursor.fetchall()
    documents = [dict(row) for row in rows]
    
    return documents
```

---

## 4️⃣ **Frontend Display**

### **Template**: `app/templates/ghostlayer.html`

**Table HTML**:
```html
<table class="min-w-full divide-y divide-gray-200">
    <thead>
        <tr>
            <th>Image Name</th>
            <th><i class="fas fa-tag"></i>Type</th>  ← Column Header
            <th>Format</th>
            <th>Size</th>
            <th>Status</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody id="documents-table-body">
        <!-- Rows populated by JavaScript -->
    </tbody>
</table>
```

**JavaScript (line 598)**:
```javascript
function renderDocumentsTable(documents) {
    documents.forEach(doc => {
        const row = `
            <tr>
                <td>${doc.document_name}</td>
                <td>${doc.document_type || 'Unknown'}</td>  ← Displayed here!
                <td>${doc.document_format}</td>
                <td>${formatSize(doc.document_size)}</td>
                <td>${getStatusBadge(doc.processing_status)}</td>
                <td>${getActionButtons(doc.id)}</td>
            </tr>
        `;
        // Append to table...
    });
}
```

---

## 5️⃣ **What User Sees**

### **GhostLayer AI Documents Table**:

```
┌────────────────┬──────────────────┬────────┬──────────┬───────────┬─────────┐
│ Image Name     │ Type             │ Format │ Size     │ Status    │ Actions │
├────────────────┼──────────────────┼────────┼──────────┼───────────┼─────────┤
│ aadhaar1.png   │ Aadhaar Card     │ PNG    │ 240 KB   │ Completed │ [View]  │
│ vot1.png       │ Voter ID Card    │ PNG    │ 356 KB   │ Completed │ [View]  │
│ vot2.png       │ Voter ID Card    │ PNG    │ 298 KB   │ Completed │ [View]  │
└────────────────┴──────────────────┴────────┴──────────┴───────────┴─────────┘
                          ↑
                    This column!
```

---

## 🔄 **How document_type Gets Updated**

### **Method 1: During Upload & Processing**

**When you upload and process a document:**

1. **Upload**: Creates record with `document_type = ""` (empty)
   ```python
   document_data = {
       'document_type': document_type,  # From form or ""
       ...
   }
   db.insert_user_ghostlayer_document(document_data)
   ```

2. **Process**: GhostLayer OCR extracts text
   ```python
   # Extract text with Google Document AI
   full_text = ocr_result['full_text']
   ```

3. **Classify**: Text is analyzed against keywords
   ```python
   # In main.py (line ~1760)
   classification_result = classify_document(full_text, config)
   document_type = classification_result['document_type']
   ```

4. **Update**: Database is updated
   ```python
   update_data = {
       'document_type': document_type,  # "Voter ID Card"
       'processing_status': 'completed'
   }
   db.update_user_ghostlayer_document(document_id, update_data)
   ```

### **Method 2: Reclassification (What We Just Did)**

**For existing documents with old classifications:**

```python
# Read JSON file with OCR text
with open(json_path, 'r', encoding='utf-8') as f:
    ocr_data = json.load(f)

full_text = ocr_data['full_text']

# Classify with updated keywords
result = classify_document(full_text, config)
new_type = result['document_type']

# Update database
cursor.execute("""
    UPDATE user_ghostlayer_documents
    SET document_type = ?
    WHERE id = ?
""", (new_type, document_id))
```

---

## 📋 **Summary**

### **The "Type" column displays the `document_type` field from:**

```
Database: app/idms.db
Table:    user_ghostlayer_documents  
Column:   document_type (TEXT NOT NULL)
                ↓
API:      GET /api/ghostlayer/documents
Returns:  { "document_type": "Voter ID Card" }
                ↓
Frontend: ghostlayer.html
Display:  ${doc.document_type || 'Unknown'}
                ↓
User Sees: "Voter ID Card" in Type column
```

### **Classification Logic:**

The `document_type` value is determined by:
1. **Text extraction** from image (Google Document AI OCR)
2. **Keyword matching** against `app/document_identification.json`
3. **Confidence calculation** (matched keywords / total keywords)
4. **Threshold check** (must meet minimum confidence)
5. **Best match selection** (highest confidence above threshold)

### **Example for Voter ID Card:**

```
Text: "ELECTION COMMISSION OF INDIA..."
      ↓
Keywords matched: 5 of 23
      ↓
Confidence: 22%
      ↓
Threshold: 10% ✓ PASS
      ↓
Result: document_type = "Voter ID Card"
      ↓
Stored in database
      ↓
Displayed in Type column
```

---

**The Type column is a direct reflection of what's stored in the `document_type` column of the `user_ghostlayer_documents` table!**
