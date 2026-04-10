import cv2
import easyocr
import numpy as np

class PhishLensOCR:
    def __init__(self):
        # Initialize EasyOCR with English
        self.reader = easyocr.Reader(['en'], gpu=False) # GPU False for compatibility in prototype

    def preprocess_image(self, image_bytes):
        """
        Preprocess image to improve OCR accuracy
        """
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 1. Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 2. Denoising
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 3. Adaptive Thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh

    def extract_text(self, image_bytes):
        """
        Extract text and bounding boxes from image
        """
        processed_img = self.preprocess_image(image_bytes)
        
        # EasyOCR can take numpy array directly
        results = self.reader.readtext(processed_img)
        
        # Format results: list of {text, box, confidence}
        extracted = []
        full_text = ""
        for (bbox, text, prob) in results:
            extracted.append({
                "text": text,
                "box": [list(map(int, point)) for point in bbox],
                "confidence": float(prob)
            })
            full_text += text + " "
            
        return full_text.strip(), extracted
