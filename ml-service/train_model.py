import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from config import MODEL_PATH, VECTORIZER_PATH

def train_baseline_model():
    # 1. Synthetic Dataset (Phishing vs Safe)
    data = [
        # Phishing Examples
        ("Urgent: Your account is blocked. Click here to verify immediately.", 1),
        ("Congratulations! You won a ₹50,000 cashback reward. Claim now.", 1),
        ("SBI Bank: KYC update required within 24 hours to avoid suspension.", 1),
        ("Your PhonePe wallet has received a bonus. Click to accept.", 1),
        ("Final Notice: Your subscription expires today. Pay now to stay active.", 1),
        ("Income Tax Refund: You are eligible for a refund of ₹12,000. Login here.", 1),
        ("Suspected activity on your bank account. Reset your password immediately.", 1),
        
        # Safe Examples
        ("Hey, are we still meeting for lunch today?", 0),
        ("The report for the project is due on Friday afternoon.", 0),
        ("Don't forget to pick up some milk on your way home.", 0),
        ("Welcome to our newsletter! We hope you enjoy the updates.", 0),
        ("Your order has been shipped and will arrive in 3-5 business days.", 0),
        ("Can you send me the link to the meeting notes?", 0),
        ("The weather today is sunny with a high of 25 degrees.", 0),
    ]

    df = pd.DataFrame(data, columns=['text', 'label'])

    # 2. Vectorization (TF-IDF)
    print("Vectorizing text data...")
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    X = vectorizer.fit_transform(df['text'])
    y = df['label']

    # 3. Model Training (Random Forest)
    print("Training Random Forest classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # 4. Save Model and Vectorizer
    models_dir = os.path.dirname(MODEL_PATH)
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"Created directory: {models_dir}")

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Vectorizer saved to {VECTORIZER_PATH}")

if __name__ == "__main__":
    train_baseline_model()
