from pymongo import MongoClient
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