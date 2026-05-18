# 🚀 Quick Start Guide

## 5-Minute Setup

### **1. Install Python (if not already installed)**
Download from: https://www.python.org/downloads/

### **2. Open Command Prompt in the project folder**
```bash
cd C:\Users\gabba\Desktop\Destop2\ML\ project\whatsapp-chat-analyzer
```

### **3. Install dependencies**
```bash
pip install -r requirements.txt
```

### **4. Download NLTK data**
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### **5. Run the application**
```bash
streamlit run app.py
```

**The app will open automatically in your browser!**

---

## 📱 How to Export WhatsApp Chat

1. Open WhatsApp
2. Go to the chat you want to analyze
3. Tap Menu ⋮ → **More** → **Export Chat**
4. Choose **"Without Media"**
5. Save the `.txt` file

---

## 📊 Features at a Glance

| Feature | What It Does |
|---------|-------------|
| **Overview** | Quick stats (messages, users, words) |
| **User Analysis** | See who talks most, individual profiles |
| **Activity Trends** | Daily/weekly/hourly patterns |
| **NLP Analysis** | Words, emojis, sentiment, hashtags |
| **ML Insights** | Topics, keywords, predictions |

---

## 💡 Example: Analyze the Sample Chat

```bash
# 1. The sample chat is in: data/sample_chat.txt
# 2. When you run the app, click "Browse files"
# 3. Select: data/sample_chat.txt
# 4. Explore all the tabs!
```

---

## ❓ Need Help?

See **README.md** for:
- Complete installation guide
- Detailed feature explanations
- Code walkthroughs
- Troubleshooting tips
- Full documentation

---

**Version**: 1.0.0  
**Ready to go!** 🎉
