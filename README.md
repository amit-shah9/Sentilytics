# 🧠 Sentilytics – Reddit Sentiment Analyzer

Analyze public sentiment around any topic on Reddit in real-time using NLP and data visualization.  

**Live App:** [sentilytics.streamlit.app](https://sentilytics-kbp3dwnjmasdbywax4kmnk.streamlit.app)

![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Containerized-Docker-2496ED?logo=docker&logoColor=white)

---

## ✨ Features

- **Sentiment Analysis** of Reddit posts using VADER NLP
- **Trendiness Score** – how active the topic is right now
- **Top Positive & Negative Posts**
- **Keyword Co-occurrence** insights
- Sleek **Streamlit UI** with rich visualizations
- Optional **Dockerized setup**
- Simple **FastAPI backend**

---

## 🚀 How It Works

- **User inputs a keyword or topic**
- App fetches latest Reddit posts containing that keyword
- Sentiment is analyzed using VADER from NLTK
- Trendiness is calculated based on post timestamps
- Outputs:
  - Sentiment breakdown
  - Most positive/negative posts
  - Co-occurring keywords
  - Trend signal

---

## 📸 Preview

![Preview](https://github.com/user-attachments/assets/5a71e876-d49b-4ba9-b320-cdd8e35b87f6)

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **NLP:** NLTK (VADER)
- **Reddit API:** PRAW
- **Container:** Docker
- **Data viz:** Altair, Pandas

---

### 👨‍💻 Author

**Amit Shah**  
Data Science & MLOps Enthusiast  
🔗 [Connect on LinkedIn](https://www.linkedin.com/in/amit-shah-296099237/)  
💼 Open to ML Engineering / AI Product Roles

---

## ⚙️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/amit-shah9/Sentilytics.git
cd Sentilytics

# 2. Create a virtual environment
python -m venv venv
source venv/Scripts/activate  # or source venv/bin/activate on Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create config.py with your Reddit API credentials
# config.py
REDDIT_CLIENT_ID = "your_id"
REDDIT_CLIENT_SECRET = "your_secret"
REDDIT_USER_AGENT = "sentilytics-app"

# 5. Run the FastAPI backend
uvicorn api.sentiment_api:app --reload

# 6. In a new terminal, run the Streamlit dashboard
streamlit run dashboard/app.py
