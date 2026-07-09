# Day 6 – ML Data Preparation (NLP Dataset)

## Overview

Today focused on preparing the dataset required for the Machine Learning spam detection model. No model training was performed. The objective was to clean and preprocess the SMS dataset so it is ready for training on Day 7.

---

## Objectives

- Set up the `ml/` directory
- Download the SMS Spam Collection dataset (5572 labelled messages)
- Load the dataset using Pandas
- Explore the dataset
- Clean and preprocess message text
- Convert labels (`ham` → 0, `spam` → 1)
- Split the dataset into training and testing sets (80:20)

---

## Folder Structure

```text
scanly-backend/
├── ml/
│   ├── dataset.csv
│   └── preprocess.py
├── main.py
├── rules.py
├── url_checker.py
├── db.py
└── .env
```

---

## Dataset

**Dataset:** SMS Spam Collection Dataset

- Total Messages: **5572**
- Labels:
  - **ham** → Legitimate message
  - **spam** → Scam/Spam message

Example:

| Label | Message |
|-------|---------|
| ham | Hey, are we meeting today? |
| spam | Congratulations! You've won a free prize. |

---

## Data Preprocessing

The preprocessing pipeline performs:

- Convert text to lowercase
- Remove punctuation
- Remove extra whitespace
- Encode labels:
  - ham → 0
  - spam → 1
- Split data into:
  - 80% Training
  - 20% Testing

---

## ML Pipeline

```text
dataset.csv
      │
      ▼
Load with Pandas
      │
      ▼
Clean Text
(lowercase + remove punctuation)
      │
      ▼
Label Encoding
ham → 0
spam → 1
      │
      ▼
Train/Test Split
80% / 20%
      │
      ▼
Ready for Day 7 Training
```

---

## Learning Outcomes

Today covered the fundamentals of Machine Learning datasets.

### Features (X)

The SMS message itself.

Example:

```
"Congratulations! You won a free iPhone."
```

### Labels (y)

The correct answer.

```
0 = Ham (Safe)
1 = Spam (Scam)
```

The model learns the relationship between Features (X) and Labels (y).

---

## Expected Output

```python
X_train.shape
```

Output:

```text
(4457,)
```

Approximately 80% of the dataset is used for training.

---

## Technologies Used

- Python
- Pandas
- NumPy
- scikit-learn

---

## Next Step

Day 7 will train a Machine Learning model using:

- TF-IDF Vectorizer
- Multinomial Naive Bayes
- Model Evaluation
- Save trained model (`model.pkl`)
- Save TF-IDF vocabulary (`vectorizer.pkl`)