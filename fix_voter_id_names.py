"""
Fix voter_id to show "Voter ID Card" instead of "voter_id"
"""
import sqlite3
import os

# Connect to database
db_path = os.path.join('app', 'idms.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update records that show "voter_id" to "Voter ID Card"
cursor.execute("""
    UPDATE user_ghostlayer_documents
    SET document_type = 'Voter ID Card'
    WHERE document_type = 'voter_id'
""")

affected = cursor.rowcount
conn.commit()
conn.close()

print(f"Updated {affected} document(s) from 'voter_id' to 'Voter ID Card'")
