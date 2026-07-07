# SCANLY

An AI-powered scam detection system that analyzes text messages and URLs using a hybrid approach combining Machine Learning, rule-based detection, and URL reputation analysis to provide real-time, explainable scam risk scores.

> **Project Status:** 🚧 In Development (Day 4 of 20)

---

## Features

* Rule-based scam keyword detection
* Dynamic scam risk scoring
* Explainable detection with matched keywords
* REST API built with FastAPI
* Input validation using Pydantic
* MongoDB integration
* Interactive API documentation (Swagger UI)
* React frontend (under development)
* Machine Learning detection *(Coming Soon)*
* URL reputation analysis *(Coming Soon)*

---

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn
* MongoDB
* PyMongo
* Motor

### Frontend

* React
* Vite
* JavaScript

### Database

* MongoDB Community Server

---

## Project Structure

```text
scanly/
│
├── docs/
│   ├── DAY-01.md
│   ├── DAY-02.md
│   ├── DAY-03.md
│   └── DAY-04.md
│
├── scanly-backend/
│   ├── main.py
│   ├── models.py
│   ├── rules.py
│   ├── db.py
│   ├── requirements.txt
│   └── .env
│
└── scanly-frontend/
    ├── src/
    ├── package.json
    └── vite.config.js
```

---

## Current API Endpoints

| Method | Endpoint  | Description                      |
| ------ | --------- | -------------------------------- |
| GET    | `/`       | Backend status                   |
| GET    | `/health` | Health check                     |
| POST   | `/scan`   | Analyze text for scam indicators |

---

## Example Request

```json
{
  "text": "You won a prize! Click here urgently"
}
```

---

## Example Response

```json
{
  "status": "success",
  "input_text": "You won a prize! Click here urgently",
  "final_score": 53,
  "category": "Suspicious",
  "ml_score": 70,
  "rule_score": 60,
  "url_score": 0,
  "matched_keywords": [
    "prize",
    "click here",
    "urgent"
  ],
  "explanation": "Suspicious patterns found. Triggered by: prize, click here, urgent."
}
```

---

## Progress

| Day   | Status | Description                      |
| ----- | :----: | -------------------------------- |
| Day 1 |    ✅   | Project setup (React + FastAPI)  |
| Day 2 |    ✅   | MongoDB local setup              |
| Day 3 |    ✅   | REST API and Pydantic validation |
| Day 4 |    ✅   | Rule-based scam detection engine |
| Day 5 |    ⏳   | In Progress                      |

Detailed daily progress is available in the `docs/` directory.

---

## Current Detection Pipeline

```
User Input
     │
     ▼
FastAPI API
     │
     ▼
Rule Engine
     │
     ▼
Weighted Scoring
     │
     ▼
Risk Category
     │
     ▼
JSON Response
```

---

## Roadmap

* [x] Backend setup
* [x] MongoDB integration
* [x] REST API
* [x] Rule-based detection
* [ ] Machine Learning model
* [ ] URL reputation analysis
* [ ] Save scan history
* [ ] React UI integration
* [ ] User authentication
* [ ] Deployment

---

## Running the Project

### Backend

```bash
cd scanly-backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Backend:

```
http://localhost:8000
```

Swagger Documentation:

```
http://localhost:8000/docs
```

### Frontend

```bash
cd scanly-frontend
npm install
npm run dev
```

Frontend:

```
http://localhost:5173
```

---

## License

This project is being developed for educational and portfolio purposes.
