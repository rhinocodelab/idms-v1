# GhostLayer View Permissions Implementation

## 🎯 **Overview**
Enhanced the GhostLayer AI module with granular view permissions, allowing administrators to control whether users can view original documents, redacted documents, or both.

## ✅ **Implementation Summary**

### **1. Database Schema Enhancement**
Added new columns to the `users` table:
- `ghostlayer_view_original BOOLEAN DEFAULT 1` - Permission to view original documents
- `ghostlayer_view_redacted BOOLEAN DEFAULT 1` - Permission to view redacted documents

### **2. User Management Interface**
Enhanced Create/Edit User forms with sub-permissions:
- **Main Checkbox**: GhostLayer AI Access
- **Sub-checkboxes**:
  - View Original Documents
  - View Redacted Documents
- **Smart UI**: Sub-permissions show/hide based on main checkbox state

### **3. Backend Security**
Added permission checks in API endpoints:
- `/api/ghostlayer/original/{document_id}` - Checks `ghostlayer_view_original` permission
- `/api/ghostlayer/view/{document_id}` - Checks `ghostlayer_view_redacted` permission
- Enhanced error handling with specific permission messages

### **4. Frontend Document Viewer**
Updated `ghostlayer_view.html` with permission-based UI:
- **Tab Visibility**: Hides tabs based on user permissions
- **Content Loading**: Only loads images user has permission to view
- **Smart Navigation**: Hides tab navigation when user has only one permission
- **Error Handling**: Shows appropriate error messages for permission denials

## 🔒 **Permission Combinations**

### **1. Full Access (Default)**
- ✅ View Original Documents
- ✅ View Redacted Documents
- **UI**: Full tab navigation with both tabs visible

### **2. Original Only**
- ✅ View Original Documents
- ❌ View Redacted Documents
- **UI**: Single view showing only original content

### **3. Redacted Only**
- ❌ View Original Documents
- ✅ View Redacted Documents
- **UI**: Single view showing only redacted content

### **4. No Access**
- ❌ View Original Documents
- ❌ View Redacted Documents
- **UI**: Error message - "No permission to view documents"

## 🛠 **Technical Implementation**

### **Database Changes**
```sql
-- Migration automatically adds these columns
ALTER TABLE users ADD COLUMN ghostlayer_view_original BOOLEAN DEFAULT 1;
ALTER TABLE users ADD COLUMN ghostlayer_view_redacted BOOLEAN DEFAULT 1;
```

### **API Endpoints**
```python
# Original image with permission check
@app.get("/api/ghostlayer/original/{document_id}")
async def get_ghostlayer_original_image(request: Request, document_id: int):
    # Checks ghostlayer_view_original permission
    if not user_data.get('ghostlayer_view_original', False):
        raise HTTPException(status_code=403, detail="No permission to view original documents")

# Redacted image with permission check  
@app.get("/api/ghostlayer/view/{document_id}")
async def get_ghostlayer_marked_image(request: Request, document_id: int):
    # Checks ghostlayer_view_redacted permission
    if not user_data.get('ghostlayer_view_redacted', False):
        raise HTTPException(status_code=403, detail="No permission to view redacted documents")
```

### **Frontend JavaScript**
```javascript
// Check user permissions and configure UI
function checkUserPermissions() {
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    
    // Hide tabs based on permissions
    if (!userData.ghostlayer_view_original) {
        document.getElementById('tab-original').style.display = 'none';
    }
    
    if (!userData.ghostlayer_view_redacted) {
        document.getElementById('tab-marked').style.display = 'none';
    }
}
```

## 📋 **User Experience**

### **Admin Workflow**
1. **Create User**: Select GhostLayer AI access + sub-permissions
2. **Edit User**: Modify existing user permissions
3. **User Management**: View permission status in user table

### **User Workflow**
1. **Access Control**: Users only see what they have permission for
2. **Seamless Experience**: No broken links or error pages
3. **Clear Feedback**: Appropriate error messages for permission denials

## 🔐 **Security Benefits**

### **Data Privacy**
- **Sensitive Data Protection**: Control who can see original documents
- **Compliance**: Meet regulatory requirements for data access
- **Audit Trail**: Track who accessed what type of documents

### **Role-Based Access**
- **Analysts**: May only need redacted documents for analysis
- **Reviewers**: May need original documents for verification
- **Viewers**: May only need redacted documents for general viewing

## 🧪 **Testing Scenarios**

### **Test Cases**
1. **Full Access User**: Can view both original and redacted documents
2. **Original Only User**: Can only view original documents, redacted tab hidden
3. **Redacted Only User**: Can only view redacted documents, original tab hidden
4. **No Access User**: Cannot access document viewer at all
5. **Permission Changes**: Real-time updates when admin modifies permissions

### **Error Handling**
- **403 Forbidden**: When user lacks specific permission
- **404 Not Found**: When document doesn't exist
- **401 Unauthorized**: When user is not authenticated

## 📊 **Database Migration**

The system automatically migrates existing users:
- **Existing Users**: Get default permissions (both original and redacted access)
- **New Users**: Get permissions based on admin selection
- **Backward Compatibility**: No data loss during migration

## 🚀 **Deployment Notes**

### **Requirements**
- Database migration runs automatically on startup
- No manual intervention required
- Backward compatible with existing users

### **Configuration**
- Permissions are stored in user records
- No additional configuration files needed
- Admin interface provides full control

## ✅ **Status: COMPLETED**

All components have been successfully implemented:
- ✅ Database schema updated
- ✅ User management interface enhanced
- ✅ Backend APIs secured
- ✅ Frontend viewer updated
- ✅ Permission system fully functional

---

**Date:** September 30, 2025  
**Version:** GhostLayer Permissions v1.0  
**Status:** Ready for Production
