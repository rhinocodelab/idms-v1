# Admin Module Access Control - User Guide

## 🎯 **How to Update User Module Access**

### **Method 1: Edit Existing User**

#### **Step-by-Step Process:**

1. **Navigate to User Management**
   - Login as admin
   - Click "User Management" in the sidebar
   - You'll see the User Management table

2. **Find the User**
   - Look for the user in the table
   - Check the "Module Access" column to see current permissions

3. **Click Edit Button**
   - Click the blue "Edit" button (pencil icon) in the Actions column
   - The Edit User modal will open

4. **Modify Module Access**
   ```
   ┌─────────────────────────────────────────────────────────┐
   │ EDIT USER: user1                                        │
   ├─────────────────────────────────────────────────────────┤
   │                                                         │
   │ Basic Information:        Settings & Role:              │
   │ Username: user1          ☑️ Active User                │
   │ Full Name: [User One]    ☐ Enable MFA                 │
   │ Email: [user1@...]      Role: [Analyst ▼]            │
   │                           Module Access:                │
   │                           ☐ AI Document Classification  │
   │                           ☑️ GhostLayer AI             │
   │                                                         │
   │                    [Cancel] [Update User]               │
   └─────────────────────────────────────────────────────────┘
   ```

5. **Update Permissions**
   - Check/uncheck the module access boxes as needed:
     - ☑️ **AI Document Classification**: User can upload and classify documents
     - ☑️ **GhostLayer AI**: User can use GhostLayer OCR features
   - Click "Update User"

6. **Verify Changes**
   - The modal will close
   - The user table will refresh automatically
   - Check the "Module Access" column to confirm changes

---

### **Method 2: Create New User with Specific Access**

#### **Step-by-Step Process:**

1. **Click "Add User" Button**
   - In User Management page
   - Click the blue "Add User" button

2. **Fill User Information**
   - Enter username, full name, password
   - Select role (Analyst/Manager/Viewer)

3. **Set Module Access**
   ```
   ┌─────────────────────────────────────────────────────────┐
   │ CREATE NEW USER                                        │
   ├─────────────────────────────────────────────────────────┤
   │                                                         │
   │ Basic Information:        Settings & Role:              │
   │ Username: [new_user]      ☑️ Active User                │
   │ Full Name: [John Doe]     ☐ Enable MFA                 │
   │ Password: [password123]   Role: [Analyst ▼]            │
   │                           Module Access:                │
   │                           ☑️ AI Document Classification  │
   │                           ☐ GhostLayer AI             │
   │                                                         │
   │                    [Cancel] [Create User]               │
   └─────────────────────────────────────────────────────────┘
   ```

4. **Configure Access**
   - Check the modules you want the user to access
   - Uncheck modules you want to restrict
   - Click "Create User"

---

## 📊 **Understanding Module Access Indicators**

### **In User Management Table:**

```
┌─────────────────────────────────────────────────────────┐
│ USER MANAGEMENT TABLE                                   │
├─────────────────────────────────────────────────────────┤
│ User    │ Role    │ Module Access        │ Actions     │
├─────────┼─────────┼──────────────────────┼─────────────┤
│ user1   │ Analyst │ ✅ AI Class          │ [Edit]     │
│         │         │ ❌ GhostLayer         │            │
├─────────┼─────────┼──────────────────────┼─────────────┤
│ user2   │ Manager │ ❌ AI Class          │ [Edit]     │
│         │         │ ✅ GhostLayer         │            │
├─────────┼─────────┼──────────────────────┼─────────────┤
│ user3   │ Analyst │ ✅ AI Class          │ [Edit]     │
│         │         │ ✅ GhostLayer         │            │
└─────────┴─────────┴──────────────────────┴─────────────┘
```

### **Indicator Meanings:**
- ✅ **Green Checkmark**: User has access to this module
- ❌ **Red X**: User does NOT have access to this module

---

## 🎯 **Common Scenarios**

### **Scenario 1: Restrict AI Classification Access**
**Goal**: User can only use GhostLayer AI, not document classification

**Steps**:
1. Click "Edit" for the user
2. Uncheck "AI Document Classification"
3. Keep "GhostLayer AI" checked
4. Click "Update User"

**Result**: User will only see "GhostLayer AI" menu, not "Upload Documents"

### **Scenario 2: Restrict GhostLayer Access**
**Goal**: User can only upload documents, not use GhostLayer

**Steps**:
1. Click "Edit" for the user
2. Keep "AI Document Classification" checked
3. Uncheck "GhostLayer AI"
4. Click "Update User"

**Result**: User will only see "Upload Documents" menu, not "GhostLayer AI"

### **Scenario 3: Full Access**
**Goal**: User can access both modules

**Steps**:
1. Click "Edit" for the user
2. Check both "AI Document Classification" and "GhostLayer AI"
3. Click "Update User"

**Result**: User will see both menus

### **Scenario 4: No Module Access**
**Goal**: User can only view analytics, no document processing

**Steps**:
1. Click "Edit" for the user
2. Uncheck both modules
3. Click "Update User"

**Result**: User will only see "Analytics" menu

---

## 🔧 **Technical Details**

### **What Happens When You Update Access:**

1. **Immediate Effect**: Changes apply instantly
2. **Menu Updates**: User's sidebar menu updates automatically
3. **Session Persistence**: Changes persist across user logins
4. **Database Update**: Permissions stored in database

### **Admin Override:**
- **Admins always see all menus** regardless of their own module access
- **Admins can edit any user's permissions**
- **Admins cannot restrict their own access**

### **User Experience:**
- **Restricted users**: Don't see menus they can't access
- **Clean interface**: No confusion about available features
- **Immediate feedback**: Menu changes when permissions change

---

## 🚨 **Important Notes**

### **Before Making Changes:**
- ✅ **Consider user workflow**: What does this user actually need?
- ✅ **Check current usage**: Are they actively using these features?
- ✅ **Communicate changes**: Let users know about permission changes

### **After Making Changes:**
- ✅ **Test user experience**: Login as the user to verify menu changes
- ✅ **Monitor usage**: Check if users can still do their work
- ✅ **Be ready to adjust**: Permissions can be changed anytime

### **Best Practices:**
- ✅ **Start restrictive**: Give minimal access, add more as needed
- ✅ **Document changes**: Keep track of why permissions were changed
- ✅ **Regular review**: Periodically check if users still need their access level

---

## 🎉 **Quick Reference**

### **Permission Matrix:**
| Module Access | Upload Documents | GhostLayer AI | Analytics |
|---------------|-----------------|---------------|-----------|
| **AI Classification** | ✅ Shows | ❌ Hidden | ✅ Shows |
| **GhostLayer AI** | ❌ Hidden | ✅ Shows | ✅ Shows |
| **Both Modules** | ✅ Shows | ✅ Shows | ✅ Shows |
| **No Modules** | ❌ Hidden | ❌ Hidden | ✅ Shows |

### **Admin Actions:**
- ✅ **View permissions**: Check "Module Access" column
- ✅ **Edit permissions**: Click blue "Edit" button
- ✅ **Create users**: Use "Add User" with specific access
- ✅ **Monitor changes**: Watch for immediate menu updates

**The module access control system is now fully functional and ready for use!** 🚀
