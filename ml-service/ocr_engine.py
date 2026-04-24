import cv2
import easyocr
import numpy as np
from config import MAX_IMAGE_DIMENSION, EASYOCR_GPU

class PhishLensOCR:
    def __init__(self):
        # Initialize EasyOCR with English
        self.reader = easyocr.Reader(['en'], gpu=EASYOCR_GPU)

    def preprocess_image(self, image_bytes):
        """
        Preprocess image to improve OCR accuracy and performance
        """
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return None

        # 1. Resize Image if too large (Performance Optimization)
        height, width = img.shape[:2]
        if max(height, width) > MAX_IMAGE_DIMENSION:
            scale = MAX_IMAGE_DIMENSION / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            print(f"Resized image from {width}x{height} to {new_width}x{new_height}")

        # 2. Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 3. Contrast Enhancement (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # 4. Denoising
        denoised = cv2.GaussianBlur(enhanced, (3, 3), 0)
        
        # 5. Adaptive Thresholding
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
        
        if processed_img is None:
            return "", []
            
        # EasyOCR can take numpy array directly
        # Use paragraph=True for faster processing if we don't need word-level precision
        results = self.reader.readtext(processed_img, paragraph=False)
        
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
