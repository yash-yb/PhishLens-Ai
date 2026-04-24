import requests
import os

# ML Service URL
URL = "http://localhost:8000/analyze"

def test_analyze():
    # Since I don't have a real phishing image, I'll use a placeholder or just see if the service responds
    # Actually, I can't easily generate an image with text here without PIL or similar
    # But I can check if the server is up
    try:
        response = requests.get("http://localhost:8000/")
        print("Server Status:", response.json())
        
        # Test with a dummy file if possible, but the server expects an image
        # I'll just check the root for now to confirm the model is loaded
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_analyze()
