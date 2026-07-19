# ── SCANLY Rule-Based Engine ──────────────────────
# Pure Python keyword detection with weighted scoring
# No external libraries needed

# Keyword → point value dictionary
# Higher points = stronger scam signal
SCAM_KEYWORDS = {
    # High risk — very rarely in legitimate messages
    "prize":             25,
    "lottery":           20,
    "otp":               20,
    "free money":        20,
    "bank blocked":      20,
    "account suspended": 20,
    "verify account":    20,
    "click here":        20,

    # Medium risk — suspicious but sometimes legit
    "urgent":            15,
    "winner":            15,
    "congratulations":   15,
    "act now":           15,
    "claim now":         15,
    "you have been selected": 15,
    "limited offer":     10,

    # Lower risk — weak signals on their own
    "limited time":      10,
    "dear customer":     10,
    "confirm your":      10,
    "kindly verify":     10,
    "reactivate":        10,
}


def score_rules(text: str) -> dict:
    """
    Scan text for scam keywords and return a score + matched list.

    Args:
        text: the message to analyze

    Returns:
        {
            "score":    int  (0–100),
            "matched":  list (keywords that were found)
        }
    """

    # Convert to lowercase so matching is case-insensitive
    # "OTP", "Otp", "otp" all match the same keyword
    text_lower = text.lower()

    total_score  = 0
    matched_keywords = []

    # Loop through every keyword in our dictionary
    for keyword, points in SCAM_KEYWORDS.items():
        if keyword in text_lower:          # check if keyword exists in text
            total_score += points          # add its points to total
            matched_keywords.append(keyword)  # remember it was matched

    # Cap score at 100 — can't go above maximum
    total_score = min(total_score, 100)

    return {
        "score":   total_score,
        "matched": matched_keywords
    }


