# PhishLens AI: Explainable Phishing Detection

This repository contains the technical prototype for **PhishLens AI**, a system designed to detect phishing in WhatsApp images using OCR and ML.

## 🚀 Getting Started

The project is split into three main components:

### 1. ML Inference Service (Python)
Provides OCR extraction and phishing risk analysis.
- **Path:** `ml-service/`
- **Port:** 8000
- **Commands:**
  ```bash
  cd ml-service
  source venv/bin/activate
  python main.py
  ```

### 2. API Gateway (Node.js)
Orchestrates file uploads to Supabase and manages communications.
- **Path:** `backend-gateway/`
- **Port:** 5000
- **Commands:**
  ```bash
  cd backend-gateway
  npm start # or node index.js
  ```

### 3. Web Frontend (React)
Premium Glassmorphism dashboard for users.
- **Path:** `web-frontend/`
- **Port:** 5173
- **Commands:**
  ```bash
  cd web-frontend
  npm run dev
  ```

## 🛠️ Architecture
- **Frontend:** React + Tailwind CSS + Framer Motion
- **Gateway:** Node.js + Express + Multer
- **ML Engine:** FastAPI + EasyOCR + OpenCV
- **Database:** Supabase (Auth, Storage, Database)

## 🏗️ Environment Setup
Ensure you have the following keys in `backend-gateway/.env`:
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `ML_SERVICE_URL` (defaults to http://localhost:8000)

---
*Developed as a technical prototype for image-based social engineering mitigation.*
