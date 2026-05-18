"""
WhatsApp Chat Analyzer - Main Application
===========================================
A comprehensive tool to analyze WhatsApp chat exports with EDA, NLP, and ML features.

To run this app:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time
import sys
import gc
import nltk

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# =================== OPTIMIZATION: Download NLTK Data ===================
@st.cache_resource
def download_nltk_data():
    """Download NLTK data once and cache it for future use"""
    try:
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
    except Exception as e:
        st.warning(f"NLTK     warning: {e}")

# Download NLTK data on app start
download_nltk_data()

from data_preprocessing import load_chat_file, extract_chat_data, get_statistics, count_media_and_links
from eda import (
    get_most_active_users, get_daily_activity, get_weekly_activity,
    get_monthly_activity, get_hourly_activity, get_message_statistics,
    get_chat_activity_heatmap_data
)
from nlp_analysis import (
    extract_words_from_messages, extract_emojis, analyze_sentiments,
    get_common_phrases, extract_hashtags
)
from ml_features import (
    predict_most_active_day, predict_most_active_user, cluster_messages,
    extract_keywords, predict_user_activity_pattern, get_engagement_score
)
from visualization import (
    plot_top_users, plot_daily_activity, plot_weekly_activity,
    plot_hourly_activity, plot_monthly_activity, plot_word_cloud,
    plot_emoji_distribution, plot_heatmap, plot_sentiment_distribution,
    plot_top_words, close_all_figures
)
from utils import (
    validate_chat_file, create_summary_table, get_timestamp,
    estimate_processing_time, format_duration
)
from voice_commands import capture_voice_command, match_voice_command, speak_text


# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    h1 {
        color: #075e54;
        text-align: center;
    }
    h2 {
        color: #075e54;
        border-bottom: 2px solid #25d366;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None
if 'raw_stats' not in st.session_state:
    st.session_state.raw_stats = None
if 'voice_command_text' not in st.session_state:
    st.session_state.voice_command_text = ''
if 'voice_action' not in st.session_state:
    st.session_state.voice_action = None
if 'voice_error' not in st.session_state:
    st.session_state.voice_error = None


def render_voice_command_result(action, command_text, df):
    st.markdown("---")
    st.markdown("### 🎙️ Voice Command Result")
    st.write(f"**Recognized:** {command_text}")
    st.write(f"**Action:** {action.replace('_', ' ').title()}")

    if action == 'sentiment':
        sentiment = analyze_sentiments(df)
        fig = plot_sentiment_distribution(sentiment)
        st.pyplot(fig)
        close_all_figures()

        total = sum(sentiment.values())
        if total > 0:
            st.metric("😊 Positive", f"{sentiment['positive']} ({sentiment['positive']/total*100:.1f}%)")
            st.metric("😐 Neutral", f"{sentiment['neutral']} ({sentiment['neutral']/total*100:.1f}%)")
            st.metric("😞 Negative", f"{sentiment['negative']} ({sentiment['negative']/total*100:.1f}%)")

    elif action == 'emoji':
        emojis = extract_emojis(df)
        if emojis:
            fig = plot_emoji_distribution(emojis)
            st.pyplot(fig)
            close_all_figures()
            with st.expander("📋 Emoji Counts"):
                st.dataframe(pd.DataFrame(emojis, columns=['Emoji', 'Count']), use_container_width=True)
        else:
            st.info("No emojis found in this chat.")

    elif action == 'most_active_user':
        user_stats = predict_most_active_user(df)
        st.metric("🏆 Most Active User", user_stats['user'])
        st.metric("💬 Messages", f"{user_stats['messages']} ({user_stats['percentage']}%)")
        top_users_df = get_most_active_users(df, top_n=5)
        fig = plot_top_users(top_users_df)
        st.pyplot(fig)
        close_all_figures()

    elif action == 'heatmap':
        heatmap_data = get_chat_activity_heatmap_data(df)
        fig = plot_heatmap(heatmap_data)
        st.pyplot(fig)
        close_all_figures()

    elif action == 'wordcloud':
        top_words = extract_words_from_messages(df)
        fig = plot_word_cloud(top_words)
        st.pyplot(fig)
        close_all_figures()

    else:
        st.warning("Voice command recognized, but this action is not supported yet.")


def display_voice_command_status():
    """Show the current voice command text and any recognition errors."""
    if st.session_state.voice_error or st.session_state.voice_command_text:
        with st.expander("🎤 Voice command status", expanded=True):
            if st.session_state.voice_command_text:
                st.write(f"**Recognized text:** {st.session_state.voice_command_text}")
            if st.session_state.voice_action:
                st.write(f"**Mapped action:** {st.session_state.voice_action.replace('_', ' ').title()}")
            if st.session_state.voice_error:
                st.error(st.session_state.voice_error)


# =================== OPTIMIZATION: Caching Functions ===================
@st.cache_data(ttl=3600)
def process_chat_file(file):
    """
    Cache file processing for 1 hour.
    Same file = instant results!
    """
    try:
        # Validate file
        with st.spinner("📋 Validating file..."):
            temp_path = "temp_chat.txt"
            with open(temp_path, 'wb') as f:
                f.write(file.getbuffer())
        
        validation = validate_chat_file(temp_path)
        
        if not validation['is_valid']:
            st.error(f"❌ File validation failed: {', '.join(validation['errors'])}")
            return None
        
        # Load and process
        with st.spinner("⚙️ Processing chat data..."):
            lines = load_chat_file(temp_path)
            df = extract_chat_data(lines)
        
        if df.empty:
            st.error("❌ Could not extract any messages from the file.")
            return None
        
        stats = get_statistics(df)
        stats.update(count_media_and_links(df))
        
        return df, stats, validation
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        return None


# ========================= SIDEBAR =========================
st.sidebar.title("📱 WhatsApp Chat Analyzer")
st.sidebar.markdown("---")

# File upload
uploaded_file = st.sidebar.file_uploader(
    "Upload your WhatsApp chat (.txt)",
    type=['txt'],
    help="Export your WhatsApp chat without media (Settings → Chat → Export Chat)"
)

# Navigation
page = st.sidebar.radio(
    "Choose Analysis",
    [
        "📊 Overview",
        "👥 User Analysis",
        "📈 Activity Trends",
        "💬 NLP Analysis",
        "🤖 ML Insights",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**💡 Tips:**")
st.sidebar.markdown("""
- Make sure your chat file is in **UTF-8** encoding
- Longer chats = more insights!
- Try different filters for detailed analysis
""")

st.sidebar.markdown("---")
st.sidebar.header("🎙️ Voice Command")
st.sidebar.write(
    "Click the button below and speak a command like:\n"
    "- \"Show most active user\"\n"
    "- \"Display sentiment analysis\"\n"
    "- \"Show chat statistics\"\n"
    "- \"Generate word cloud\""
)

if st.sidebar.button("🎤 Start Voice Command"):
    if not st.session_state.data_loaded:
        st.sidebar.warning("Please upload a chat file before using voice commands.")
    else:
        try:
            with st.spinner("Listening for your voice command..."):
                command_text = capture_voice_command()

            action = match_voice_command(command_text)
            if action is None:
                st.sidebar.error(f"Could not map the spoken text: '{command_text}'")
                st.session_state.voice_action = None
                st.session_state.voice_error = f"No supported command found for '{command_text}'"
            else:
                st.session_state.voice_command_text = command_text
                st.session_state.voice_action = action
                st.session_state.voice_error = None
                st.sidebar.success(f"Command recognized: {command_text}")
                speak_text(f"Showing {action.replace('_', ' ')}")
        except Exception as e:
            st.sidebar.error(f"Voice input failed: {str(e)}")
            st.session_state.voice_action = None
            st.session_state.voice_error = str(e)






# ========================= PAGES =========================

if uploaded_file is not None:
    result = process_chat_file(uploaded_file)
    if result:
        st.session_state.df, st.session_state.raw_stats, validation = result
        st.session_state.data_loaded = True

if st.session_state.data_loaded and st.session_state.voice_action:
    render_voice_command_result(
        st.session_state.voice_action,
        st.session_state.voice_command_text,
        st.session_state.df
    )

# Show voice status on every page when available
display_voice_command_status()


# ========================= PAGE 1: OVERVIEW =========================
if page == "📊 Overview":
    st.title("📊 WhatsApp Chat Analysis Dashboard")
    
    if not st.session_state.data_loaded:
        st.warning("👆 Please upload a WhatsApp chat file to begin analysis")
        st.info("""
        **How to export WhatsApp chat:**
        1. Open the chat → Tap **Menu** ⋮
        2. Select **More** → **Export Chat**
        3. Choose **Without Media**
        4. Save and upload the .txt file here
        """)
    else:
        df = st.session_state.df
        stats = st.session_state.raw_stats
        
        st.success(f"✅ Loaded {len(df)} messages from {stats['unique_users']} users")
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("📨 Total Messages", f"{stats['total_messages']:,}")
        with col2:
            st.metric("👥 Users", f"{stats['unique_users']}")
        with col3:
            st.metric("📝 Total Words", f"{stats['total_words']:,}")
        with col4:
            st.metric("📸 Media Files", f"{stats['media_count']}")
        with col5:
            st.metric("🔗 Links", f"{stats['links_count']}")
        
        st.markdown("---")
        
        # Date range
        col1, col2 = st.columns(2)
        with col1:
            st.text_area("📅 Date Range", stats['date_range'], disabled=True)
        with col2:
            avg_words = stats['total_words'] / stats['total_messages']
            st.text_area("📊 Avg Words/Message", f"{avg_words:.1f}", disabled=True)
        
        st.markdown("---")
        
        # Most active user
        st.subheader("👤 Most Active User")
        top_users = get_most_active_users(df, top_n=1)
        user_stats = predict_most_active_user(df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏆 User", user_stats['user'])
        with col2:
            st.metric("💬 Messages", f"{user_stats['messages']} ({user_stats['percentage']}%)")
        with col3:
            st.metric("📌 Days Active", user_stats['days_active'])
        
        st.markdown("---")
        
        # Most active day
        st.subheader("📅 Peak Activity")
        peak_info = predict_most_active_day(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🔥 Most Active Day", peak_info['day'])
        with col2:
            st.metric("📊 Percentage", f"{peak_info['percentage']}%")


# ========================= PAGE 2: USER ANALYSIS =========================
elif page == "👥 User Analysis":
    st.title("👥 User Activity Analysis")
    
    if not st.session_state.data_loaded:
        st.warning("👆 Please upload a chat file first")
    else:
        df = st.session_state.df
        
        # Top N users selector
        col1, col2 = st.columns(2)
        with col1:
            top_n = st.slider("Show top N users", 5, 20, 10)
        
        users = df['sender'].unique()
        with col2:
            selected_user = st.selectbox("Analyze specific user", ["All Users"] + list(users))
        
        st.markdown("---")
        
        # Top users chart
        st.subheader("📊 Top Active Users")
        top_users_df = get_most_active_users(df, top_n=top_n)
        fig = plot_top_users(top_users_df)
        st.pyplot(fig)
        close_all_figures()
        gc.collect()  # Free memory
        
        st.markdown("---")
        
        # Single user analysis
        if selected_user != "All Users":
            st.subheader(f"📈 User Profile: {selected_user}")
            
            user_stats = get_message_statistics(df, selected_user)
            engagement = get_engagement_score(df, selected_user)
            activity_pattern = predict_user_activity_pattern(df, selected_user)
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💬 Messages", user_stats['total_messages'])
            with col2:
                st.metric("🔤 Avg Words", f"{user_stats['avg_words_per_message']:.1f}")
            with col3:
                st.metric("⏰ Peak Hour", f"{user_stats['most_active_hour']:02d}:00")
            with col4:
                st.metric("⚡ Engagement Score", f"{engagement:.1f}/100")
            
            st.markdown("---")
            
            # Activity pattern
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**🌟 Peak Days:** {', '.join(activity_pattern['peak_days'])}")
            with col2:
                st.write(f"**🕐 Peak Hours:** {', '.join([f'{h:02d}:00' for h in activity_pattern['peak_hours']])}")
            
            st.markdown("---")
            
            # User's top words
            st.subheader(f"💬 {selected_user}'s Most Used Words")
            top_words = extract_words_from_messages(df, selected_user)
            fig = plot_top_words(top_words[:15])
            st.pyplot(fig)
            close_all_figures()
            
            st.markdown("---")
            
            # User's top emojis
            st.subheader(f"😊 {selected_user}'s Favorite Emojis")
            emojis = extract_emojis(df, selected_user)
            if emojis:
                fig = plot_emoji_distribution(emojis)
                st.pyplot(fig)
                close_all_figures()
            else:
                st.info("No emojis used by this user")


# ========================= PAGE 3: ACTIVITY TRENDS =========================
elif page == "📈 Activity Trends":
    st.title("📈 Chat Activity Trends")
    
    if not st.session_state.data_loaded:
        st.warning("👆 Please upload a chat file first")
    else:
        df = st.session_state.df
        
        # Tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📅 Daily", "📊 Weekly", "🗓️ Monthly", "⏰ Hourly", "🔥 Heatmap"]
        )
        
        with tab1:
            st.subheader("Daily Activity Timeline")
            daily = get_daily_activity(df)
            fig = plot_daily_activity(daily)
            st.pyplot(fig)
            close_all_figures()
            
            # Stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Avg Messages/Day", f"{daily['Messages'].mean():.0f}")
            with col2:
                st.metric("📈 Peak Day", f"{daily['Messages'].max()}")
            with col3:
                st.metric("📉 Slowest Day", f"{daily['Messages'].min()}")
        
        with tab2:
            st.subheader("Weekly Activity Pattern")
            weekly = get_weekly_activity(df)
            fig = plot_weekly_activity(weekly)
            st.pyplot(fig)
            close_all_figures()
            
            # Show data
            st.dataframe(weekly, use_container_width=True)
        
        with tab3:
            st.subheader("Monthly Activity Trend")
            monthly = get_monthly_activity(df)
            fig = plot_monthly_activity(monthly)
            st.pyplot(fig)
            close_all_figures()
        
        with tab4:
            st.subheader("Peak Chat Hours")
            hourly = get_hourly_activity(df)
            fig = plot_hourly_activity(hourly)
            st.pyplot(fig)
            close_all_figures()
            
            # Show peak hours
            peak_hours = hourly.nlargest(3, 'Messages')
            st.write("**🔥 Top 3 Peak Hours:**")
            for idx, row in peak_hours.iterrows():
                st.write(f"• {int(row['Hour']):02d}:00 - {int(row['Messages'])} messages")
        
        with tab5:
            st.subheader("Activity Heatmap (Hour × Day)")
            heatmap_data = get_chat_activity_heatmap_data(df)
            fig = plot_heatmap(heatmap_data)
            st.pyplot(fig)
            close_all_figures()
            st.info("🔍 Red indicates higher message volume")


# ========================= PAGE 4: NLP ANALYSIS =========================
elif page == "💬 NLP Analysis":
    st.title("💬 Natural Language Processing Analysis")
    
    if not st.session_state.data_loaded:
        st.warning("👆 Please upload a chat file first")
    else:
        df = st.session_state.df
        
        # User selector
        users = ["All Users"] + list(df['sender'].unique())
        selected_user = st.selectbox("Analyze", users)
        
        st.markdown("---")
        
        # Tabs for different NLP analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📝 Words", "😊 Emojis", "💭 Sentiment", "🏷️ Hashtags", "🍃 Phrases"]
        )
        
        with tab1:
            st.subheader("Most Common Words")
            stop_words = st.checkbox("Remove stopwords", value=True)
            
            top_words = extract_words_from_messages(
                df, 
                selected_user if selected_user != "All Users" else None,
                remove_stopwords=stop_words
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Word Cloud**")
                fig = plot_word_cloud(top_words)
                st.pyplot(fig)
                close_all_figures()
            
            with col2:
                st.write("**Word Frequency (Top 15)**")
                fig = plot_top_words(top_words[:15])
                st.pyplot(fig)
                close_all_figures()
            
            # Show as table
            with st.expander("📋 View as Table"):
                words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
                st.dataframe(words_df, use_container_width=True)
        
        with tab2:
            st.subheader("Emoji Usage")
            emojis = extract_emojis(
                df,
                selected_user if selected_user != "All Users" else None
            )
            
            if emojis:
                fig = plot_emoji_distribution(emojis)
                st.pyplot(fig)
                close_all_figures()
                
                # Show as table
                with st.expander("📋 View as Table"):
                    emoji_df = pd.DataFrame(emojis, columns=['Emoji', 'Count'])
                    st.dataframe(emoji_df, use_container_width=True)
            else:
                st.info("No emojis found")
        
        with tab3:
            st.subheader("Sentiment Analysis")
            sentiment = analyze_sentiments(
                df,
                selected_user if selected_user != "All Users" else None
            )
            
            fig = plot_sentiment_distribution(sentiment)
            st.pyplot(fig)
            close_all_figures()
            
            # Stats
            total_sentiment = sum(sentiment.values())
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if total_sentiment > 0:
                    st.metric("😊 Positive", f"{sentiment['positive']} ({sentiment['positive']/total_sentiment*100:.1f}%)")
                else:
                    st.metric("😊 Positive", "0")
            
            with col2:
                if total_sentiment > 0:
                    st.metric("😐 Neutral", f"{sentiment['neutral']} ({sentiment['neutral']/total_sentiment*100:.1f}%)")
                else:
                    st.metric("😐 Neutral", "0")
            
            with col3:
                if total_sentiment > 0:
                    st.metric("😞 Negative", f"{sentiment['negative']} ({sentiment['negative']/total_sentiment*100:.1f}%)")
                else:
                    st.metric("😞 Negative", "0")
        
        with tab4:
            st.subheader("Hashtags Found")
            hashtags = extract_hashtags(
                df,
                selected_user if selected_user != "All Users" else None
            )
            
            if hashtags:
                hashtags_df = pd.DataFrame(hashtags, columns=['Hashtag', 'Count'])
                st.dataframe(hashtags_df, use_container_width=True)
                
                # Create chart
                fig, ax = plt.subplots(figsize=(10, 5))
                tags, counts = zip(*hashtags)
                ax.barh(tags, counts, color='#25d366')
                ax.set_xlabel('Frequency')
                ax.set_title('Hashtag Frequency')
                st.pyplot(fig)
                close_all_figures()
            else:
                st.info("No hashtags found")
        
        with tab5:
            st.subheader("Common Phrases")
            
            gram_type = st.radio("Select phrase type:", ["Bigrams (2 words)", "Trigrams (3 words)"])
            n_grams = 2 if "Bigrams" in gram_type else 3
            
            phrases = get_common_phrases(
                df,
                n_grams=n_grams,
                top_n=15,
                username=selected_user if selected_user != "All Users" else None
            )
            
            if phrases:
                phrases_df = pd.DataFrame(phrases, columns=['Phrase', 'Frequency'])
                st.dataframe(phrases_df, use_container_width=True)
            else:
                st.info("No phrases found")


# ========================= PAGE 5: ML INSIGHTS =========================
elif page == "🤖 ML Insights":
    st.title("🤖 Machine Learning & Advanced Analytics")
    
    if not st.session_state.data_loaded:
        st.warning("👆 Please upload a chat file first")
    else:
        df = st.session_state.df
        
        tab1, tab2, tab3, tab4 = st.tabs(
            ["🔍 Clustering", "🔑 Keywords", "📊 Predictions", "⚡ Engagement"]
        )
        
        with tab1:
            st.subheader("Message Clustering (Topic Analysis)")
            st.info("Groups similar messages together to identify main topics")
            
            n_clusters = st.slider("Number of clusters", 3, 10, 5)
            
            with st.spinner("Clustering messages..."):
                df_clustered = cluster_messages(df, n_clusters=n_clusters)
                cluster_summary = pd.DataFrame(
                    df_clustered['cluster'].value_counts().sort_index()
                ).reset_index()
                cluster_summary.columns = ['Cluster', 'Messages']
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.metric("Total Clusters", len(cluster_summary))
            with col2:
                st.metric("Avg Messages/Cluster", f"{cluster_summary['Messages'].mean():.0f}")
            
            st.dataframe(cluster_summary, use_container_width=True)
        
        with tab2:
            st.subheader("Key Topics/Keywords")
            
            users = ["All Users"] + list(df['sender'].unique())
            selected_user = st.selectbox("Extract keywords for", users)
            
            with st.spinner("Extracting keywords..."):
                keywords = extract_keywords(
                    df,
                    top_n=20,
                    username=selected_user if selected_user != "All Users" else None
                )
            
            if keywords:
                col1, col2, col3 = st.columns(3)
                for idx, kw in enumerate(keywords):
                    if idx < 7:
                        with col1:
                            st.write(f"🔑 {kw}")
                    elif idx < 14:
                        with col2:
                            st.write(f"🔑 {kw}")
                    else:
                        with col3:
                            st.write(f"🔑 {kw}")
            else:
                st.info("No keywords found")
        
        with tab3:
            st.subheader("Activity Predictions")
            
            # Most active day prediction
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📅 Most Active Day Prediction**")
                peak_day = predict_most_active_day(df)
                st.write(f"🔥 {peak_day['day']}")
                st.write(f"Confidence: {peak_day['percentage']}%")
            
            with col2:
                st.write("**👤 Most Active User Prediction**")
                peak_user = predict_most_active_user(df)
                st.write(f"🏆 {peak_user['user']}")
                st.write(f"Percentage: {peak_user['percentage']}%")
            
            st.markdown("---")
            
            # User behavior prediction
            users = df['sender'].unique()
            selected_user = st.selectbox("Predict behavior for", users, key="behavior_user")
            
            behavior = predict_user_activity_pattern(df, selected_user)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Peak Hours:** {', '.join([f'{h:02d}:00' for h in behavior['peak_hours']])}")
                st.write(f"**Peak Days:** {', '.join(behavior['peak_days'])}")
            
            with col2:
                st.write(f"**Avg Daily Messages:** {behavior['avg_messages_per_day']}")
                st.write(f"**Consistency Score:** {behavior['consistency_score']:.1f}%")
        
        with tab4:
            st.subheader("User Engagement Analytics")
            
            users_list = df['sender'].unique()
            
            engagement_data = []
            for user in users_list:
                score = get_engagement_score(df, user)
                engagement_data.append({'User': user, 'Engagement Score': score})
            
            engagement_df = pd.DataFrame(engagement_data).sort_values('Engagement Score', ascending=False)
            
            st.dataframe(engagement_df, use_container_width=True)
            
            # Visualization
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.barh(engagement_df['User'], engagement_df['Engagement Score'], color='#25d366')
            ax.set_xlabel('Engagement Score (0-100)')
            ax.set_title('User Engagement Comparison')
            st.pyplot(fig)
            close_all_figures()


# ========================= PAGE 6: ABOUT =========================
elif page == "ℹ️ About":
    st.title("ℹ️ About WhatsApp Chat Analyzer")
    
    st.markdown("""
    ## 📱 WhatsApp Chat Analyzer
    
    A comprehensive tool for analyzing WhatsApp group/personal chats with powerful visualizations and insights.
    
    ### ✨ Features
    
    #### 📊 Overview Dashboard
    - Total messages, users, words, media items
    - Date range and engagement metrics
    - Key statistics at a glance
    
    #### 👥 User Analysis
    - Top active users
    - Individual user profiles
    - Engagement scores
    - Word usage patterns
    
    #### 📈 Activity Trends
    - Daily, weekly, monthly patterns
    - Peak chat hours
    - Interactive heatmaps
    - Trend analysis
    
    #### 💬 NLP Analysis
    - Most common words (with stopword removal)
    - Emoji frequency analysis
    - Sentiment analysis (positive/negative/neutral)
    - Hashtag extraction
    - Common phrases and bigrams
    
    #### 🤖 ML Insights
    - Message clustering (topic detection)
    - Automatic keyword extraction
    - Activity predictions
    - User behavior patterns
    - Engagement scoring
    
    ### 🛠️ Technologies Used
    
    - **Python**: Core language
    - **Pandas & NumPy**: Data processing
    - **Streamlit**: Web interface
    - **Matplotlib & Seaborn**: Charting
    - **Scikit-learn**: ML algorithms
    - **NLTK**: NLP analysis
    - **WordCloud**: Text visualization
    - **Emoji**: Emoji analysis
    
    ### 📥 How to Use
    
    1. **Export WhatsApp Chat**
       - Open the chat
       - Tap Menu ⋮ → More → Export Chat
       - Choose "Without Media"
       - Save the .txt file
    
    2. **Upload File**
       - Click on the upload area in the sidebar
       - Select your exported chat file
    
    3. **Explore Insights**
       - Navigate through different tabs
       - Use filters to customize analysis
       - Download insights if needed
    
    ### ⚙️ Settings & Tips
    
    - **File Size**: Works best with chats < 10MB
    - **Date Format**: Supports multiple WhatsApp date formats
    - **Encoding**: Ensure file is in UTF-8 encoding
    - **Privacy**: All processing happens locally
    
    ### 🚀 Performance Notes
    
    - Large chats (100k+ messages) may take a few seconds to process
    - Clustering and NLP analysis handle large datasets efficiently
    - Memory usage increases with chat size
    
    ### 📝 About the Developer
    
    This tool was built with ❤️ for WhatsApp chat enthusiasts, researchers, and data analysts.
    
    ### 📞 Support
    
    For issues or feature requests, please refer to the documentation or contact support.
    
    ---
    
    **Version**: 1.0.0  
    **Last Updated**: 2026  
    **License**: Indian_Web
    """)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px;">
    <p>💡 Optimized for cloud deployment | Auto-cached for speed</p>
</div>
""", unsafe_allow_html=True)

# ============= OPTIMIZATION: Cleanup on Session End =============
# This runs when user closes the app or refreshes
def cleanup():
    gc.collect()

import atexit
atexit.register(cleanup)
