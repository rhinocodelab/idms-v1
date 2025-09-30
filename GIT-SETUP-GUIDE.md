# Git Setup and GitHub Push Guide for IDMS

## Problem
```
error: src refspec main does not match any
error: failed to push some refs to 'https://github.com/rhinocodelab/idms-v1.git'
```

## Root Cause
Git is not installed on your Windows system.

---

## Solution

### **Step 1: Install Git**

#### **Option A: Download Git for Windows (Recommended)**
1. Visit: https://git-scm.com/download/win
2. Download the latest version (64-bit)
3. Run the installer
4. **Important Settings During Installation:**
   - ✅ Use Git from the Windows Command Prompt
   - ✅ Use the OpenSSL library
   - ✅ Checkout Windows-style, commit Unix-style line endings
   - ✅ Use MinTTY (default terminal)
   - ✅ Default branch name: `main`

5. After installation, **restart your terminal/PowerShell**

#### **Option B: Install via Chocolatey (If you have Chocolatey)**
```powershell
choco install git -y
```

#### **Option C: Install via Winget (Windows Package Manager)**
```powershell
winget install --id Git.Git -e --source winget
```

---

### **Step 2: Configure Git (First Time Setup)**

After installing Git, configure your identity:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

### **Step 3: Initialize Git Repository**

```powershell
# Navigate to your project directory (if not already there)
cd C:\Users\prashant\Projects\idms

# Initialize git repository
git init

# Check current branch name
git branch

# If no branch exists yet, create initial commit
git add .
git commit -m "Initial commit: IDMS v1 with admin features"
```

---

### **Step 4: Set Default Branch to 'main'**

If your branch is named "master" but GitHub expects "main":

```powershell
# Rename branch from master to main
git branch -M main
```

---

### **Step 5: Add GitHub Remote**

```powershell
# Add your GitHub repository as remote
git remote add origin https://github.com/rhinocodelab/idms-v1.git

# Or if remote already exists, update it
git remote set-url origin https://github.com/rhinocodelab/idms-v1.git
```

---

### **Step 6: Push to GitHub**

#### **Option A: First Time Push**
```powershell
# Push to main branch (first time)
git push -u origin main
```

#### **Option B: If Repository Already Has Content**
```powershell
# Pull first, then push
git pull origin main --allow-unrelated-histories
git push -u origin main
```

#### **Option C: Force Push (Use with Caution)**
```powershell
# Force push (overwrites remote)
git push -u origin main --force
```

---

### **Step 7: Verify Push**

```powershell
# Check remote URL
git remote -v

# Check branch
git branch

# Check status
git status
```

---

## Common Errors & Solutions

### **Error: "src refspec main does not match any"**
**Cause:** No commits exist yet or branch not named "main"

**Solution:**
```powershell
# Create initial commit if none exists
git add .
git commit -m "Initial commit"

# Rename branch to main if needed
git branch -M main

# Push
git push -u origin main
```

---

### **Error: "failed to push some refs"**
**Cause:** Remote has commits that local doesn't have

**Solution:**
```powershell
# Pull first
git pull origin main --rebase

# Then push
git push -u origin main
```

---

### **Error: "Permission denied"**
**Cause:** Authentication issue with GitHub

**Solution:**
1. Use Personal Access Token (PAT) instead of password
2. Generate PAT at: https://github.com/settings/tokens
3. Use PAT when prompted for password

Or use SSH:
```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to GitHub: https://github.com/settings/keys

# Change remote to SSH
git remote set-url origin git@github.com:rhinocodelab/idms-v1.git
```

---

## Quick Reference

### **First Time Git Setup (Complete)**
```powershell
# 1. Install Git (download from git-scm.com)

# 2. Configure Git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 3. Initialize repository
cd C:\Users\prashant\Projects\idms
git init

# 4. Create .gitignore
# (Add venv/, __pycache__/, *.db, .env, etc.)

# 5. Add all files
git add .

# 6. Create initial commit
git commit -m "Initial commit: IDMS project"

# 7. Rename to main branch
git branch -M main

# 8. Add remote
git remote add origin https://github.com/rhinocodelab/idms-v1.git

# 9. Push to GitHub
git push -u origin main
```

---

## .gitignore Recommended

Create a `.gitignore` file in your project root:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3

# Environment
.env
*.env

# Temp files
temp/
tmp/
app/temp/
upload_ghostlayer_docs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log

# Credentials
ghostlayer.json
isl.json
*.ini
```

---

## Post-Push Verification

After successful push, verify at:
```
https://github.com/rhinocodelab/idms-v1
```

You should see:
- ✅ All your project files
- ✅ README.md displayed
- ✅ File structure visible
- ✅ Commit history

---

**Next Steps After Git Setup:**
1. Install Git
2. Restart PowerShell
3. Run the git commands above
4. Push to GitHub
5. Verify on GitHub website
