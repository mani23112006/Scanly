from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

model = RobertaForSequenceClassification.from_pretrained("ml/roberta/saved_model")
tokenizer = RobertaTokenizer.from_pretrained("ml/roberta/saved_model")

model.eval()

messages = [
    "Your account is blocked. Share OTP urgently. Click http://bit.ly/free",
    "Hey, are we still on for dinner at 7pm?",
    "Congratulations! You won a lottery prize of Rs 50000. Claim now!",
]

for msg in messages:
    inputs = tokenizer(
        msg,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]

    spam_prob = float(probs[1])
    label = "SPAM" if spam_prob > 0.5 else "HAM"

    print(f"{label} ({spam_prob:.2%}) - {msg}")