# Day 9 – MongoDB Integration & Scan History API

## ✅ Completed

Integrated **MongoDB** with the Scanly backend to persist scan results and implemented asynchronous FastAPI endpoints for a complete, production-style backend workflow.

## Features Added

### 📌 Scan History Storage

* Every scan result is automatically saved to MongoDB.
* Each record stores:

  * Input text
  * Final risk score
  * Risk category
  * ML score
  * Rule-based score
  * URL score
  * Matched scam keywords
  * Flagged URLs
  * Explanation
  * Timestamp

### 📌 Async FastAPI Endpoints

Updated API routes to use `async def`, enabling non-blocking request handling and preparing the backend for future scalability.

### 📌 New API Endpoints

| Method | Endpoint                | Description                                                   |
| ------ | ----------------------- | ------------------------------------------------------------- |
| GET    | `/`                     | Health check                                                  |
| GET    | `/health`               | API status and version                                        |
| POST   | `/scan`                 | Analyze text, generate risk score, and save result to MongoDB |
| GET    | `/history`              | Retrieve the latest scan history                              |
| DELETE | `/history` *(Optional)* | Clear all stored scan history                                 |

### 📌 MongoDB Integration

Each scan is stored in the `scanly_db` database under the `scans` collection.

Example document:

```json
{
  "input_text": "Your account is blocked. OTP: 4829. Click http://bit.ly/free",
  "final_score": 37,
  "category": "Suspicious",
  "ml_score": 47,
  "rule_score": 20,
  "url_score": 40,
  "matched_keywords": ["otp"],
  "flagged_urls": ["http://bit.ly/free"],
  "explanation": "Scam keywords found: otp | HTTP not HTTPS | URL shortener detected: bit.ly",
  "timestamp": "2026-07-11T10:30:00Z"
}
```

## Backend Workflow

```text
Client Request
      │
      ▼
POST /scan
      │
      ▼
ML Detector
      │
Rule-Based Detector
      │
URL Analyzer
      │
Risk Scoring Engine
      │
Save Result to MongoDB
      │
Return Complete JSON Response
```

## Folder Structure

```text
scanly-backend/
├── main.py
├── models.py
├── scorer.py
├── rule_detector.py
├── url_detector.py
├── ml_detector.py
├── db.py
├── ml/
│   ├── train.py
│   ├── model.pkl
│   └── vectorizer.pkl
├── .env
├── requirements.txt
└── README.md
```

## Learning Outcomes

* MongoDB CRUD operations with Python
* FastAPI asynchronous endpoints (`async def`)
* REST API design and endpoint organization
* Persistent scan history
* Backend modularization
* Automatic API documentation using FastAPI Swagger (`/docs`)

## Project Status

### ✅ Backend MVP Completed

The Scanly backend now supports:

* Rule-based scam detection
* Machine Learning classification
* URL risk analysis
* Weighted risk scoring
* Explainable detection
* MongoDB scan history
* RESTful API endpoints
* Interactive Swagger API documentation

**Next:** Day 10 – React frontend integration and dashboard development.
