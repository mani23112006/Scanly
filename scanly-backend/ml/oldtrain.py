"""
Training Pipeline

dataset.csv
      │
      ▼
preprocess.py (clean text)
      │
      ▼
TF-IDF Vectorizer (convert text → numerical vectors)
      │
      ▼
Naive Bayes Model (learn spam/ham patterns)
      │
      ▼
Evaluate Accuracy
      │
      ▼
Save trained files:
    ├── model.pkl
    └── vectorizer.pkl
"""




import os
import sys
import joblib
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# Add parent directory to path so we can import preprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml.preprocess import preprocess, clean_text

# ── File paths ──────────────────────────────────────
BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH     = os.path.join(BASE_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")


def train():
    """Train TF-IDF + Naive Bayes model and save to disk."""

    print("=" * 55)
    print("SCANLY ML Training — Day 7")
    print("=" * 55)

    # ── Step 1: Load preprocessed data ─────────────
    print("\nStep 1: Loading and preprocessing data...")
    X_train, X_test, y_train, y_test = preprocess()

    # ── Step 2: TF-IDF vectorization ───────────────
    print("\nStep 2: Converting text to TF-IDF numbers...")
    vectorizer = TfidfVectorizer(
        max_features=5000,    # keep top 5000 most important words
        ngram_range=(1, 2),   # include single words AND word pairs
        stop_words="english"  # ignore common words like "the", "is"
    )

    # fit_transform: learn vocabulary from train, then convert
    X_train_tfidf = vectorizer.fit_transform(X_train)

    # transform only: use same vocabulary to convert test set
    X_test_tfidf  = vectorizer.transform(X_test)

    print(f"Vocabulary size : {len(vectorizer.vocabulary_)} words")
    print(f"Train matrix    : {X_train_tfidf.shape}")
    print(f"Test matrix     : {X_test_tfidf.shape}")

       # ── Step 3: Train Naive Bayes ───────────────────
    print("\nStep 3: Training Naive Bayes classifier...")
    model = MultinomialNB(alpha=0.1)   # alpha: smoothing (0.1 works well for spam)
    model.fit(X_train_tfidf, y_train)
    print("Training complete!")

    # ── Step 4: Evaluate ────────────────────────────
    print("\nStep 4: Evaluating on test set...")
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nAccuracy : {accuracy * 100:.2f}%")

    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  True Negatives  (ham   → ham  ) : {cm[0][0]}")
    print(f"  False Positives (ham   → spam ) : {cm[0][1]}")
    print(f"  False Negatives (spam  → ham  ) : {cm[1][0]}")
    print(f"  True Positives  (spam  → spam ) : {cm[1][1]}")

    print("\nFull Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["ham", "spam"]))

    # ── Step 5: Save model and vectorizer ───────────
    print("Step 5: Saving model and vectorizer...")
    joblib.dump(model,      MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"  Model saved      → {MODEL_PATH}")
    print(f"  Vectorizer saved → {VECTORIZER_PATH}")

    return model, vectorizer


def load_model():
    """Load saved model and vectorizer from disk."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "model.pkl not found. Run train.py first."
        )
    model      = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


def predict(text: str) -> float:
    """
    Predict scam probability for a single text message.

    Args:
        text: raw message string

    Returns:
        float: probability of being spam/scam (0.0 to 1.0)
    """
    model, vectorizer = load_model()

    # Clean text the same way training data was cleaned
    cleaned = clean_text(text)

    # Convert to TF-IDF using the saved vocabulary
    text_tfidf = vectorizer.transform([cleaned])

    # predict_proba returns [prob_ham, prob_spam]
    # we want index [1] = spam probability
    prob_spam = model.predict_proba(text_tfidf)[0][1]

    return round(float(prob_spam), 4)


# ── Run directly to train + test ────────────────────
if __name__ == "__main__":

    # Train the model
    model, vectorizer = train()

    # Test predict() on sample messages
    print("\n" + "=" * 55)
    print("PREDICT FUNCTION TEST")
    print("=" * 55)

    test_messages = [
        "You won a free prize! Claim now urgently.",
        "Hey, are we still meeting at 5pm today?",
        "Your bank account is blocked. Share OTP immediately.",
        "Congratulations! You are selected for a lottery of $10000.",
        "Can you send me the project report by tomorrow?",
        "FREE entry to win FA Cup tickets. Text WIN to 87121 now!"
    ]

    for msg in test_messages:
        prob = predict(msg)
        label = "SCAM" if prob > 0.5 else "SAFE"
        print(f"\nMessage : {msg[:55]}...")
        print(f"Score   : {prob}  [{label}]")