from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import re
import time
import uvicorn
from ocr_engine import PhishLensOCR
from classifier import PhishLensClassifier
from config import URGENCY_CUES, FINANCIAL_CUES, AUTHORITY_CUES, WEIGHTS

app = FastAPI(title="PhishLens AI ML Service")
ocr = PhishLensOCR()
classifier = PhishLensClassifier()

class DetectionResult(BaseModel):
    risk_score: float
    risk_level: str
    detected_cues: list
    full_text: str
    ml_confidence: float
    processing_time: float

@app.get("/")
def read_root():
    return {
        "status": "ML Service Online",
        "ml_model_ready": classifier.is_ready()
    }

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    start_time = time.time()
    try:
        # 1. Read Image content
        image_content = await file.read()
        
        # 2. OCR Extraction
        full_text, details = ocr.extract_text(image_content)
        if not full_text:
            return {
                "risk_score": 0,
                "risk_level": "Safe",
                "detected_cues": [],
                "full_text": "",
                "ml_confidence": 0,
                "processing_time": time.time() - start_time
            }

        text_lower = full_text.lower()
        
        # 3. Rule-based Detection
        detected_cues = []
        rule_score = 0
        
        for p in URGENCY_CUES:
            if re.search(p, text_lower, re.IGNORECASE):
                detected_cues.append({"type": "Urgency", "cue": p})
                rule_score += WEIGHTS["Urgency"]
        
        for p in FINANCIAL_CUES:
            if re.search(p, text_lower, re.IGNORECASE):
                detected_cues.append({"type": "Financial Bait", "cue": p})
                rule_score += WEIGHTS["Financial Bait"]
                
        for p in AUTHORITY_CUES:
            if re.search(p, text_lower, re.IGNORECASE):
                detected_cues.append({"type": "Authority Spoofing", "cue": p})
                rule_score += WEIGHTS["Authority Spoofing"]

        # 4. ML Model Prediction
        ml_confidence = classifier.predict(full_text)
        ml_score = ml_confidence * 100
        
        # 5. Hybrid Score (Weighted average or Max)
        # We give ML model weight if it's confident, otherwise fallback to rules
        if ml_confidence > 0.7:
            final_score = max(rule_score, ml_score)
        else:
            # If ML isn't confident, rules take precedence but ML still contributes
            final_score = (rule_score * 0.7) + (ml_score * 0.3)

        # Cap score at 100
        final_score = min(final_score, 100)
        
        # Determine Risk Level
        if final_score < 30:
            risk_level = "Safe"
        elif final_score < 60:
            risk_level = "Suspicious"
        else:
            risk_level = "Highly Likely Phishing"
            
        processing_time = time.time() - start_time
        print(f"Analysis completed in {processing_time:.2f}s. Score: {final_score}")

        return {
            "risk_score": round(final_score, 2),
            "risk_level": risk_level,
            "detected_cues": detected_cues,
            "full_text": full_text,
            "ml_confidence": round(ml_confidence, 4),
            "processing_time": round(processing_time, 2)
        }

    except Exception as e:
        print(f"Analysis Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
