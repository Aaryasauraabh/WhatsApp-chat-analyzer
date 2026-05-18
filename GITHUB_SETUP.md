# 🐙 GitHub Quick Setup Guide

## Minutes to Get Your Code on GitHub

### **What is GitHub?**
- Cloud storage for your code
- Streamlit Cloud will access it from here
- Free version control system

---

## 5-Minute Setup

### **Step 1: Create GitHub Account** (3 minutes)

1. Go to https://github.com/signup
2. Enter email address
3. Create password
4. Choose username (remember this!)
5. Click **Create account**
6. Verify email
7. Done!

---

### **Step 2: Install Git** (2 minutes)

**Windows:**
1. Download from: https://git-scm.com/download/win
2. Run installer (click Next → Next → Install)
3. Open PowerShell or Command Prompt
4. Type: `git --version`
5. Should show: `git version 2.xx.x`

**Mac:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt-get install git
```

---

### **Step 3: Create Repository on GitHub** (2 minutes)

1. Log in to GitHub
2. Click **+** (top right corner)
3. Click **New repository**
4. **Repository name**: `whatsapp-chat-analyzer`
5. **Description**: `ML + NLP project to analyze WhatsApp chats`
6. **Public**: ✅ (so Streamlit can access it)
7. Click **Create repository**

**Copy the URL** - looks like:
```
https://github.com/YOUR_USERNAME/whatsapp-chat-analyzer.git
```

---

### **Step 4: Push Your Project to GitHub** (Your Code Upload)

Open PowerShell in your project folder:

```bash
cd C:\Users\gabba\Desktop\Destop2\ML\ project\whatsapp-chat-analyzer

# Initialize Git
git init

# Configure Git (one time only)
git config --global user.name "Your Name"
git config --global user.email "your-email@gmail.com"

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: WhatsApp Chat Analyzer project"

# Add GitHub remote (paste YOUR repo URL)
git remote add origin https://github.com/YOUR_USERNAME/whatsapp-chat-analyzer.git

# Push code to GitHub
git branch -M main
git push -u origin main
```

**When prompted:**
- Username: Your GitHub username
- Password: Your GitHub password (or personal access token)

---

### **Step 5: Verify Upload** ✅

1. Open: `https://github.com/YOUR_USERNAME/whatsapp-chat-analyzer`
2. Should see all your project files
3. Done!

---

## Future Updates

Every time you update your code:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will **automatically redeploy** in 1-2 minutes!

---

## 🆘 Common Issues

### **"fatal: could not read Username"**

Solution:
```bash
# Use personal access token instead of password
# Generate at: https://github.com/settings/tokens
# Click "Generate new token"
# Paste the token instead of password
```

### **"fatal: 'origin' does not appear to be a git repository"**

Solution:
```bash
git remote add origin https://github.com/YOUR_USERNAME/whatsapp-chat-analyzer.git
```

### **"Everything up-to-date" but no files on GitHub**

Check:
- [ ] You ran `git push origin main`
- [ ] No errors in console
- [ ] Refreshed GitHub page

---

## ✅ You're Ready for Streamlit Deployment!

Next: Follow the [DEPLOYMENT.md](DEPLOYMENT.md) guide to deploy on Streamlit Cloud.

---

**Time saved: 5 minutes! 🎉**
