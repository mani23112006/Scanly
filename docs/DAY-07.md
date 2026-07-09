# Day 7 – NLP Model Training (TF-IDF + Naive Bayes)

## Overview

Today focused on building the Machine Learning component of Scanly. The SMS dataset prepared on Day 6 was converted into numerical features using TF-IDF, and a Multinomial Naive Bayes classifier was trained to detect spam and scam messages. The trained model and vectorizer were saved for reuse, eliminating the need to retrain on every request.

---

## Objectives

- Load preprocessed SMS dataset
- Convert text into numerical features using TF-IDF
- Train a Multinomial Naive Bayes classifier
- Evaluate model performance
- Save trained model and vectorizer
- Implement reusable prediction function
- Integrate ML scoring into Scanly backend

---

## Folder Structure

```text
scanly-backend/
├── ml/
│   ├── dataset.csv
│   ├── preprocess.py
│   ├── train.py
│   ├── model.pkl
│   └── vectorizer.pkl
├── main.py
├── rules.py
├── url_checker.py
├── db.py
└── .env
```

---

## Machine Learning Pipeline

```text
dataset.csv
      │
      ▼
preprocess.py
(Clean Text)
      │
      ▼
TF-IDF Vectorizer
(Text → Numerical Features)
      │
      ▼
Multinomial Naive Bayes
(Model Training)
      │
      ▼
Model Evaluation
(Accuracy & Metrics)
      │
      ▼
Save
model.pkl
vectorizer.pkl
      │
      ▼
Predict New Messages
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- scikit-learn
- Joblib

---

## Model Used

### TF-IDF (Term Frequency–Inverse Document Frequency)

TF-IDF converts text messages into numerical vectors based on the importance of words.

Example:

```
"You won a free prize"
```

↓

```
[0.00, 0.42, 0.17, 0.68, ...]
```

These numerical vectors become the input for the Machine Learning model.

---

### Multinomial Naive Bayes

A probabilistic classification algorithm widely used for text classification.

The model learns patterns from thousands of labelled SMS messages and predicts the probability that a new message is spam.

---

## Model Evaluation

The trained model is evaluated using:

- Accuracy Score
- Confusion Matrix
- Classification Report
  - Precision
  - Recall
  - F1-Score

Expected accuracy:

```
≈97–99%
```

(depending on dataset split)

---

## Saved Files

### model.pkl

Stores the trained Naive Bayes classifier.

Purpose:

- Avoid retraining every time
- Load instantly during API requests

---

### vectorizer.pkl

Stores the trained TF-IDF vocabulary.

Purpose:

Ensures new messages are converted into numerical vectors using the exact same vocabulary learned during training.

---

## Prediction Flow

```text
User Message
      │
      ▼
Clean Text
      │
      ▼
Load vectorizer.pkl
      │
      ▼
Convert Text → TF-IDF Features
      │
      ▼
Load model.pkl
      │
      ▼
Predict Scam Probability
      │
      ▼
Return ML Score
```

---

## Backend Integration

The fake ML score was replaced with the real Machine Learning prediction.

Example:

```json
{
  "ml_score": 99
}
```

The ML score is combined with:

- Rule-based detection
- URL phishing analysis

to calculate the final scam risk score.

---

## Sample Prediction

Input

```
You won a free prize! Claim your OTP now urgently.
```

Output

```json
{
  "ml_score": 99,
  "rule_score": 60,
  "url_score": 0,
  "final_score": 67,
  "category": "Suspicious"
}
```

---

## Learning Outcomes

Today covered:

- Natural Language Processing (NLP)
- TF-IDF Vectorization
- Text Classification
- Multinomial Naive Bayes
- Model Evaluation
- Model Persistence using Joblib

---

## Key Takeaways

- Text must be converted into numbers before Machine Learning.
- TF-IDF assigns importance scores to words.
- Naive Bayes learns spam and ham patterns from labelled data.
- Saving both the model and vectorizer avoids retraining and ensures consistent predictions.
- The backend now uses a real Machine Learning model instead of hardcoded values.

---

## Next Steps

- Improve final scoring strategy
- Store scan history in MongoDB
- Collect user feedback for future model improvements
- Connect the React frontend with the backend API