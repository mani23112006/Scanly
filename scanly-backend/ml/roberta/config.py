import os

# ── Model ──────────────────────────────────────────
MODEL_NAME    = "roberta-base"         # HuggingFace model ID
MAX_LENGTH    = 128                    # max tokens per message
BATCH_SIZE    = 4                   # reduce to 4 if RAM < 4GB
EPOCHS        = 3                      # 3 is enough for SMS data
LEARNING_RATE = 2e-5                   # standard for fine-tuning
WARMUP_STEPS  = 100
WEIGHT_DECAY  = 0.01

# ── Labels ─────────────────────────────────────────
LABELS        = ["ham", "spam"]        # index 0=ham, index 1=spam
NUM_LABELS    = 2

# ── Paths ──────────────────────────────────────────
# Use absolute paths to avoid "not found" errors
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH  = os.path.join(BASE_DIR, "dataset.csv")
SAVE_DIR      = os.path.join(BASE_DIR, "roberta", "saved_model")
CHECKPOINT_DIR = os.path.join(BASE_DIR, "roberta", "checkpoints")

# ── Training ───────────────────────────────────────
EVAL_STRATEGY = "epoch"               # evaluate after each epoch
TEST_SIZE     = 0.2                   # 80/20 train/test split
RANDOM_SEED   = 42

# ── Inference ──────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.5            # above this = spam
MODEL_VERSION = "roberta-base-finetuned-v1"