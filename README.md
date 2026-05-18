# 📱 WhatsApp Chat Analyzer

## Complete Guide to Building & Using the Project

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation & Setup](#installation--setup)
5. [How to Run](#how-to-run)
6. [Usage Guide](#usage-guide)
7. [File Descriptions](#file-descriptions)
8. [Code Explanations](#code-explanations)
9. [Example Outputs](#example-outputs)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**WhatsApp Chat Analyzer** is a comprehensive Machine Learning + NLP project that analyzes exported WhatsApp chat data and generates meaningful insights through:

- **Data Preprocessing**: Cleaning and extracting structured data from raw exports
- **Exploratory Data Analysis (EDA)**: Discovering patterns in chat behavior
- **Natural Language Processing (NLP)**: Analyzing text, sentiments, and keywords
- **Machine Learning (ML)**: Clustering, predictions, and pattern detection
- **Interactive Visualizations**: Beautiful charts and dashboards
- **Web Interface**: Modern Streamlit UI for easy exploration

## ✨ Key Features

### 1. **Data Processing** ✅
- Extracts date, time, sender, and message from raw WhatsApp exports
- Removes system notifications automatically
- Handles multi-line messages
- Supports multiple date formats

### 2. **Exploratory Data Analysis (EDA)** 📊
- **Total Statistics**: Messages count, unique users, words, media, links
- **User Analytics**: Most active users, individual profiles, engagement scores
- **Time Patterns**: Daily, weekly, monthly, and hourly activity trends
- **Peak Hours**: Identifies when chat is most active
- **Heatmaps**: Visual representation of activity (hour × day of week)

### 3. **Natural Language Processing (NLP)** 💬
- **Word Analysis**: Most common words with stopword removal
- **Emoji Analytics**: Emoji frequency and distribution
- **Sentiment Analysis**: Classifies messages as positive, negative, or neutral
- **Hashtag Extraction**: Identifies and ranks hashtags
- **Phrase Analysis**: Bigrams and trigrams (common 2-3 word combinations)

### 4. **Machine Learning Features** 🤖
- **Message Clustering**: Groups similar messages by topic using TF-IDF + K-Means
- **Keyword Extraction**: Automatically extracts important keywords
- **Behavior Prediction**: Predicts most active days and users
- **Engagement Scoring**: Scores user engagement from 0-100
- **Pattern Detection**: Identifies activity patterns for each user

### 5. **Visualizations** 📈
- Bar charts for user activity
- Line graphs for trends over time
- Heatmaps for activity patterns
- Word clouds for text frequency
- Emoji distribution charts
- Pie charts for sentiment analysis

### 6. **Interactive Web App** 🌐
- Clean, intuitive Streamlit interface
- File upload and processing
- Multiple analysis tabs
- Interactive filters and selectors
- Real-time calculations

---

## 📁 Project Structure

```
whatsapp-chat-analyzer/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── src/                           # Source code modules
│   ├── __init__.py               # Package initialization
│   ├── data_preprocessing.py      # Data loading and cleaning
│   ├── eda.py                    # Exploratory data analysis
│   ├── nlp_analysis.py           # NLP and text analysis
│   ├── ml_features.py            # ML models and predictions
│   ├── visualization.py          # Charting and plots
│   └── utils.py                  # Utility functions
│
├── data/                         # Data folder
│   └── sample_chat.txt          # Sample WhatsApp export for testing
│
└── outputs/                     # Generated outputs (created after running)
    ├── *.png                   # Saved charts
    ├── *.csv                   # Exported data
    └── report.json             # Analysis report
```

---

## 🚀 Installation & Setup

### **Step 1: Prerequisites**

Make sure you have:
- **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- **pip** package manager (comes with Python)
- A WhatsApp chat file exported from your phone

### **Step 2: Clone or Download the Project**

```bash
# Navigate to the project directory
cd C:\Users\gabba\Desktop\Destop2\ML\ project\whatsapp-chat-analyzer
```

### **Step 3: Create a Virtual Environment (Recommended)**

A virtual environment keeps your project dependencies isolated:

```bash
# Create virtual environment
python -m venv myenv

# Activate it
# On Windows:
myenv\Scripts\activate

# On Mac/Linux:
source myenv/bin/activate
```

**Why? ** Prevents package conflicts with other projects.

### **Step 4: Install Dependencies**

```bash
pip install -r requirements.txt
```

This installs all required packages:
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **matplotlib/seaborn**: Visualization
- **scikit-learn**: ML algorithms
- **nltk**: NLP tools
- **wordcloud**: Word cloud generation
- **emoji**: Emoji analysis
- **streamlit**: Web interface

**Takes ~2-3 minutes**

### **Step 5: Download NLTK Data (Required for NLP)**

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

This downloads stopword lists needed for NLP analysis.

---

## ▶️ How to Run

### **Quick Start:**

```bash
streamlit run app.py
```

The app will open automatically in your browser at: `http://localhost:8501`

---

## 📖 Usage Guide

### **Step 1: Export Your WhatsApp Chat**

1. Open WhatsApp on your phone
2. Open the chat you want to analyze (group or personal)
3. Tap **Menu** ⋮ → **More** → **Export Chat**
4. Choose **"Without Media"** (faster, no privacy issues)
5. Save the `.txt` file to your computer

### **Step 2: Upload the File**

1. Click **"Browse files"** in the left sidebar
2. Select your exported `.txt` file
3. Wait for processing (shown with spinner)

### **Step 3: Explore the Analysis**

Navigate through tabs in the left sidebar:

#### **📊 Overview Tab**
- Quick stats at a glance
- Total messages, users, words
- Most active user and day
- Date range and engagement metrics

#### **👥 User Analysis Tab**
- See top active users
- Click on a user to view their:
  - Message count and frequency
  - Peak active hours and days
  - Most used words
  - Favorite emojis

#### **📈 Activity Trends Tab**
- **Daily**: Message count per day (shows hot/cold days)
- **Weekly**: Which days are busiest
- **Monthly**: Trends over months
- **Hourly**: Peak chat hours
- **Heatmap**: Visual pattern of activity

#### **💬 NLP Analysis Tab**
- **Words**: Most common words (with/without stopwords)
- **Emojis**: Emoji frequency and favorites
- **Sentiment**: Positive/negative/neutral distribution
- **Hashtags**: Trending hashtags
- **Phrases**: Common 2 or 3 word combinations

#### **🤖 ML Insights Tab**
- **Clustering**: Groups messages by topic
- **Keywords**: Auto-extracted important terms
- **Predictions**: Predicts most active day/user
- **Engagement**: Scores user engagement (0-100)

#### **ℹ️ About Tab**
- Project information and tips

---

## 📄 File Descriptions

### **Core Application**

**`app.py`** - Main Streamlit Web Application
- Creates the interactive web interface
- Manages file uploads
- Calls all analysis functions
- Renders visualizations in tabs
- ~600 lines of code with detailed comments

### **Data Processing Modules**

**`src/data_preprocessing.py`** - Data Loading & Cleaning
```
Functions:
- load_chat_file()          → Load WhatsApp .txt file
- extract_chat_data()       → Parse messages into structured data
- is_system_notification()  → Identify & remove system messages
- clean_dataframe()         → Convert data types and add features
- get_statistics()          → Calculate basic stats
- preprocess_text()         → Clean text for NLP
- count_media_and_links()   → Count media/links in chat
```

**`src/eda.py`** - Exploratory Data Analysis
```
Functions:
- get_most_active_users()          → Top N users by message count
- get_daily_activity()             → Messages per day
- get_weekly_activity()            → Messages per day of week
- get_monthly_activity()           → Messages per month
- get_hourly_activity()            → Messages per hour
- get_user_activity_timeline()     → Activity over time for a user
- get_message_statistics()         → Stats for a specific user
- get_chat_activity_heatmap_data() → Hour × Day activity matrix
```

**`src/nlp_analysis.py`** - NLP Text Analysis
```
Functions:
- extract_words_from_messages()  → Word frequency (with stopword removal)
- extract_emojis()              → Emoji frequency
- simple_sentiment_analysis()    → Classify text sentiment
- analyze_sentiments()           → Sentiment distribution
- get_common_phrases()           → Bigrams/trigrams
- extract_hashtags()             → Find and count hashtags
- extract_mentions()             → Find @mentions
- get_message_response_time()    → Avg response time between messages
```

**`src/ml_features.py`** - Machine Learning
```
Functions:
- predict_most_active_day()      → Which day has most messages
- predict_most_active_user()     → Most frequent user
- cluster_messages()             → Group messages by topic (K-Means)
- get_cluster_summary()          → Stats for each cluster
- extract_keywords()             → TF-IDF keyword extraction
- predict_user_activity_pattern() → Behavior prediction
- get_engagement_score()         → Rate user engagement (0-100)
- detect_conversation_starters() → Who starts conversations most
```

**`src/visualization.py`** - Creating Charts
```
Functions:
- plot_top_users()               → Bar chart of active users
- plot_daily_activity()          → Line chart over time
- plot_weekly_activity()         → Bar chart by day of week
- plot_hourly_activity()         → Hour distribution
- plot_monthly_activity()        → Month By month graph
- plot_word_cloud()              → Word cloud visualization
- plot_emoji_distribution()      → Emoji bar chart
- plot_heatmap()                 → Hour × Day heatmap
- plot_sentiment_distribution()  → Pie chart of sentiments
- plot_top_words()               → Horizontal bar of words
- close_all_figures()            → Free memory from plots
```

**`src/utils.py`** - Helper Functions
```
Functions:
- ensure_directory_exists()  → Create folders
- save_dataframe_to_csv()    → Export data
- save_visualization()       → Save charts as PNG
- validate_chat_file()       → Check file validity
- create_summary_table()     → Format data nicely
- get_timestamp()            → Current time
- format_number()            → Add thousands separator
- sanitize_filename()        → Clean filenames
```

---

## 💡 Code Explanations (Beginner-Friendly)

### **Example 1: Data Preprocessing**

```python
from src.data_preprocessing import load_chat_file, extract_chat_data

# Step 1: Load the raw file
lines = load_chat_file("data/sample_chat.txt")
# Returns: ['[1/7/2023, 10:45:23 am] Alice: Hi!', ...]

# Step 2: Extract structured data
df = extract_chat_data(lines)
# Returns: DataFrame with columns [date, time, sender, message, hour, day_name, month]
```

**How it works:**
1. Reads the file line by line
2. Uses regex pattern matching to extract: date, time, sender, message
3. Skips system messages (like "user joined")
4. Creates a pandas DataFrame with columns
5. Converts dates to proper format
6. Adds useful derived columns (hour, day name, month)

### **Example 2: Finding Most Common Words**

```python
from src.nlp_analysis import extract_words_from_messages

# Get top 20 words for Alice, removing common stopwords
top_words = extract_words_from_messages(df, username="Alice", remove_stopwords=True)
# Returns: [('amazing', 45), ('project', 38), ('great', 32), ...]
```

**How it works:**
1. Filters messages from Alice only
2. Combines all her messages into one text
3. Converts to lowercase
4. Removes URLs
5. Splits into individual words
6. Removes common words like "the", "a", "is" (stopwords)
7. Counts frequency of each word
8. Returns top 50 most common

### **Example 3: Sentiment Analysis**

```python
from src.nlp_analysis import analyze_sentiments

# Analyze sentiment for all messages
sentiments = analyze_sentiments(df)
# Returns: {'positive': 342, 'negative': 12, 'neutral': 156}
```

**How it works:**
1. Goes through each message
2. Checks if it contains positive words: "good", "great", "love", "awesome", etc.
3. Checks if it contains negative words: "bad", "hate", "terrible", etc.
4. Counts which type appears more
5. Classifies as positive/negative/neutral

### **Example 4: User Clustering**

```python
from src.ml_features import cluster_messages

# Group messages into 5 topics
df_with_clusters = cluster_messages(df, n_clusters=5)
# New column 'cluster' contains group number for each message
```

**How it works:**
1. Uses TF-IDF (Term Frequency-Inverse Document Frequency)
   - Converts text to numbers
   - Important words get higher values
2. Applies K-Means clustering algorithm
   - Groups similar messages together
   - 5 clusters = 5 different topics
3. Each message gets a cluster label (0-4)

### **Example 5: Creating Visualizations**

```python
from src.visualization import plot_top_users
import matplotlib.pyplot as plt

# Create bar chart
fig = plot_top_users(top_users_df, title="Top 10 Users")
plt.show()
```

**How it works:**
1. Uses matplotlib to create figure and axes
2. Draws bars for each user
3. Adds colors, labels, and titles
4. Adds value labels on top of bars
5. Rotates x-axis labels for readability
6. Returns figure object for displaying

---

## 📊 Example Outputs

### **Overview Dashboard Output**
```
✅ Loaded 450 messages from 4 users

📊 Key Metrics:
- Total Messages: 450
- Unique Users: 4
- Total Words: 5,234
- Media Shared: 12
- Links: 8
- Date Range: 2023-01-07 to 2023-01-10

👤 Most Active User: Alice (45%)
📅 Most Active Day: Wednesday (28%)
```

### **User Analysis Output**
```
Top 5 Users:
1. Alice:   180 messages (40%)
2. Bob:     150 messages (33%)
3. Charlie: 85 messages (19%)
4. Diana:   35 messages (8%)

Alice's Profile:
- Messages: 180
- Avg Words: 8.5
- Peak Hour: 10:00
- Peak Day: Wednesday
- Engagement Score: 85/100
```

### **Activity Trends Output**
```
Daily Statistics:
- Avg Messages/Day: 112.5
- Peak Day: 156 messages
- Slowest Day: 89 messages

Weekly Pattern:
- Monday-Friday: Higher activity
- Weekend: Lower activity

Peak Hours:
- 10:00 AM: 45 messages
- 2:00 PM: 42 messages
- 5:00 PM: 38 messages
```

### **NLP Analysis Output**
```
Top 10 Words:
1. project:  56
2. great:    48
3. amazing:  45
4. work:     42
5. team:     38

Sentiment Distribution:
- Positive: 68%
- Neutral: 25%
- Negative: 7%

Top Emojis:
- 😊: 45 times
- 👍: 38 times
- 🚀: 32 times
```

### **ML Insights Output**
```
Message Clustering (5 Topics):
- Cluster 0: 180 messages (Project discussion)
- Cluster 1: 145 messages (Updates & Announcements)
- Cluster 2: 78 messages (Social/Casual)
- Cluster 3: 32 messages (Technical Issues)
- Cluster 4: 15 messages (Scheduling)

Extracted Keywords:
project, deployment, team, meeting, feature, update, fix, review, testing, production

Predictions:
- Most Active Day: Wednesday (confidence: 92%)
- Most Active User: Alice (confidence: 88%)
```

---

## 🔧 Troubleshooting

### **Issue 1: "ModuleNotFoundError: No module named 'streamlit'"**
```bash
# Solution: Install dependencies again
pip install -r requirements.txt
```

### **Issue 2: "UnicodeDecodeError" when uploading file**
```
Problem: File not in UTF-8 encoding
Solution:
1. Open the chat file with Notepad++
2. Encoding → Encode in UTF-8
3. Save and try again
```

### **Issue 3: "No emojis found" or "No words extracted"**
```
This might mean:
- Chat file is too small (< 50 messages)
- Chat only contains media messages
- File format is incorrect
Try with the sample_chat.txt file to test
```

### **Issue 4: Slow processing for large files**
```
For chats with 100k+ messages:
- Processing may take 1-5 minutes
- This is normal - be patient!
- Larger files = more accurate analysis
```

### **Issue 5: "Port 8501 is already in use"**
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### **Issue 6: Charts not displaying**
```bash
# Try updating matplotlib
pip install --upgrade matplotlib
```

---

## 🎓 Learning Path

### **Beginner Topics**
1. Understand WhatsApp export format
2. Learn pandas DataFrame basics
3. Study basic statistics (mean, median, mode)
4. Learn about plotting with matplotlib

### **Intermediate Topics**
1. Regular expressions (regex) for text parsing
2. NLP concepts (tokenization, stopwords)
3. Sentiment analysis basics
4. Basic machine learning (clustering)

### **Advanced Topics**
1. TF-IDF algorithm
2. K-Means clustering
3. Advanced NLP with transformers
4. Time series analysis

---

## 📚 Dependencies Explained

| Package | Purpose | Version |
|---------|---------|---------|
| pandas | Data manipulation | 1.3.0+ |
| numpy | Numerical computing | 1.21.0+ |
| matplotlib | Basic plotting | 3.4.0+ |
| seaborn | Statistical visualization | 0.11.0+ |
| scikit-learn | ML algorithms | 0.24.0+ |
| nltk | NLP tools | 3.6.0+ |
| wordcloud | Word cloud generation | 1.8.0+ |
| emoji | Emoji handling | 1.6.0+ |
| streamlit | Web interface | 1.28.0+ |

---

## 💾 Exporting Results

All results are saved in the `outputs/` folder:

```
outputs/
├── top_users.png                    # Bar chart
├── daily_activity.png               # Line chart
├── word_frequency.png               # Word chart
├── emoji_distribution.png           # Emoji chart
├── sentiment_pie.png                # Pie chart
├── heatmap.png                      # Activity heatmap
├── analysis_report.csv              # Exported data
└── analysis_report.json             # Full report
```

---

## 🔐 Privacy & Security

✅ **Safe to Use:**
- All processing happens on your computer
- No data is sent to external servers
- No internet required after installation
- Chat file never uploaded anywhere

---

## 🚀 Future Enhancements

Possible improvements:
- [ ] Real-time chat monitoring
- [ ] Advanced NLP with transformers
- [ ] Multi-group comparison
- [ ] Predictive analytics
- [ ] Export to PDF reports
- [ ] Dark mode UI
- [ ] Voice message transcription

---

## 📞 Support & Help

If you encounter issues:
1. Check the **Troubleshooting** section
2. Review the requirements are installed
3. Try with the sample_chat.txt file
4. Check your Python version (should be 3.8+)

For any queries, feedback, or support, feel free to contact:  
📧 shilpashukla651@gmail.com

---

## 📄 License

This project is open-source and free to use.

---

## 🎉 Conclusion

You now have a complete WhatsApp Chat Analyzer! Use it to:
- Understand group dynamics
- Track communication patterns
- Identify key topics
- Analyze team engagement
- Generate insights from your chats

**Happy analyzing!** 🚀

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Author**: Your Name
