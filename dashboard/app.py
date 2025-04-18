import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

# Page setup
st.set_page_config(page_title="Sentilytics", layout="wide")
st.markdown(
    """
    <style>
    .centered { display: flex; justify-content: center; text-align: center; }
    .card {
        padding: 1rem;
        border-radius: 0.75rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 5px rgba(255, 255, 255, 0.05);
    }
    .positive {
        background-color: rgba(0, 128, 0, 0.1);
        border-left: 6px solid #2ecc71;
    }
    .negative {
        background-color: rgba(255, 0, 0, 0.1);
        border-left: 6px solid #e74c3c;
    }
    .info {
        background-color: rgba(30, 144, 255, 0.1);
        border-left: 6px solid #3498db;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Inputs
st.sidebar.title("🧠 Sentilytics Settings")
query = st.sidebar.text_input("Topic / Keyword", "AI")
limit = st.sidebar.slider("Number of Posts", 10, 200, 100, 10)

st.title("🧠 Sentilytics - Reddit Sentiment Analysis")

if st.sidebar.button("🔍 Analyze"):
    with st.spinner("Analyzing Reddit posts..."):
        from api_utils import fetch_reddit_sentiment

        data = fetch_reddit_sentiment(query, limit)
        df = pd.DataFrame(data["posts"])


        # Sentiment Breakdown
        pos_pct = data["positive_percentage"]
        neg_pct = data["negative_percentage"]

        st.markdown("## 📊 Sentiment Breakdown")
        chart_data = pd.DataFrame({
            "Sentiment": ["Positive", "Negative"],
            "Percentage": [pos_pct, neg_pct]
        })
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("Percentage:Q", scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("Sentiment:N", sort="-x"),
            color=alt.Color("Sentiment", scale=alt.Scale(range=["#e74c3c", "#2ecc71"])),
            tooltip=["Sentiment", "Percentage"]
        ).properties(width=600)
        st.altair_chart(chart, use_container_width=True)

        # Trendiness Signal
        st.markdown("## 📈 Trendiness")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        time_diff = df["timestamp"].max() - df["timestamp"].min()
        total_minutes = round(time_diff.total_seconds() / 60)
        trendiness = "🔥 High activity!" if total_minutes < 60 else "📉 Slower trend"

        st.markdown(f'''
            <div class="card info">
                🕒 {limit} posts in <strong>{total_minutes} minutes</strong> → <strong>{trendiness}</strong>
            </div>
        ''', unsafe_allow_html=True)

        # Top Posts
        st.markdown("## 🏆 Top Posts")
        top_positive = df[df["sentiment"] == "positive"].sort_values("score", ascending=False).head(1)
        top_negative = df[df["sentiment"] == "negative"].sort_values("score", ascending=True).head(1)

        col1, col2 = st.columns(2)
        with col1:
            if not top_positive.empty:
                st.markdown(f"""
                <div class="card positive">
                    ✅ <strong>Most Positive Post:</strong><br><br>
                    <em>{top_positive.iloc[0]['title']}</em><br>
                    <small>Score: {top_positive.iloc[0]['score']:.2f}</small>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            if not top_negative.empty:
                st.markdown(f"""
                <div class="card negative">
                    ⚠️ <strong>Most Negative Post:</strong><br><br>
                    <em>{top_negative.iloc[0]['title']}</em><br>
                    <small>Score: {top_negative.iloc[0]['score']:.2f}</small>
                </div>
                """, unsafe_allow_html=True)

        # Keyword Co-occurrence
        st.markdown("## 🧠 Keyword Co-occurrence")
        all_words = []
        for title in df["title"]:
            words = re.findall(r"\b\w+\b", title.lower())
            words = [w for w in words if w not in stopwords.words("english") and w != query.lower()]
            all_words.extend(words)

        common_words = Counter(all_words).most_common(10)
        if common_words:
            for word, count in common_words:
                st.write(f"🔹 **{word}** — {count} times")
        else:
            st.write("No significant keywords found.")
