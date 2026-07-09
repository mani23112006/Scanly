import pandas as pd
import numpy as np
import string
import os
from sklearn.model_selection import train_test_split

# ── File path ───────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATASET_CSV = os.path.join(BASE_DIR, "dataset.csv")
DATASET_TSV = os.path.join(BASE_DIR, "dataset.tsv")


def load_dataset() -> pd.DataFrame:
    """Load the SMS spam dataset from CSV or TSV."""

    if os.path.exists(DATASET_CSV):
        # Kaggle version — has encoding issues, specify latin-1
        df = pd.read_csv(
            DATASET_CSV,
            encoding="latin-1",
            usecols=[0, 1],          # only need first 2 columns
            names=["label", "text"], # rename them
            header=0                 # skip original header row
        )
        print(f"Loaded CSV: {len(df)} rows")

    elif os.path.exists(DATASET_TSV):
        # GitHub version — tab separated, clean encoding
        df = pd.read_csv(
            DATASET_TSV,
            sep="\t",
            names=["label", "text"]
        )
        print(f"Loaded TSV: {len(df)} rows")

    else:
        raise FileNotFoundError(
            "No dataset found. Place dataset.csv or dataset.tsv "
            "inside the ml/ folder."
        )

    return df


def explore_dataset(df: pd.DataFrame):
    """Print basic stats so you understand the data."""
    print("\n" + "=" * 50)
    print("DATASET EXPLORATION")
    print("=" * 50)

    print(f"\nShape      : {df.shape}")
    print(f"Columns    : {list(df.columns)}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nLabel distribution:")
    print(df["label"].value_counts())

    print("\nBasic stats:")
    print(df.describe())

    print("\nSample spam message:")
    spam_sample = df[df["label"] == "spam"]["text"].iloc[0]
    print(f"  {spam_sample}")

    print("\nSample ham message:")
    ham_sample = df[df["label"] == "ham"]["text"].iloc[0]
    print(f"  {ham_sample}")


def clean_text(text: str) -> str:
    """
    Clean a single text message:
    1. Lowercase everything
    2. Remove punctuation
    3. Strip extra whitespace
    """
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split())   # collapse multiple spaces
    return text


def preprocess(test_size: float = 0.2, random_state: int = 42):
    """
    Full pipeline: load → clean → encode → split.

    Returns:
        X_train, X_test, y_train, y_test
    """
    # 1. Load
    df = load_dataset()
    explore_dataset(df)

    # 2. Drop any rows with missing values
    df = df.dropna(subset=["text", "label"])

    # 3. Clean text
    print("\nCleaning text...")
    df["text_clean"] = df["text"].apply(clean_text)

    # 4. Encode labels: spam → 1, ham → 0
    df["label_encoded"] = df["label"].map({"spam": 1, "ham": 0})

    # Drop any rows where label didn't map (safety check)
    df = df.dropna(subset=["label_encoded"])

      # 5. Separate features and labels
    X = df["text_clean"].values   # array of cleaned message strings
    y = df["label_encoded"].values.astype(int)

    # 6. Train/test split — 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,  # same split every time you run
        stratify=y                  # keep spam/ham ratio equal in both splits
    )

    print("\n" + "=" * 50)
    print("SPLIT RESULTS")
    print("=" * 50)
    print(f"Total messages : {len(X)}")
    print(f"X_train shape  : {X_train.shape}  ← 80% for training")
    print(f"X_test shape   : {X_test.shape}   ← 20% for testing")
    print(f"y_train shape  : {y_train.shape}")
    print(f"y_test shape   : {y_test.shape}")

    spam_train = sum(y_train)
    print(f"\nSpam in train  : {spam_train} ({spam_train/len(y_train)*100:.1f}%)")
    spam_test = sum(y_test)
    print(f"Spam in test   : {spam_test} ({spam_test/len(y_test)*100:.1f}%)")

    print("\nSample cleaned message:")
    print(f"  Original : {df['text'].iloc[0]}")
    print(f"  Cleaned  : {df['text_clean'].iloc[0]}")

    return X_train, X_test, y_train, y_test


# ── Run directly to verify ──────────────────────────
if __name__ == "__main__":
    X_train, X_test, y_train, y_test = preprocess()
    print("\nPreprocessing complete. Ready for Day 7 training.")