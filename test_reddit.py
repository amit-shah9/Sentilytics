import os
import certifi

# ✅ Hardcode cert path explicitly
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

import praw
import requests
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

session = requests.Session()

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    requestor_kwargs={"session": session}
)

try:
    for post in reddit.subreddit("MachineLearning").hot(limit=5):
        print(post.title)
except Exception as e:
    print("❌ Reddit fetch failed:", e)
