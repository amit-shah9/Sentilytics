import os
import praw
import certifi
import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime

nltk.download("vader_lexicon")

# Reddit Auth from environment variables
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Secure session
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

def fetch_reddit_sentiment(query, limit=100):
    posts = []
    positive, negative = 0, 0

    for submission in reddit.subreddit("all").search(query, sort="new", limit=limit):
        score = sia.polarity_scores(submission.title)["compound"]
        timestamp = datetime.utcfromtimestamp(submission.created_utc).isoformat()

        if score > 0.2:
            sentiment = "positive"
            positive += 1
        elif score < -0.2:
            sentiment = "negative"
            negative += 1
        else:
            continue

        posts.append({
            "title": submission.title,
            "sentiment": sentiment,
            "score": score,
            "timestamp": timestamp,
        })

    total = positive + negative
    pos_pct = round((positive / total) * 100, 2) if total else 0.0
    neg_pct = round((negative / total) * 100, 2) if total else 0.0

    return {
        "positive_percentage": pos_pct,
        "negative_percentage": neg_pct,
        "posts": posts
    }
