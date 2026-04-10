from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import re
from ocr_engine import PhishLensOCR
import uvicorn
import requests
from io import BytesIO

app = FastAPI(title="PhishLens AI ML Service")
ocr = PhishLensOCR()

class AnalyzeRequest(BaseModel):
    image_url: str

class DetectionResult(BaseModel):
    risk_score: float
    risk_level: str
    detected_cues: list
    full_text: str

# Detection Rules (Phishing Cues)
URGENCY_CUES = [r"urgent", r"immediately", r"within 24 hours", r"account blocked", r"last chance"]
FINANCIAL_CUES = [r"cashback", r"lottery", r"winner", r"₹[0-9,]+", r"bonus", r"claimed"]
AUTHORITY_CUES = [r"sbi", r"phonepe", r"government", r"official", r"bank support", r"kyc"]

@app.get("/")
def read_root():
    return {"status": "ML Service Online"}

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        # 1. Read Image content
        image_content = await file.read()
        
        # 2. OCR Extraction
        full_text, details = ocr.extract_text(image_content)
        text_lower = full_text.lower()
        
        # 3. Hybrid Detection (Rule-based for now)
        detected_cues = []
        score = 0
        
        for p in URGENCY_CUES:
            if re.search(p, text_lower):
                detected_cues.append({"type": "Urgency", "cue": p.replace(r"r'", "").replace("'", "")})
                score += 25
        
        for p in FINANCIAL_CUES:
            if re.search(p, text_lower):
                detected_cues.append({"type": "Financial Bait", "cue": p})
                score += 20
                
        for p in AUTHORITY_CUES:
            if re.search(p, text_lower):
                detected_cues.append({"type": "Authority Spoofing", "cue": p})
                score += 15

        # Cap score at 100
        score = min(score, 100)
        
        # Determine Risk Level
        if score < 20:
            risk_level = "Safe"
        elif score < 50:
            risk_level = "Suspicious"
        else:
            risk_level = "Highly Likely Phishing"
            
        return {
            "risk_score": score,
            "risk_level": risk_level,
            "detected_cues": detected_cues,
            "full_text": full_text
        }

    except Exception as e:
        print(f"Analysis Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
