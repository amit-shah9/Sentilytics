# api_utils.py
import requests

API_URL = "http://api:8000/analyze"  # 'api' is service name in Docker

def fetch_reddit_sentiment(query: str, limit: int = 100):
    try:
        response = requests.get(API_URL, params={"query": query, "limit": limit})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
