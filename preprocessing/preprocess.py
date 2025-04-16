import pandas as pd
import os
import re
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download VADER if not already
nltk.download('vader_lexicon')

# 📁 Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'reddit_posts.csv')
PROCESSED_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'reddit_sentiment.csv')

# 🧼 Cleaning helper
def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    text = text.lower()
    return text.strip()

# 🔄 Load and process
print("🔍 Loading raw data...")
df = pd.read_csv(RAW_PATH)
df['clean_text'] = df['title'].apply(clean_text)

# 🔎 Apply VADER
print("🧠 Running sentiment analysis...")
sia = SentimentIntensityAnalyzer()
df['sentiment_score'] = df['clean_text'].apply(lambda x: sia.polarity_scores(x)['compound'])

def get_sentiment(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

df['sentiment'] = df['sentiment_score'].apply(get_sentiment)

# 💾 Save
os.makedirs(os.path.join(BASE_DIR, 'data', 'processed'), exist_ok=True)
df.to_csv(PROCESSED_PATH, index=False)
print(f"✅ Processed data saved to: {PROCESSED_PATH}")
