# 🤖 Day 5 – AI URL Risk Analysis Module

## Overview

Today, I enhanced **Scanly**, my AI-powered scam detection system, by adding an intelligent **URL Risk Analysis** module.

Scammers frequently disguise malicious links to trick users into revealing sensitive information. This module automatically extracts URLs from incoming messages, analyzes multiple phishing indicators, and generates an explainable risk score.

Instead of relying on external APIs or blacklists, Scanly uses an **AI-inspired heuristic engine** that mimics how a cybersecurity analyst evaluates suspicious URLs.

---

## What This Module Does

Given any message, Scanly:

* Detects embedded URLs
* Parses each URL into its components
* Evaluates multiple phishing indicators
* Assigns a cumulative risk score
* Explains every detected red flag

This makes the decision process transparent and easy to understand.

---

## Detection Rules

| Security Check                            | Risk Score |
| ----------------------------------------- | ---------: |
| Raw IP address instead of domain          |        +30 |
| HTTP instead of HTTPS                     |        +25 |
| Suspicious TLD (.xyz, .tk, .ml, .ga, .cf) |        +20 |
| URL longer than 75 characters             |        +20 |
| Multiple subdomains                       |        +15 |
| Suspicious path keywords                  |        +15 |
| URL shortening service                    |        +15 |

---

## AI Pipeline

```text
Incoming Message
        │
        ▼
Extract URLs
        │
        ▼
Parse URL Components
        │
        ▼
Heuristic Analysis Engine
        │
        ├── HTTPS Check
        ├── Domain Analysis
        ├── TLD Detection
        ├── URL Length Analysis
        ├── Subdomain Analysis
        ├── Path Keyword Detection
        └── Shortened URL Detection
        │
        ▼
Risk Score Generation
        │
        ▼
Explainable Security Report
```

---

## Example

### Input

```text
Congratulations!

Verify your account immediately.

http://bit.ly/freegift
```

### Output

```text
Detected URL:
http://bit.ly/freegift

Risk Score: 40/100

Reasons:
• Uses HTTP
• URL Shortener

Verdict:
⚠️ Medium Risk
```

---

## Technologies Used

* Python 3
* Regular Expressions (`re`)
* `urllib.parse`
* Rule-Based AI
* Explainable AI (XAI) Principles

---

## Why This Matters

Traditional URL filters often rely on online databases or third-party APIs. This module demonstrates how intelligent rule-based analysis can identify suspicious URLs offline using explainable decision-making.

This approach keeps the system lightweight, transparent, and suitable for cybersecurity-focused AI applications.

---

## Next Steps

* Domain reputation scoring
* Homoglyph domain detection
* Punycode detection
* WHOIS-based domain age analysis
* AI-based phishing classification
* Ensemble scam detection engine
