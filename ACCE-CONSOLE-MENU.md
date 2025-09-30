# ACCE Console Menu - Admin-Only External Link

## Overview
Added a new "ACCE Console" menu item in the sidebar navigation that is **only visible to admin users**. This menu opens an external ACCE Console login page in a new browser tab.

---

## Implementation Details

### **Menu Item Added**
**Location:** Sidebar navigation (after "Database" menu)

**HTML:**
```html
<!-- ACCE Console - Admin Only -->
<div id="acce-console-menu" class="hidden">
    <a href="https://win-1gpq0nalnpb:9443/acce/login.jsp" target="_blank" 
       class="flex items-center px-4 py-3 text-gray-300 hover:bg-gray-800 hover:text-white mb-2 transition-colors duration-200">
        <i class="fas fa-external-link-alt mr-3"></i>
        <span>ACCE Console</span>
    </a>
</div>
```

**Features:**
- 🔗 **External Link**: Opens `https://win-1gpq0nalnpb:9443/acce/login.jsp`
- 🆕 **New Tab**: `target="_blank"` opens in new browser tab
- 🔒 **Admin-Only**: Hidden by default, shown only for admin role
- 🎨 **External Link Icon**: `fa-external-link-alt` indicates external resource
- 🖱️ **Hover Effect**: Highlights on hover like other menu items

---

## Visibility Control

### **JavaScript Logic:**
```javascript
const acceConsoleMenu = document.getElementById('acce-console-menu');

if (userData.role === 'admin') {
    acceConsoleMenu.classList.remove('hidden');  // Show for admin
} else {
    if (acceConsoleMenu) acceConsoleMenu.classList.add('hidden');  // Hide for others
}
```

**Access Control:**
- ✅ **Admin users**: Menu item visible
- ❌ **Manager users**: Menu item hidden
- ❌ **Analyst users**: Menu item hidden
- ❌ **Viewer users**: Menu item hidden

---

## Navigation Menu Structure

### **Admin Users See:**
```
IDMS Sidebar Menu
├─ 🏠 Dashboard
├─ 👥 User Management
├─ 📤 Upload Documents
│  └─ 🧠 AI Document Classification
├─ 👻 GhostLayer AI
├─ ⚙️ API Endpoint
├─ 📊 Analytics
├─ 🗄️ Database
└─ 🔗 ACCE Console ← NEW (Admin Only)
   Opens: https://win-1gpq0nalnpb:9443/acce/login.jsp
```

### **Regular Users See:**
```
IDMS Sidebar Menu
├─ 🏠 Dashboard
├─ 📤 Upload Documents
│  └─ 🧠 AI Document Classification
├─ 👻 GhostLayer AI
└─ 📊 Analytics
```

---

## Menu Item Properties

| Property | Value |
|----------|-------|
| **Label** | ACCE Console |
| **Icon** | 🔗 External Link (`fa-external-link-alt`) |
| **URL** | https://win-1gpq0nalnpb:9443/acce/login.jsp |
| **Target** | _blank (new tab) |
| **Visibility** | Admin only |
| **Has Page Component** | No (external link) |

---

## Security Considerations

### ✅ **Frontend Visibility Control:**
- Menu item hidden in HTML by default (`class="hidden"`)
- JavaScript shows it only for admin users
- Non-admin users never see the menu item

### ⚠️ **Note on Security:**
This is **frontend-only hiding**. The external URL itself is not protected by IDMS authentication. Users who know the URL could access it directly. The ACCE Console login page should have its own authentication.

**Recommendation:** ACCE Console should have its own login/authentication system (which it likely does).

---

## ACCE Console Details

**URL:** `https://win-1gpq0nalnpb:9443/acce/login.jsp`

**Components:**
- **Protocol**: HTTPS (secure)
- **Host**: win-1gpq0nalnpb
- **Port**: 9443
- **Path**: /acce/login.jsp

**Purpose:** External ACCE (Administration Console for Content Platform Engine) - IBM FileNet administration console for content management and document processing workflows.

---

## Icon Consistency

All admin-only menu items now have appropriate icons:
- 👥 User Management: `fa-users`
- ⚙️ API Endpoint: `fa-cogs`
- 🗄️ Database: `fa-database`
- 🔗 ACCE Console: `fa-external-link-alt` (indicates external link)

The external link icon (`fa-external-link-alt`) clearly indicates this menu item opens an external resource.

---

## Testing

### **Test as Admin:**
1. **Login as admin** (username: `admin`, password: `admin123`)
2. **Check sidebar navigation**
3. **Verify you see:**
   - ✅ "ACCE Console" menu item
   - ✅ External link icon (🔗)
4. **Click "ACCE Console"**
5. **Verify:**
   - ✅ Opens in new browser tab
   - ✅ URL: https://win-1gpq0nalnpb:9443/acce/login.jsp
   - ✅ IDMS tab remains open

### **Test as Regular User:**
1. **Login as analyst/manager/viewer**
2. **Check sidebar navigation**
3. **Verify:**
   - ❌ "ACCE Console" menu item NOT visible
   - ❌ Cannot access via UI

---

## Files Modified

- ✅ `app/templates/base.html` - Added ACCE Console menu item + visibility control

---

## Future Enhancements (Optional)

### **Possible Improvements:**
1. **SSO Integration**: Auto-login to ACCE Console using IDMS session
2. **Iframe Embed**: Embed ACCE Console within IDMS (if CORS allows)
3. **Role-Based URL**: Different ACCE Console URLs for different admin types
4. **Status Indicator**: Show ACCE Console connection status in System Status section
5. **Quick Actions**: Add "Open ACCE" button in Admin Dashboard

---

**Status**: ✅ **COMPLETE** - ACCE Console menu added to sidebar (admin-only, opens in new tab)
