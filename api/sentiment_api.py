import os
import certifi
import nltk
import praw
import requests
from datetime import datetime
import re
from collections import Counter

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon
nltk.download("vader_lexicon")

# Use certifi for secure HTTPS requests
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
session = requests.Session()
session.verify = certifi.where()

# Reddit API credentials from config
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    requestor_kwargs={"session": session}
)

# Initialize FastAPI and sentiment analyzer
app = FastAPI(title="Sentilytics API")
sia = SentimentIntensityAnalyzer()

# Pydantic models
class RedditPost(BaseModel):
    title: str
    sentiment: str
    score: float
    timestamp: datetime 

class SentimentSummary(BaseModel):
    positive_percentage: float
    negative_percentage: float
    posts: List[RedditPost]
    timestamps: List[str]
    co_occurring_keywords: List[tuple]

# Main API route
@app.get("/analyze", response_model=SentimentSummary)
def analyze_sentiment(query: str = Query(..., description="Search keyword")):
    posts = []
    positive = 0
    negative = 0
    timestamps = []
    word_list = []

    try:
        for submission in reddit.subreddit("all").search(query, sort="new", limit=200):
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

            # Extract co-occurring words
            words = re.findall(r"\b\w+\b", submission.title.lower())
            filtered = [w for w in words if w != query.lower() and len(w) > 3]
            word_list.extend(filtered)

            posts.append(RedditPost(
                title=submission.title,
                sentiment=sentiment,
                score=score,
                timestamp=datetime.fromtimestamp(submission.created_utc)  # Add this
            ))

        total = positive + negative
        if total == 0:
            return SentimentSummary(
                positive_percentage=0.0,
                negative_percentage=0.0,
                posts=[],
                timestamps=[],
                co_occurring_keywords=[]
            )

        co_occurrence = Counter(word_list).most_common(10)

        return SentimentSummary(
            positive_percentage=round((positive / total) * 100, 2),
            negative_percentage=round((negative / total) * 100, 2),
            posts=posts,
            timestamps=timestamps,
            co_occurring_keywords=co_occurrence
        )

    except Exception as e:
        print(f"Reddit fetch failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch or analyze Reddit posts.")
