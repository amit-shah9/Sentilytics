import praw
import pandas as pd
import os
from datetime import datetime
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

# Output path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Config
SUBREDDIT = "MachineLearning"
LIMIT = 200

# Scrape submissions
print(f"🔍 Fetching {LIMIT} posts from r/{SUBREDDIT}...")
posts = []
for submission in reddit.subreddit(SUBREDDIT).hot(limit=LIMIT):
    posts.append({
        "id": submission.id,
        "title": submission.title,
        "selftext": submission.selftext,
        "created_utc": datetime.fromtimestamp(submission.created_utc),
        "score": submission.score,
        "num_comments": submission.num_comments,
        "subreddit": submission.subreddit.display_name,
        "type": "post",
        "text": submission.title + "\n" + submission.selftext
    })

# Save to CSV
df = pd.DataFrame(posts)
output_path = os.path.join(RAW_DIR, "reddit_posts.csv")
df.to_csv(output_path, index=False)

print(f"✅ Fetched {len(df)} posts. Saved to {output_path}")
