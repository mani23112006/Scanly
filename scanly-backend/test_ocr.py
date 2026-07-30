from ocr.extract import extract_text, get_ocr_status
print("Loading image...")

# Optional: OCR status
try:
    print("OCR Status:", get_ocr_status())
except Exception:
    pass

# Read image
with open("test_image.png", "rb") as f:
    image_bytes = f.read()

print(f"Image size: {len(image_bytes) / 1024:.1f} KB")
print("Running OCR...")

# Run OCR
result = extract_text(image_bytes)

print("\n=== OCR RESULT ===")
print(f"Quality: {result['quality']}")
print(f"Confidence: {result['confidence_avg']}")
print(f"Words: {result['word_count']}")
print(f"Time: {result['ocr_ms']} ms")
print(f"Warning: {result['warning']}")

print("\nExtracted text:")
print(result["text"])

print("\nIndividual lines:")
for i, line in enumerate(result["lines"], start=1):
    print(f"{i}. {line}")