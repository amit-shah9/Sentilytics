import os
import certifi
import nltk
import praw
import requests
import re
from datetime import datetime
from collections import Counter

from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

# Fix SSL issues
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
session = requests.Session()
session.verify = certifi.where()

# Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    requestor_kwargs={"session": session}
)

# Sentiment analyzer
sia = SentimentIntensityAnalyzer()

def fetch_reddit_sentiment(query: str, limit: int = 100):
    posts = []
    timestamps = []
    word_list = []
    positive = 0
    negative = 0

    for submission in reddit.subreddit("all").search(query, sort="new", limit=limit):
        score = sia.polarity_scores(submission.title)["compound"]
        if score > 0.2:
            sentiment = "positive"
            positive += 1
        elif score < -0.2:
            sentiment = "negative"
            negative += 1
        else:
            continue

        created_time = datetime.utcfromtimestamp(submission.created_utc).isoformat()
        timestamps.append(created_time)

        words = re.findall(r"\b\w+\b", submission.title.lower())
        filtered = [w for w in words if w != query.lower() and len(w) > 3]
        word_list.extend(filtered)

        posts.append({
            "title": submission.title,
            "sentiment": sentiment,
            "score": score,
            "timestamp": created_time
        })

    total = positive + negative
    co_occurrence = Counter(word_list).most_common(10)

    return {
        "positive_percentage": round((positive / total) * 100, 2) if total else 0.0,
        "negative_percentage": round((negative / total) * 100, 2) if total else 0.0,
        "posts": posts,
        "timestamps": timestamps,
        "co_occurring_keywords": co_occurrence
    }
