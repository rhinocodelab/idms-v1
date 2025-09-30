# Analytics Dashboard - GhostLayer Integration Complete

## Problem Identified
The Analytics Dashboard was only showing data from AI Document Classification (and the old `documents` table), completely **ignoring GhostLayer AI documents**.

## Database Analysis (app/idms.db)

### **Current State:**
```
Tables with Data:
├─ user_ghostlayer_documents    : 1 row  (aadhaar by user1)
├─ ghostlayer_documents         : 2 rows (old table, deprecated)
├─ users                        : 2 rows (admin + user1)
└─ ai_document_classifications  : 0 rows (empty currently)

Old/Empty Tables:
└─ documents                    : 0 rows (old table, not used anymore)
```

### **Issue:**
Analytics was querying the **old `documents` table** which is **empty**, missing all data from:
- ❌ `ai_document_classifications` (new AI classification table)
- ❌ `user_ghostlayer_documents` (GhostLayer table)

---

## Solution Implemented

### **1. Updated Database Method** (`app/database.py`)

**Modified:** `get_analytics_data(user_id: int = None)`

**Now Queries:**
- ✅ `ai_document_classifications` (AI classification documents)
- ✅ `user_ghostlayer_documents` (GhostLayer documents)
- ✅ Combines data from BOTH sources
- ✅ Supports user-specific filtering

**Key Features:**
```python
def get_analytics_data(self, user_id: int = None):
    # Query AI documents
    SELECT ... FROM ai_document_classifications WHERE user_id = ?
    
    # Query GhostLayer documents  
    SELECT ... FROM user_ghostlayer_documents WHERE user_id = ?
    
    # Combine results
    - Document types (AI + GhostLayer aggregated)
    - Processing trends (AI + GhostLayer by date)
    - File types (AI + GhostLayer formats)
    - Total counts (AI + GhostLayer combined)
```

**Data Returned:**
```json
{
  "total_documents": 156,           // AI + GhostLayer total
  "ai_documents": 100,              // AI Classification count
  "ghostlayer_documents": 56,       // GhostLayer count
  "processed_today": 12,            // Combined today
  "error_rate": 1.5,                // Combined error %
  "success_rate": 98.5,             // Combined success %
  "document_types": [               // Combined & aggregated
    {"name": "Aadhaar", "count": 45},
    {"name": "Invoice", "count": 30}
  ],
  "criticality_levels": [...],      // AI only (GL doesn't have)
  "processing_trends": [...],       // Combined by date
  "file_types": [...]               // Combined formats
}
```

---

### **2. Updated API Endpoint** (`app/main.py`)

**Modified:** `GET /api/analytics`

**New Logic:**
```python
@app.get("/api/analytics")
async def get_analytics_data(request: Request):
    user_data = require_auth(request)
    
    if user_data.get('role') == 'admin':
        # Admin sees ALL documents (all users)
        analytics_data = db.get_analytics_data(user_id=None)
    else:
        # Regular users see only THEIR documents
        analytics_data = db.get_analytics_data(user_id=user_data['id'])
    
    return analytics_data
```

**Access Control:**
- **Admin**: Sees all users' documents in analytics
- **Regular User**: Sees only their own documents in analytics

---

## What's Now Included in Analytics

### **Data Sources Combined:**

| Data Source | Table | Included? |
|-------------|-------|-----------|
| AI Document Classification | `ai_document_classifications` | ✅ Yes |
| GhostLayer AI Documents | `user_ghostlayer_documents` | ✅ Yes (NEW!) |
| Old Documents | `documents` | ❌ No (deprecated) |
| Old GhostLayer | `ghostlayer_documents` | ❌ No (deprecated) |

---

### **Charts Updated:**

#### **1. Document Types Distribution (Doughnut Chart)**
**Before:** Only AI classification types  
**After:** AI + GhostLayer types **combined and aggregated**

Example:
```
Aadhaar: 45 docs (30 from AI + 15 from GhostLayer)
Invoice: 30 docs (25 from AI + 5 from GhostLayer)
```

#### **2. Criticality Levels (Bar Chart)**
**Before:** Only from old `documents` table  
**After:** From `ai_document_classifications` table  
**Note:** GhostLayer documents don't have criticality levels

#### **3. Processing Trends (Line Chart - 30 days)**
**Before:** Only AI documents  
**After:** AI + GhostLayer **combined by date**

Shows total uploads per day from both sources.

#### **4. File Types Distribution (Pie Chart)**
**Before:** Only AI file types  
**After:** AI file_type + GhostLayer document_format **combined**

Example:
```
PNG: 40 files (10 from AI + 30 from GhostLayer)
PDF: 35 files (30 from AI + 5 from GhostLayer)
```

---

### **KPI Metrics Updated:**

| Metric | Before | After |
|--------|--------|-------|
| Total Documents | Only AI | ✅ AI + GhostLayer |
| Processed Today | Only AI | ✅ AI + GhostLayer |
| Error Rate | Only AI | ✅ AI + GhostLayer |
| Success Rate | Only AI | ✅ AI + GhostLayer |

**New Metrics Added:**
- `ai_documents`: Count of AI classification docs
- `ghostlayer_documents`: Count of GhostLayer docs

---

## User-Specific vs Admin Analytics

### **Regular User Analytics:**
- Shows ONLY their own documents
- AI Classification + GhostLayer combined
- Personal trends, types, and statistics
- Privacy-focused

### **Admin Analytics:**
- Shows ALL users' documents
- System-wide AI + GhostLayer analytics
- All document types across all users
- Complete oversight

---

## Database Query Strategy

### **User-Specific Queries:**
```sql
-- AI Documents
SELECT ... FROM ai_document_classifications 
WHERE user_id = 5  -- Specific user

-- GhostLayer Documents
SELECT ... FROM user_ghostlayer_documents 
WHERE user_id = 5  -- Specific user
```

### **Admin Queries (All Data):**
```sql
-- AI Documents
SELECT ... FROM ai_document_classifications 
-- No WHERE clause = all users

-- GhostLayer Documents
SELECT ... FROM user_ghostlayer_documents 
-- No WHERE clause = all users
```

---

## Testing Verification

### **Test Data Status:**
From `app/idms.db`:
- ✅ 1 GhostLayer document exists (aadhaar by user1)
- ❌ 0 AI Classification documents
- ✅ 2 users (admin + user1)

### **To Properly Test:**
1. Upload some AI Classification documents
2. Upload more GhostLayer documents
3. Use multiple users
4. Check analytics shows combined data

---

## Files Modified

1. ✅ `app/database.py` - Updated `get_analytics_data()` method
   - Added `user_id` parameter
   - Queries both AI and GhostLayer tables
   - Combines results intelligently
   
2. ✅ `app/main.py` - Updated `/api/analytics` endpoint
   - Added user authentication
   - Filters by user_id for regular users
   - Admin sees all data

---

## Impact

### **Before:**
```
Analytics Dashboard
├─ Document Types: Empty (queried old 'documents' table)
├─ Criticality: Empty
├─ Trends: Empty
└─ File Types: Empty
```

### **After:**
```
Analytics Dashboard
├─ Document Types: AI + GhostLayer combined ✅
├─ Criticality: From AI documents ✅
├─ Trends: AI + GhostLayer combined by date ✅
├─ File Types: AI + GhostLayer formats ✅
└─ User-filtered: Shows only user's own data ✅
```

---

## Next Steps to See Data in Analytics

### **Upload Test Documents:**
```
1. Login as user1
2. Upload AI Classification documents (PDF, DOCX, etc.)
3. Upload more GhostLayer documents (PNG, JPG)
4. Navigate to Analytics Dashboard
5. You should now see:
   ✅ Combined document counts
   ✅ Document types from both sources
   ✅ Processing trends
   ✅ File type distribution
```

---

**Status**: ✅ **FIXED** - Analytics now includes **both** AI Document Classification **and** GhostLayer AI documents, with proper user-specific filtering!
