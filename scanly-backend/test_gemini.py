from services.gemini_service import generate_explanation


test_data = {
    "scan_type": "text",
    "category": "Scam",
    "score": 92,
    "reasons": [
        "Urgent language detected",
        "Suspicious link detected",
        "Prize or reward claim detected"
    ],
    "original_input": (
        "Congratulations! You have won Rs 50,000. "
        "Claim your prize immediately by clicking the link."
    )
}


result = generate_explanation(test_data)

print("\nGemini Explanation:")
print(result)