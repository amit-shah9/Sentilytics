import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 📁 Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'reddit_sentiment.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
os.makedirs(MODEL_DIR, exist_ok=True)

# 🔄 Load data
print("📥 Loading processed data...")
df = pd.read_csv(DATA_PATH)

# 🎯 Features and labels
X = df['clean_text']
y = df['sentiment']

# 📊 TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=1000)
X_vec = vectorizer.fit_transform(X)

# 🔀 Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# 🧠 Train model
print("🤖 Training classifier...")
model = LogisticRegression()
model.fit(X_train, y_train)

# 📈 Evaluate
y_pred = model.predict(X_test)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# 💾 Save model and vectorizer
joblib.dump(model, os.path.join(MODEL_DIR, 'sentiment_model.pkl'))
joblib.dump(vectorizer, os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'))
print("✅ Model and vectorizer saved.")
