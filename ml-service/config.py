import re

# OCR Configuration
MAX_IMAGE_DIMENSION = 1024  # Max width or height to prevent slow OCR
EASYOCR_GPU = False        # Set to True if GPU is available

# Detection Rules (Regex Patterns)
URGENCY_CUES = [
    r"urgent", r"immediately", r"within 24 hours", 
    r"account blocked", r"last chance", r"expires soon",
    r"action required"
]

FINANCIAL_CUES = [
    r"cashback", r"lottery", r"winner", r"₹[0-9,]+", 
    r"bonus", r"claimed", r"reward", r"refund"
]

AUTHORITY_CUES = [
    r"sbi", r"phonepe", r"government", r"official", 
    r"bank support", r"kyc", r"income tax", r"police"
]

# Risk Score Weights
WEIGHTS = {
    "Urgency": 25,
    "Financial Bait": 20,
    "Authority Spoofing": 15
}

# ML Model Configuration
MODEL_PATH = "models/phish_model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"
