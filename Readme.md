SCANLY — Day 1: Project Setup

A modular AI-based scam detection system combining NLP, rule-based logic, and URL analysis to deliver real-time risk scoring with explainable results.

What was built today

Day 1 scaffolds the full project: a React (Vite) frontend, a FastAPI backend, and the folder structure both will grow into over the next 20 days. No scam-detection logic yet — today is purely getting both servers running and talking to each other.

Prerequisites installed


Node.js (v20+) and npm
Python 3.10+
VS Code with Python and Prettier extensions


Folder structure

scanly/
├── scanly-backend/
│   ├── main.py            FastAPI app entry point, CORS config, health routes
│   ├── requirements.txt   Python dependencies
│   ├── .env                Environment variables (not committed)
│   └── .gitignore          Excludes .env, __pycache__, venv, etc.
│
└── scanly-frontend/
    ├── src/
    │   ├── components/     Reusable UI pieces (empty for now)
    │   ├── pages/           Full page views (empty for now)
    │   ├── services/        API call logic (empty for now)
    │   ├── App.jsx           Root component
    │   └── main.jsx          Vite entry point
    ├── index.html
    └── package.json

Backend setup

bashcd scanly-backend
pip install fastapi uvicorn pymongo python-dotenv
uvicorn main:app --reload

Runs at http://localhost:. Interactive API docs at http://localhost:/docs.

main.py

pythonfrom dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "SCANLY")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SCANLY API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SCANLY backend is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

requirements.txt

fastapi
uvicorn
pymongo
motor
python-dotenv

.env

MONGO_URI=mongodb+srv://placeholder_for_now
APP_NAME=SCANLY
DEBUG=True


The real MONGO_URI gets filled in on Day 2.



.gitignore

.env
__pycache__/
*.pyc
*.pkl
venv/
.venv/

Frontend setup

bashcd scanly-frontend
npm install
npm run dev


src/App.jsx

jsxfunction App() {
  return (
    <div>
      <h1>SCANLY</h1>
      <p>Scam detection system — coming soon</p>
    </div>
  )
}

export default App





Next: Day 2

SCANLY — Day 2: MongoDB Local Setup

MongoDB Atlas required billing info for the Flex tier, so we installed MongoDB Community Server locally instead. Works identically with Python — no billing, no account needed.

What was installed


MongoDB Community Server (via MSI installer) — the actual database engine, runs as a Windows service automatically
MongoDB Compass — GUI app to visually browse your database and collections
mongosh — MongoDB shell to interact with the database from the terminal


Verify MongoDB is running

Open a terminal and run:

bashmongosh

You should see a test> prompt. That means MongoDB is live on your machine.

Type exit to quit the shell.

Folder changes today

scanly-backend/
├── main.py
├── db.py              ← NEW: MongoDB connection file
├── requirements.txt   ← UPDATED: added motor
├── .env               ← UPDATED: real local MONGO_URI
└── .gitignore

.env — update this

Replace the Day 1 placeholder with the local connection string:

MONGO_URI=mongodb://localhost:27017
DB_NAME=scanly_db
APP_NAME=SCANLY
DEBUG=True

No username, no password needed — local MongoDB runs without auth by default.

requirements.txt — add motor

fastapi
uvicorn
pymongo
motor
python-dotenv

Install the updated packages:

bashpip install pymongo motor python-dotenv

db.py — create this file

Create scanly-backend/db.py with the following content:

pythonfrom pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "scanly_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

scans_collection = db["scans"]

def test_connection():
    try:
        client.admin.command("ping")
        print("✅ Connected to MongoDB successfully!")
        print(f"   Database: {DB_NAME}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()

Test the connection

Run this from inside scanly-backend:

bashpython db.py

Expected output:

✅ Connected to MongoDB successfully!
   Database: scanly_db

If you see that, your Python backend can now talk to your local MongoDB database.

Verify in Compass (optional but useful)


Open MongoDB Compass
Connection string is already pre-filled: mongodb://localhost:27017
Click Connect
You won't see scanly_db yet — MongoDB creates the database automatically the first time you write data to it (that happens on Day 9)


What scans_collection is

scans_collection = db["scans"] creates a reference to a collection called scans inside scanly_db. Think of it like a table in a regular database. Every time a user scans a message (Day 9 onward), the result gets saved here. You'll see it appear in Compass after the first scan.