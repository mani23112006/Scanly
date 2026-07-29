from ml.roberta.predict import predict, get_model_status

print("Testing predict.py...")

tests = [
    "Your account is blocked. Share OTP urgently. Click http://bit.ly/free",
    "Hey, are we still on for dinner tonight?",
    "Congratulations! You won Rs 50000 lottery prize. Claim free money now!",
    "Can you send the project report by tomorrow?",
    "Verify account now or it will be suspended. OTP: 4829"
]

for msg in tests:
    result = predict(msg)

    icon = "🔴" if result["label"] == "spam" else "🟢"

    print(
        f"{icon} {result['label'].upper()} "
        f"({result['probability']:.2%}) "
        f"[{result['inference_ms']}ms] — "
        f"{msg[:45]}..."
    )

print()
print("Status:", get_model_status())