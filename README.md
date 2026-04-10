# PhishLens AI: Explainable Phishing Detection for WhatsApp

PhishLens AI is a specialized security prototype designed to identify and explain phishing threats within images—such as screenshots of scam messages, forwarded posters, and fake authority alerts—using OCR and Machine Learning.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Node.js** (v18.0 or higher) & **npm**
- **Python** (v3.9 or higher) & **pip**
- **Git**

---

## 🚀 Step 1: Clone and Project Setup

```bash
git clone <your-repository-url>
cd PhishLens-Ai
```

---

## 🐍 Step 2: ML Inference Service Setup (Python)

This service handles the heavy lifting: Image preprocessing, OCR extraction, and risk analysis.

1. Navigate to the ML service directory:
   ```bash
   cd ml-service
   ```
2. Create and activate a Virtual Environment:
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On macOS/Linux: source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn easyocr scikit-learn pandas requests python-multipart opencv-python-headless
   ```
   *Note: The first time you run the service, it will download ~100MB of OCR model weights.*

---

## 🌐 Step 3: API Gateway Setup (Node.js)

The gateway manages communications between the frontend and the ML service.

1. Navigate to the gateway directory:
   ```bash
   cd ../backend-gateway
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. (Optional) Configure Supabase:
   If you wish to persist scans, create a `.env` file based on the template:
   ```env
   PORT=5000
   SUPABASE_URL=your_url
   SUPABASE_ANON_KEY=your_key
   ML_SERVICE_URL=http://localhost:8000
   ```

---

## 🎨 Step 4: Web Frontend Setup (React)

The premium dashboard for user interaction.

1. Navigate to the frontend directory:
   ```bash
   cd ../web-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

---

## 🏃‍♂️ How to Run the Project

You need to run all three components simultaneously in separate terminal windows:

### Terminal 1: ML Service
```bash
cd ml-service
source venv/bin/activate # or venv\Scripts\activate
python main.py
```

### Terminal 2: API Gateway
```bash
cd backend-gateway
npm start
```

### Terminal 3: Web Frontend
```bash
cd web-frontend
npm run dev
```

The application will be accessible at: **[http://localhost:5173](http://localhost:5173)**

---

## 🛠️ Technical Architecture

- **Frontend**: React + Tailwind CSS + Framer Motion (Glassmorphism UI)
- **Middleware**: Node.js Proxy (Bypasses external DB for local prototype mode)
- **Engine**: FastAPI + EasyOCR + Rule-based Hybrid Detection
- **Explainability**: Maps detection triggers to specific "Cues" (Urgency, Financial, Authority) for user transparency.

---

## 💡 Troubleshooting
- **OCR Errors**: Ensure you have a stable internet connection for the first run so Python can download the `english` OCR models.
- **Port Conflicts**: If port 5000 or 8000 is in use, you can change them in `backend-gateway/index.js` and `ml-service/main.py` respectively.
