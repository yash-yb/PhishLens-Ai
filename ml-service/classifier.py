import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from config import MODEL_PATH, VECTORIZER_PATH

class PhishLensClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self._load_model()

    def _load_model(self):
        """Load the model and vectorizer from disk if they exist."""
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                self.vectorizer = joblib.load(VECTORIZER_PATH)
                print("ML Model loaded successfully.")
            except Exception as e:
                print(f"Error loading ML model: {e}")
        else:
            print("ML Model files not found. Please run train_model.py first.")

    def predict(self, text):
        """
        Predict the risk score based on the text content.
        Returns a probability score (0 to 1).
        """
        if self.model is None or self.vectorizer is None:
            return 0.0  # Fallback to 0 if model is not loaded
        
        try:
            # Transform text using the loaded vectorizer
            text_vec = self.vectorizer.transform([text.lower()])
            # Get probability of the 'phishing' class (assuming class 1 is phishing)
            # Some models might return probability for each class
            probs = self.model.predict_proba(text_vec)[0]
            # Assuming classes are [0, 1] where 1 is phishing
            return float(probs[1])
        except Exception as e:
            print(f"Prediction Error: {e}")
            return 0.0

    def is_ready(self):
        return self.model is not None and self.vectorizer is not None
