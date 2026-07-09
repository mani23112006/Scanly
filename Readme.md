# SCANLY

An AI-powered scam detection system that analyzes text messages and URLs using a hybrid approach combining **Machine Learning (NLP)**, **rule-based detection**, and **URL phishing analysis** to provide real-time, explainable scam risk scores.

> **Project Status:** 🚧 In Development (Day 7 of 20)

---

# Features

- AI-powered scam detection using Machine Learning (TF-IDF + Naive Bayes)
- Rule-based scam keyword detection
- URL phishing detection using heuristic analysis
- Hybrid scam risk scoring
- Explainable predictions with matched keywords
- REST API built with FastAPI
- Input validation using Pydantic
- MongoDB integration
- Interactive API documentation (Swagger UI)
- Model persistence using Joblib
- React frontend *(Under Development)*

---

# Tech Stack

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- MongoDB
- PyMongo
- Motor

## Machine Learning

- Scikit-learn
- Pandas
- NumPy
- Joblib

## Frontend

- React
- Vite
- JavaScript

## Database

- MongoDB Community Server

---

# Project Structure

```text
scanly/
│
├── docs/
│   ├── DAY-01.md
│   ├── DAY-02.md
│   ├── DAY-03.md
│   ├── DAY-04.md
│   ├── DAY-05.md
│   ├── DAY-06.md
│   └── DAY-07.md
│
├── scanly-backend/
│   ├── ml/
│   │   ├── dataset.csv
│   │   ├── preprocess.py
│   │   ├── train.py
│   │   ├── model.pkl
│   │   └── vectorizer.pkl
│   │
│   ├── main.py
│   ├── models.py
│   ├── rules.py
│   ├── url_checker.py
│   ├── db.py
│   ├── requirements.txt
│   ├── .gitignore
│   └── .env
│
└── scanly-frontend/
    ├── src/
    ├── package.json
    └── vite.config.js
```

---

# Current API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Backend status |
| GET | `/health` | Health check |
| POST | `/scan` | Analyze text and URLs for scam indicators |

---

# Example Request

```json
{
  "text": "You won a free prize! Claim your OTP now urgently."
}
```

---

# Example Response

```json
{
  "status": "success",
  "input_text": "You won a free prize! Claim your OTP now urgently.",
  "final_score": 67,
  "category": "Suspicious",
  "ml_score": 99,
  "rule_score": 60,
  "url_score": 0,
  "matched_keywords": [
    "prize",
    "otp",
    "urgent"
  ],
  "explanation": "Some suspicious patterns found. Be cautious. | Keywords: prize, otp, urgent | ML model confidence: 99% scam probability"
}
```

---

# Detection Pipeline

```text
User Input
      │
      ▼
FastAPI API
      │
      ▼
Rule-Based Detection
      │
      ▼
URL Phishing Analysis
      │
      ▼
Machine Learning (TF-IDF + Naive Bayes)
      │
      ▼
Hybrid Risk Scoring
      │
      ▼
Risk Category
      │
      ▼
JSON Response
```

---

# Machine Learning Pipeline

```text
dataset.csv
      │
      ▼
preprocess.py
(Clean Text)
      │
      ▼
TF-IDF Vectorizer
(Text → Numerical Features)
      │
      ▼
Multinomial Naive Bayes
      │
      ▼
Evaluate Model
      │
      ▼
Save
├── model.pkl
└── vectorizer.pkl
      │
      ▼
Predict Scam Probability
```

---

# Progress

| Day | Status | Description |
|-----|:------:|-------------|
| Day 1 | ✅ | Project setup (React + FastAPI) |
| Day 2 | ✅ | MongoDB local setup |
| Day 3 | ✅ | REST API & Pydantic validation |
| Day 4 | ✅ | Rule-based scam detection engine |
| Day 5 | ✅ | URL phishing detection engine |
| Day 6 | ✅ | NLP dataset preparation & preprocessing |
| Day 7 | ✅ | TF-IDF + Naive Bayes model training & backend integration |

Detailed daily documentation is available in the **docs/** directory.

---

# Roadmap

- [x] Backend setup
- [x] MongoDB integration
- [x] REST API
- [x] Rule-based detection
- [x] URL phishing detection
- [x] NLP dataset preprocessing
- [x] Machine Learning spam detection
- [x] Model persistence
- [ ] Save scan history
- [ ] Feedback-based continuous learning
- [ ] React dashboard
- [ ] User authentication
- [ ] Deployment (Render + Vercel)

---

# Running the Project

## Backend

```bash
cd scanly-backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Backend

```
http://localhost:8000
```

Swagger UI

```
http://localhost:8000/docs
```

---

## Train the ML Model

```bash
cd scanly-backend
python ml/train.py
```

This generates:

```text
ml/
├── model.pkl
└── vectorizer.pkl
```

---

## Frontend

```bash
cd scanly-frontend
npm install
npm run dev
```

Frontend

```
http://localhost:5173
```

---

# Future Improvements

- Deep Learning (LSTM/BERT) spam detection
- Real-time URL reputation APIs
- User feedback-driven model retraining
- Dashboard with scan history & analytics
- Browser extension for phishing detection
- Email scam detection

---

# License

This project is being developed for educational, hackathon, and portfolio purposes.