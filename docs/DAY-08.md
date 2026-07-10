# Day 8 – Risk Scoring Engine

## ✅ Completed

Implemented a centralized **Risk Scoring Engine** that combines outputs from all three detection modules into a single, explainable risk verdict.

### Features Added

* Created `scorer.py` to aggregate detection results
* Combined scores using weighted averaging:

  * **Machine Learning:** 50%
  * **Rule-Based Detection:** 30%
  * **URL Analysis:** 20%
* Generated a final risk score (0–100)
* Classified messages into:

  * 🟢 **Safe** (0–30)
  * 🟡 **Suspicious** (31–70)
  * 🔴 **Scam** (71–100)
* Returned a detailed JSON response containing:

  * Final score
  * Risk category
  * ML score
  * Rule-based score
  * URL score
  * Matched scam keywords
  * Flagged URLs
  * Human-readable explanation

## Example Response

```json
{
  "status": "success",
  "final_score": 37,
  "category": "Suspicious",
  "ml_score": 47,
  "rule_score": 20,
  "url_score": 40,
  "matched_keywords": [
    "otp"
  ],
  "flagged_urls": [
    "http://bit.ly/free"
  ],
  "explanation": "Scam keywords found: otp | HTTP not HTTPS | URL shortener detected: bit.ly"
}
```

## Risk Score Formula

```text
Final Score =
(ML Score × 0.50) +
(Rule Score × 0.30) +
(URL Score × 0.20)
```

This weighted approach prioritizes the Machine Learning model while incorporating deterministic rule-based checks and URL reputation analysis for a balanced, explainable verdict.

## Folder Structure

```text
scanly-backend/
├── scorer.py
├── ml_detector.py
├── rule_detector.py
├── url_detector.py
├── main.py
└── ...
```

## Learning Outcomes

* Weighted average scoring
* Ensemble decision making
* Explainable AI outputs
* Modular backend architecture
* Risk categorization using multiple detection engines

## Status

✅ Day 8 Completed

Next: **Day 9 – Integrate the scoring engine into the `/scan` API, persist scan history in MongoDB, and add a `/history` endpoint.**
