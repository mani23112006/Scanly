
import os
import sys
import numpy as np
import pandas as pd

# Add parent dirs to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from transformers import (
    RobertaTokenizer,
    RobertaForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)
from datasets import Dataset
from sklearn.metrics import (
    accuracy_score, f1_score,
    precision_score, recall_score,
    classification_report
)

# Import config from parent
from ml.roberta.config import (
    MODEL_NAME, MAX_LENGTH, BATCH_SIZE, EPOCHS,
    LEARNING_RATE, WARMUP_STEPS, WEIGHT_DECAY,
    SAVE_DIR, CHECKPOINT_DIR, TEST_SIZE,
    RANDOM_SEED, NUM_LABELS, MODEL_VERSION
)
from ml.preprocess import load_raw_dataset

print("=" * 60)
print("SCANLY RoBERTa Fine-tuning")
print("=" * 60)

# ── 1. Load dataset ─────────────────────────────────
print("\n[1/5] Loading dataset...")
df = load_raw_dataset()

# ── 2. Create HuggingFace Dataset ───────────────────

print("\n[2/5] Creating HuggingFace dataset...")
from datasets import ClassLabel

hf_dataset = Dataset.from_pandas(df[["text", "label"]])

# Cast label column to ClassLabel so stratify works
hf_dataset = hf_dataset.cast_column(
    "label",
    ClassLabel(num_classes=2, names=["ham", "spam"])
)

# Stratified split
splits = hf_dataset.train_test_split(
    test_size=TEST_SIZE,
    seed=RANDOM_SEED,

    stratify_by_column="label"
)
train_ds = splits["train"]


test_ds  = splits["test"]



print(f"Train: {len(train_ds)} samples")
print(f"Test:  {len(test_ds)} samples")

# ── 3. Tokenization ──────────────────────────────
# 
# 
# ───
print("\n[3/5] Tokenizing with RobertaTokenizer...")
tokenizer = RobertaTokenizer.from_pretrained(MODEL_NAME)


def tokenize_batch(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
    )

train_tok = train_ds.map(tokenize_batch, batched=True, batch_size=64)
test_tok  = test_ds.map(tokenize_batch,  batched=True, batch_size=64)
   
# HuggingFace Trainer expects "labels" column
train_tok = train_tok.rename_column("label", "labels")
test_tok  = test_tok.rename_column("label",  "labels")

# Set format for PyTorch
train_tok.set_format("torch", columns=["input_ids","attention_mask","labels"])
test_tok.set_format("torch",  columns=["input_ids","attention_mask","labels"])

print("Tokenization complete.")

# ── 4. Model + Training ─────────────────────────────
print("\n[4/5] Loading roberta-base model...")
model = RobertaForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS,
    ignore_mismatched_sizes=True,
)

# ── Metrics function ────────────────────────────────
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy":  round(accuracy_score(labels, preds), 4),
        "f1":        round(f1_score(labels, preds, average="weighted"), 4),
        "precision": round(precision_score(labels, preds, average="weighted"), 4),
        "recall":    round(recall_score(labels, preds, average="weighted"), 4),
    }

# ── Training arguments ──────────────────────────────
training_args = TrainingArguments(
    output_dir=CHECKPOINT_DIR,

    # Core training
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE * 2,

    # Optimizer
    learning_rate=LEARNING_RATE,
    warmup_steps=WARMUP_STEPS,
    weight_decay=WEIGHT_DECAY,

    # Evaluation
    eval_strategy="epoch",       # evaluate after every epoch
    save_strategy="epoch",       # save checkpoint every epoch
    load_best_model_at_end=True, # restore best checkpoint at end
    metric_for_best_model="f1",
    greater_is_better=True,

    # Logging
    logging_steps=50,
    logging_dir=os.path.join(CHECKPOINT_DIR, "logs"),
    report_to="none",            # disable wandb / tensorboard

    # Reproducibility
    seed=RANDOM_SEED,
    data_seed=RANDOM_SEED,

    # Performance
    fp16=False,                  # set True only if CUDA available
    dataloader_num_workers=0,    # 0 is safest on Windows
)
# ── Trainer ─────────────────────────────────────────
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tok,
    eval_dataset=test_tok,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
)

print("\n[4/5] Starting training...")
print(f"  Epochs:     {EPOCHS}")
print(f"  Batch size: {BATCH_SIZE}")
print(f"  LR:         {LEARNING_RATE}")
print(f"  Device:     {'GPU' if __import__('torch').cuda.is_available() else 'CPU'}")
print("-" * 60)

trainer.train()

# ── 5. Evaluate + Save ──────────────────────────────
print("\n[5/5] Evaluating on test set...")
results = trainer.evaluate()

print("\n" + "=" * 60)
print("FINAL EVALUATION RESULTS")
print("=" * 60)
print(f"  Accuracy:  {results.get('eval_accuracy', 0):.4f}")
print(f"  F1 Score:  {results.get('eval_f1', 0):.4f}")
print(f"  Precision: {results.get('eval_precision', 0):.4f}")
print(f"  Recall:    {results.get('eval_recall', 0):.4f}")
print(f"  Loss:      {results.get('eval_loss', 0):.4f}")
print("=" * 60)

# Detailed classification report
print("\nDetailed Classification Report:")
preds_out = trainer.predict(test_tok)
y_pred = np.argmax(preds_out.predictions, axis=-1)
y_true = preds_out.label_ids
print(classification_report(y_true, y_pred, target_names=["ham", "spam"]))


# Save model + tokenizer
print(f"\nSaving model to: {SAVE_DIR}")
os.makedirs(SAVE_DIR, exist_ok=True)
trainer.save_model(SAVE_DIR)
tokenizer.save_pretrained(SAVE_DIR)

# Save a metadata file
import json
metadata = {
    "model_name":   MODEL_NAME,
    "model_version": MODEL_VERSION,
    "accuracy":     results.get("eval_accuracy", 0),
    "f1_score":     results.get("eval_f1", 0),
    "epochs":       EPOCHS,
    "batch_size":   BATCH_SIZE,
    "max_length":   MAX_LENGTH,
    "train_samples": len(train_tok),
    "test_samples":  len(test_tok),
}
with open(os.path.join(SAVE_DIR, "training_metadata.json"), "w") as f:
    json.dump(metadata, f, indent=2)

print("\n✅ Training complete!")
print(f"   Model saved to: {SAVE_DIR}")
print(f"   Accuracy: {results.get('eval_accuracy',0):.2%}")
print(f"   F1 Score: {results.get('eval_f1',0):.4f}")