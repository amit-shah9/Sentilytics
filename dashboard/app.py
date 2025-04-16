import streamlit as st
import joblib
import os
import pandas as pd

# 🧠 Load model and vectorizer
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'sentiment_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'tfidf_vectorizer.pkl')

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# 🖼️ Page setup
st.set_page_config(page_title="Sentilytics", layout="centered")
st.title("🧠 Sentilytics — Reddit Post Sentiment Classifier")
st.write("Paste any Reddit post or message and this model will classify the sentiment based on recent Reddit content.")

# 📝 User input
text_input = st.text_area("✍️ Enter a Reddit post or sentence:", height=150)

if st.button("🔍 Analyze Sentiment"):
    if text_input.strip() == "":
        st.warning("Please enter some text!")
    else:
        # Preprocess and predict
        input_transformed = vectorizer.transform([text_input])
        prediction = model.predict(input_transformed)[0]

        # Display result
        st.success(f"Predicted Sentiment: **{prediction.upper()}**")

        # Optional: emoji feedback
        emoji = {"positive": "😊", "neutral": "😐", "negative": "😠"}
        st.markdown(f"### {emoji.get(prediction, '')}")
