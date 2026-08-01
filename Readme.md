# 🔍 SCANLY — AI-Powered Scam Detection System

> Detect phishing attempts in **SMS, URLs, and screenshots** using a hybrid AI pipeline powered by **RoBERTa, OCR, rule-based analysis, and URL intelligence**.

---

# ✨ Features

- 🤖 **RoBERTa-Based AI Detection** — Fine-tuned RoBERTa model trained on the SMS Spam Collection dataset for high-accuracy scam classification.
- 🖼️ **OCR Scam Detection** — Extracts text from screenshots using EasyOCR before AI analysis.
- 📋 **Rule-Based Detection** — Detects phishing keywords, urgency phrases, OTP requests, banking scams, and suspicious patterns.
- 🔗 **URL Risk Analysis** — Detects IP-based URLs, shortened links, HTTP links, suspicious domains, and phishing indicators.
- ⚖️ **Hybrid Risk Scoring**
  - AI Model (50%)
  - Rule Engine (30%)
  - URL Analyzer (20%)
- 📊 **Explainable AI** — Shows AI confidence, matched keywords, URL findings, and final explanation.
- 💾 **Scan History** — Stores previous scans in MongoDB Atlas.
- 🔐 **Firebase Authentication** — Secure email/password authentication with guest access.
- 🚦 **Rate Limiting** — API protection using SlowAPI.
- 📱 **Responsive UI** — Optimized for desktop, tablet, and mobile devices.
- ⚡ **Fast Inference** — Singleton model loading minimizes prediction latency.

---

# 🏗️ Architecture

```text
                   User Input
      (Text / URL / Screenshot Image)
                    │
                    ▼
            React + Vite Frontend
                    │
            POST /scan Request
                    │
                    ▼
              FastAPI Backend
                    │
     ┌──────────────┼───────────────┐
     │              │               │
     ▼              ▼               ▼
 OCR Extractor   RoBERTa Model   URL Analyzer
 (EasyOCR)           50%             20%
     │
     ▼
Extracted Text
     │
     ▼
 Rule Engine (30%)
     │
     └──────────────┬───────────────┘
                    ▼
           Weighted Risk Scorer
                    ▼
      Safe | Suspicious | Scam
                    ▼
             MongoDB Atlas
```

---

# 🛠️ Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | React 18, Vite, Tailwind CSS, React Router |
| Backend | FastAPI, Python 3.11, Uvicorn |
| AI/NLP | Hugging Face Transformers, RoBERTa-base, PyTorch |
| OCR | EasyOCR |
| Database | MongoDB Atlas |
| Authentication | Firebase Authentication |
| Rate Limiting | SlowAPI |
| ML Libraries | Transformers, Scikit-learn |
| Version Control | Git & GitHub |

---

# 📊 Model Performance

| Metric | Value |
|---------|-------|
| Dataset | SMS Spam Collection |
| Model | RoBERTa-base |
| Accuracy | 99.28% |
| F1 Score | 0.9928 |
| Input Types | SMS, URLs, Images |
| Risk Categories | Safe, Suspicious, Scam |

---

# 📈 Risk Scoring

SCANLY combines multiple detection techniques to generate a final scam score.

```text
          Input
            │
   ┌────────┼────────┐
   ▼        ▼        ▼
RoBERTa   Rules     URL
 50%       30%      20%
   └────────┼────────┘
            ▼
    Weighted Risk Score
            ▼
 Safe | Suspicious | Scam
```

### Example

```text
Input:

"Your account is blocked.
Share OTP immediately.

http://bit.ly/verify"

RoBERTa Score = 98
Rule Score    = 70
URL Score     = 45

Final Score
= (98 × 0.5)
+ (70 × 0.3)
+ (45 × 0.2)

= 79

Category → Scam
```

| Score | Category |
|--------|----------|
| 0–30 | 🟢 Safe |
| 31–70 | 🟡 Suspicious |
| 71–100 | 🔴 Scam |

---

# 🚀 Run Locally

## Prerequisites

- Node.js 18+
- Python 3.11+
- MongoDB

---

## Backend

```bash
cd scanly-backend

pip install -r requirements.txt

python -m uvicorn main:app --reload
```

Create `.env`

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=scanly_db
APP_NAME=SCANLY
DEBUG=True
```

Backend

```
http://localhost:8000
```

Swagger Docs

```
http://localhost:8000/docs
```

---

## Frontend

```bash
cd scanly-frontend

npm install

npm run dev
```

Create `.env`

```env
VITE_API_URL=http://localhost:8000
```

Frontend

```
http://localhost:5173
```

---

# 📡 API Endpoints

## POST /scan

Request

```json
{
  "text": "Your account has been blocked. Verify immediately.",
  "url": "http://bit.ly/verify"
}
```

Response

```json
{
  "status": "success",
  "final_score": 83,
  "category": "Scam",
  "ml_score": 98,
  "rule_score": 72,
  "url_score": 40,
  "matched_keywords": [
    "blocked",
    "verify",
    "otp"
  ],
  "ocr_text": null,
  "explanation": "Detected phishing keywords and suspicious shortened URL."
}
```

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/scan` | Scan text, URL, or screenshot |
| GET | `/history` | Retrieve scan history |
| DELETE | `/history` | Delete scan history |
| GET | `/health` | Health check |

---

# 📁 Project Structure

```text
scanly/
│
├── README.md
│
├── docs/
│   └── demo.gif
│
├── scanly-backend/
│   ├── main.py
│   ├── scorer.py
│   ├── rules.py
│   ├── url_checker.py
│   ├── ocr.py
│   ├── models.py
│   ├── db.py
│   ├── render.yaml
│   │
│   └── ml/
│       ├── roberta/
│       │   ├── predict.py
│       │   ├── train.py
│       │   └── saved_model/
│       │
│       ├── preprocess.py
│       └── dataset.csv
│
└── scanly-frontend/
    ├── src/
    │
    ├── pages/
    ├── components/
    ├── services/
    └── context/
```

---

# 🧪 Sample Test Cases

| Input | Expected |
|------|----------|
| Your account is blocked. Share OTP immediately. | 🔴 Scam |
| Congratulations! You won ₹10 lakh. Click now. | 🔴 Scam |
| Meeting has been shifted to 5 PM. | 🟢 Safe |
| Exclusive offer just for you. | 🟡 Suspicious |
| http://192.168.1.1/login | 🔴 Scam |
| Screenshot containing OTP scam message | 🔴 Scam |

---

# 🔮 Future Enhancements

- Browser Extension
- WhatsApp Integration
- Telegram Scam Detection
- Chrome Safe Browsing Integration
- Multilingual Scam Detection
- Community Reported Scam Database
- Docker Deployment
- CI/CD Pipeline
- AWS Deployment
- ONNX Model Optimization

---

# 👨‍💻 Author

**Mani Aggarwal**

B.Tech CSE — ABES Engineering College

---

# 📄 License

MIT License

Feel free to use, modify, and distribute this project.