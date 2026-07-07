# Day 2 – MongoDB Integration

## Overview

Day 2 focused on integrating a local MongoDB database with the backend. Instead of using MongoDB Atlas, a local MongoDB Community Server was configured for development.

## Completed Tasks

* Installed MongoDB Community Server.
* Installed MongoDB Compass.
* Configured environment variables.
* Created a dedicated database connection module (`db.py`).
* Connected the FastAPI backend to MongoDB.
* Verified the database connection using a ping test.

## Technologies Used

* MongoDB Community Server
* MongoDB Compass
* PyMongo
* Motor

## Files Added

```text
scanly-backend/
├── db.py
├── .env
└── requirements.txt
```

## Outcome

* MongoDB connected successfully.
* Database connection tested successfully.
* Backend ready to store scan history in future updates.

## Next Goal

Develop the first REST API endpoint for scam message analysis.
