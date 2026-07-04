from dotenv import load_dotenv
import os
from db import db

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "SCANLY")

print("Connected to:", db.name)



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SCANLY API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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