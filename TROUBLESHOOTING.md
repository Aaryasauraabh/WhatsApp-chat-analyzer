# 🆘 Troubleshooting Guide

Common deployment issues and solutions.

---

## 🔴 Critical Issues

### **1. "ModuleNotFoundError: No module named 'X'"**

**Error Message:**
```
ModuleNotFoundError: No module named 'nltk'
```

**Cause:** Package not in `requirements.txt`

**Solution:**
1. Check what's imported in your code: `import nltk`
2. Add to `requirements.txt`:
   ```
   nltk>=3.6.0
   ```
3. Push to GitHub:
   ```bash
   git add requirements.txt
   git commit -m "Add missing package"
   git push origin main
   ```
4. Streamlit will redeploy automatically (1 minute)

**Prevention:** Add ALL `import` statements to requirements.txt

---

### **2. "FileNotFoundError: [Errno 2] No such file or directory"**

**Error Message:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'C:\Users\...'
```

**Cause:** Hardcoded file paths (Windows paths don't work on cloud)

**Solution:**
```python
# WRONG ❌
file_path = "C:\\Users\\YourName\\project\\data\\sample.txt"

# CORRECT ✅
from pathlib import Path
file_path = Path(__file__).parent / "data" / "sample.txt"

# OR
import os
file_path = os.path.join("data", "sample.txt")
```

**Prevention:** Use relative paths only!

---

### **3. "App crashed - RuntimeError: Application failed to start"**

**Error:**
App crashes during startup with no specific error message

**Causes & Solutions:**

**a) Missing NLTK data**
```python
# Add to top of app.py
import nltk

@st.cache_resource
def download_nltk_data():
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

download_nltk_data()
```

**b) Syntax error in code**
- Check logs for specific lines
- Test locally: `streamlit run app.py`
- Fix and push

**c) Incompatible package version**
- Update requirements.txt with version pins:
  ```
  pandas>=1.3.0,<2.0.0
  ```

---

### **4. "TimeoutError - App took too long to load"**

**Error:** App loads for > 5 minutes then times out

**Causes:**
- Heavy computations at startup
- Missing caching decorators
- Large file processing

**Solutions:**

**Add caching:**
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def slow_function():
    # Your code
    return result
```

**Move heavy imports:**
```python
# DON'T do at top
# from sklearn import * 

# DO inside function
def my_function():
    from sklearn import ensemble
    # Use it
```

**Lazy load data:**
```python
# DON'T load at startup
# df = pd.read_csv('huge_file.csv')

# DO load only when needed
if st.button('Load data'):
    df = pd.read_csv('huge_file.csv')
```

---

## 🟡 Common Issues

### **5. "MemoryError" or "Out of memory"**

**Error:**
```
MemoryError: Unable to allocate memory
```

**Cause:** Too much data in memory

**Solutions:**
```python
import gc
import matplotlib.pyplot as plt

# After using data
plt.close('all')  # Close all figures
del large_dataframe
gc.collect()      # Free memory
```

Add to end of processing blocks:
```python
st.success("Done!")
gc.collect()
```

---

### **6. "Emoji not displaying properly"**

**Error:** Emoji appears as blank or symbol

**Cause:** Emoji package issue

**Solution:**
Check `requirements.txt`:
```
emoji>=1.6.0
Pillow>=9.0.0
```

Update if needed:
```bash
git add requirements.txt
git commit -m "Update emoji package"
git push origin main
```

---

### **7. "Connection refused" or "Cannot reach GitHub"**

**Error:**
```
fatal: could not read Username for 'https://github.com'
```

**Cause:** GitHub authentication issue

**Solution:**

**Option A: Use Personal Access Token**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `gist`
4. Copy token
5. Use token as password when pushing:
   ```bash
   git push origin main
   # Username: your-username
   # Password: paste-your-token-here
   ```

**Option B: Configure SSH**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@gmail.com"

# Add to GitHub: https://github.com/settings/keys

# Test
ssh -T git@github.com
```

---

### **8. "Blank page" or "App not responding"**

**Error:** App loads but shows blank screen

**Cause:** 
- Session state issues
- Missing imports
- Error in rendering

**Solution:**
1. Check Streamlit Cloud logs
2. Check browser console (F12 - Console tab)
3. Test locally: `streamlit run app.py`
4. Look for error messages

---

### **9. "Charts not displaying" or "Empty visualizations"**

**Error:** Charts load but appear empty/broken

**Cause:**
- matplotlib backend issue
- DPI too high
- Missing Pillow package

**Solution:**
```python
# In requirements.txt, ensure:
matplotlib>=3.4.0,<4.0.0
Pillow>=9.0.0

# In your plotting code:
fig, ax = plt.subplots(figsize=(12, 6), dpi=100)  # DPI=100, not 300
# ... code ...
st.pyplot(fig)
```

---

### **10. "File upload limit exceeded"**

**Error:** Cannot upload files > 200 MB

**Cause:** Default Streamlit file limit

**Solution:**
In `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 500  # Increase to 500 MB
```

---

## 🟢 Minor Issues

### **11. "App is slow on first load"**

**Normal behavior.** Streamlit Cloud boots up your app on first request.

**Solutions:**
1. Add caching (see #4)
2. Be patient (1-2 minutes is normal)
3. Subsequent loads will be faster

---

### **12. "Dashboard looks different on mobile"**

**Cause:** Responsive design issues

**Solution:**
```python
# Make mobile-friendly
if st.checkbox("Expand view"):
    col1, col2 = st.columns(1)
else:
    col1, col2 = st.columns(2)
```

---

### **13. "Git push rejected"**

**Error:**
```
[rejected] main -> main (fetch first)
```

**Solution:**
```bash
git pull origin main
git push origin main
```

---

## 🔍 Debugging Steps

**If you get an error you don't recognize:**

1. **Check the logs:**
   - Go to your app on Streamlit Cloud
   - Click "Manage app" (bottom right)
   - Click "Logs" tab
   - Look for error messages

2. **Test locally first:**
   ```bash
   streamlit run app.py
   ```
   - Errors show in your terminal
   - Easier to debug locally

3. **Check requirements.txt:**
   ```bash
   pip install -r requirements.txt
   ```
   - Test if all packages install

4. **Check file paths:**
   - Look for hardcoded paths
   - Use relative paths instead

5. **Check imports:**
   - Every `import X` needs `X` in requirements.txt
   - Verify spelling

6. **Simplify and test:**
   - Comment out complex code
   - Push simpler version
   - Add back piece by piece

---

## 📞 Getting Help

**Can't solve it? Try:**

1. **Streamlit Documentation:** https://docs.streamlit.io
2. **Streamlit Forum:** https://discuss.streamlit.io
3. **Stack Overflow:** Tag: `streamlit`
4. **GitHub Issues:** In official Streamlit repo
5. **YouTube Tutorials:** "Streamlit deployment errors"

---

## ✅ Common Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| ModuleNotFoundError | Add to requirements.txt |
| FileNotFoundError | Use relative paths only |
| TimeoutError | Add @st.cache_data |
| MemoryError | Add gc.collect() |
| Blank page | Check logs, test locally |
| Slow load | Add caching |
| Charts empty | Update requirements.txt |
| Won't push to Git | `git pull` then `git push` |

---

**Version:** 1.0.0  
**Last Updated:** 2024
