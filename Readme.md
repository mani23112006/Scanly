# 🔍 SCANLY — AI-Powered Scam Detection System

> Paste any suspicious SMS, WhatsApp message, or URL and get an instant AI-powered risk score with a detailed explanation.

---

## ✨ Features

* 🤖 **NLP Model** — Naive Bayes + TF-IDF trained on 5500+ SMS messages (~97% accuracy)
* 📋 **Rule Engine** — 20+ weighted keyword patterns for instant scam detection
* 🔗 **URL Analyzer** — Detects IP addresses, suspicious TLDs, HTTP links, and URL shorteners
* ⚖️ **Risk Scoring** — Weighted final score: ML (50%) + Rules (30%) + URL (20%)
* 📊 **Explainable AI** — Shows exactly which keywords and URLs contributed to the final score
* 💾 **Scan History** — Stores previous scans in MongoDB
* 🔐 **Firebase Authentication** — Secure login/signup with guest access support
* 📱 **Responsive UI** — Optimized for desktop, tablet, and mobile devices
* 🚦 **Rate Limiting** — Prevents API abuse using SlowAPI

---

## 🏗️ Architecture

```text
React Frontend
        │
        │ POST /scan
        ▼
FastAPI Backend
        ├── ML Model      → TF-IDF + Naive Bayes (50%)
        ├── Rule Engine   → Keyword Analysis (30%)
        ├── URL Analyzer  → Phishing Detection (20%)
        ▼
Weighted Risk Scorer
        ▼
MongoDB Atlas
        ▼
Scan History
```

---

## 🛠️ Tech Stack

| Layer            | Technology                                    |
| ---------------- | --------------------------------------------- |
| Frontend         | React 18, Vite, Tailwind CSS, React Router    |
| Backend          | FastAPI, Python 3.11, Uvicorn                 |
| Machine Learning | scikit-learn, TF-IDF, Multinomial Naive Bayes |
| Database         | MongoDB                                       |
| Authentication   | Firebase Authentication                       |
| Rate Limiting    | SlowAPI                                       |
| Version Control  | Git & GitHub                                  |

---

## 📊 Risk Scoring

SCANLY combines three independent detection techniques to generate a final risk score.

```
Input Message
        │
        ├── ML Model
        │      ↓
        │   Scam Probability
        │
        ├── Rule Engine
        │      ↓
        │  Keyword Score
        │
        └── URL Analyzer
               ↓
          URL Risk Score

              │
              ▼

Final Score =
(ML × 50%) +
(Rules × 30%) +
(URL × 20%)
```

### Example

```
Input:
"Your account is blocked. Share OTP urgently.
Click http://bit.ly/verify"

ML Score    = 96
Rule Score  = 60
URL Score   = 40

Final Score
= (96 × 0.5) + (60 × 0.3) + (40 × 0.2)
= 74

Category → Scam
```

| Score    | Category      |
| -------- | ------------- |
| 0 – 30   | 🟢 Safe       |
| 31 – 70  | 🟡 Suspicious |
| 71 – 100 | 🔴 Scam       |

---

## 🚀 Run Locally

### Prerequisites

* Node.js 18+
* Python 3.10+
* MongoDB

### Backend

```bash
cd scanly-backend

pip install -r requirements.txt

python ml/train.py

python -m uvicorn main:app --reload
```

Create a `.env` file:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=scanly_db
APP_NAME=SCANLY
DEBUG=True
```

Backend runs at:

```
http://localhost:8000
```

Swagger Docs:

```
http://localhost:8000/docs
```

---

### Frontend

```bash
cd scanly-frontend

npm install

npm run dev
```

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

Frontend runs at:

```
http://localhost:5173
```

---

## 📡 API Endpoints

### Scan Message

**POST** `/scan`

Request

```json
{
  "text": "Your account is blocked. Share OTP urgently.",
  "url": "http://bit.ly/verify-now"
}
```

Response

```json
{
  "status": "success",
  "input_text": "Your account is blocked. Share OTP urgently.",
  "final_score": 74,
  "category": "Scam",
  "ml_score": 96,
  "rule_score": 60,
  "url_score": 40,
  "matched_keywords": [
    "otp",
    "account blocked",
    "urgent"
  ],
  "explanation": "Scam keywords found: otp, account blocked | URL shortener detected."
}
```

| Method | Endpoint   | Description           |
| ------ | ---------- | --------------------- |
| POST   | `/scan`    | Scan text and URL     |
| GET    | `/history` | Retrieve scan history |
| DELETE | `/history` | Delete scan history   |
| GET    | `/health`  | Health check          |

---

## 📁 Project Structure

```text
scanly/
│
├── README.md
├── docs/
│   └── demo.gif
│
├── scanly-backend/
│   ├── main.py
│   ├── scorer.py
│   ├── rules.py
│   ├── url_checker.py
│   ├── models.py
│   ├── db.py
│   ├── render.yaml
│   └── ml/
│       ├── train.py
│       ├── preprocess.py
│       └── dataset.csv
│
└── scanly-frontend/
    ├── vercel.json
    └── src/
        ├── pages/
        ├── components/
        ├── services/
        └── context/
```

---

## 🧪 Sample Test Cases

| Input                                             | Expected Result |
| ------------------------------------------------- | --------------- |
| Your bank account is blocked. Share OTP urgently. | 🔴 Scam         |
| Congratulations! You won a lottery. Click now.    | 🔴 Scam         |
| Hey, are we still meeting at 5 PM today?          | 🟢 Safe         |
| Special offer selected for you.                   | 🟡 Suspicious   |
| http://192.168.1.1/bank/verify                    | 🔴 Scam         |

---

## 🔮 Future Enhancements

* Replace TF-IDF + Naive Bayes with **RoBERTa-base**
* OCR-based image and screenshot scam detection
* Browser extension
* WhatsApp integration
* Multilingual scam detection
* Community-reported scam database
* CI/CD pipeline
* Docker support

---

## 👨‍💻 Author

**Mani Aggarwal**

B.Tech CSE — ABES Engineering College

---

## 📄 License

MIT License

Feel free to use, modify, and distribute this project.
