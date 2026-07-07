# Day 4 – Rule-Based Scam Detection Engine

## Overview

On Day 4, the rule-based scam detection engine was implemented and integrated into the FastAPI backend. Instead of returning a hardcoded rule score, the API now analyzes incoming text using predefined scam-related keywords and calculates a dynamic scam score.

## What Was Implemented

* Developed `rules.py` to perform keyword-based scam detection.
* Created a weighted keyword dictionary for common scam phrases.
* Implemented case-insensitive text matching.
* Calculated a dynamic rule score (maximum score capped at 100).
* Returned all matched scam keywords.
* Integrated the rule engine with the `/scan` API endpoint.
* Combined the rule score with placeholder ML and URL scores to generate a final scam score.
* Generated scam category and explanation based on the calculated score.

## Rule Engine Workflow

1. Receive the input message.
2. Convert the text to lowercase.
3. Search for predefined scam keywords.
4. Add the corresponding weight for every matched keyword.
5. Cap the score at 100.
6. Return:

   * Rule score
   * Matched keywords

## Example

### Input

```text
You won a prize! Click here urgently.
```

### Output

```json
{
  "rule_score": 60,
  "matched_keywords": [
    "prize",
    "click here",
    "urgent"
  ]
}
```

## API Response Example

```json
{
  "status": "success",
  "input_text": "Your bank account is blocked. Share your OTP urgently to verify account and claim prize.",
  "final_score": 59,
  "category": "Suspicious",
  "ml_score": 70,
  "rule_score": 80,
  "url_score": 0,
  "matched_keywords": [
    "prize",
    "otp",
    "verify account",
    "urgent"
  ],
  "explanation": "Suspicious patterns found. Triggered by: prize, otp, verify account, urgent."
}
```

## Project Structure

```text
scanly-backend/
├── main.py
├── models.py
├── rules.py
├── requirements.txt
└── ...
```

## Current Status

* ✅ Rule-based scam detection engine completed.
* ✅ Dynamic keyword scoring implemented.
* ✅ FastAPI integration completed.
* ✅ API returns rule score and matched keywords.

## Next Steps

* Replace the placeholder ML score with a trained machine learning model.
* Implement URL reputation analysis.
* Improve keyword detection using NLP techniques such as stemming and fuzzy matching.
