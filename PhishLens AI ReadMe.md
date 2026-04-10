# **PhishLens AI: Explainable Phishing Detection for WhatsApp Images**

PhishLens AI is a specialized, explainable AI-driven prototype designed to identify and mitigate phishing threats embedded in WhatsApp-shared images. Unlike traditional URL-based detectors, this system focuses on the semantic and visual cues within screenshots, forwarded alerts, and scam posters.

## **🚀 Key Features**

* **Multimodal Analysis:** Combines OCR-driven text extraction with semantic feature analysis.  
* **Explainable AI (XAI):** Not only flags a risk but provides the specific reasoning (cues) behind the detection.  
* **Risk Scoring:** Quantitative assessment of phishing probability (Safe, Suspicious, Highly Likely).  
* **Actionable Safety Tips:** Real-time recommendations to prevent financial or data loss.

## **🏗️ Technical Pipeline**

The system operates through a 5-step modular pipeline:

1. **Image Upload & Preprocessing:** Handles WhatsApp images (often compressed) and optimizes them for character recognition using grayscale conversion and noise reduction.  
2. **OCR Module (Extraction):** Utilizes **Tesseract OCR** or **EasyOCR** to convert visual text into machine-readable strings.  
3. **Detection Module (Classification):** A hybrid engine that uses **scikit-learn** models and rule-based logic to search for:  
   * **Urgency Cues:** Keywords like "Immediate action," "Account blocked," or "Last chance."  
   * **Financial Bait:** Keywords like "Cashback," "Lottery," "₹50,000," or "Bonus."  
   * **Authority Spoofing:** Identifying fake references to "SBI," "PhonePe," or "Govt."  
4. **Explainability Layer:** Maps the detection results back to specific "Suspicious Cues," informing the user which words or patterns triggered the alert.  
5. **Recommendation Engine:** Outputs tailored safety advice based on the detected phishing type (e.g., "Do not scan this QR," "Do not share OTP").

## **💻 Tech Stack**

| Layer | Technology |
| :---- | :---- |
| **Frontend** | HTML5 / CSS3 / JavaScript (or React) |
| **Backend** | Python \+ Flask |
| **OCR Engine** | Tesseract OCR / EasyOCR |
| **Machine Learning** | Scikit-learn (Support Vector Machines or Random Forest) |
| **Database** | SQLite / Firebase (Optional) |

## **💡 Technical Highlights for Research & Reporting**

To assist in the creation of the **Technical Report** and **Research Paper**, the following points should be emphasized:

### **1\. The Research Gap**

Most current security systems target **URL-based** phishing or **Email** headers. There is a significant gap in protecting users from **Image-based Social Engineering** on Instant Messaging (IM) platforms like WhatsApp. PhishLens AI fills this by analyzing the *intent* of the message within an image.

### **2\. Innovation: The Explainability Layer**

Traditional AI models are often "black boxes." Our implementation focuses on **Transparency**. By highlighting the exact cues that triggered a "Highly Likely Phishing" status, we increase user trust and educational awareness.

### **3\. Future Scope for Integration**

While currently a Web Prototype, the backend architecture is built to support:

* **WhatsApp Bot Integration:** Real-time analysis of forwarded messages.  
* **Android Accessibility Service:** Scanning images as they appear in the gallery.  
* **Deep Learning Upgrades:** Transitioning to Vision Transformers (ViT) for better logo detection and visual spoofing analysis.

## **🛠️ Setup & Installation**

*Note: Ensure you have Python 3.8+ installed.*

1. **Clone the repository:**  
   git clone \[repository-url\]

2. **Install Dependencies:**  
   pip install flask flask-cors scikit-learn pytesseract easyocr

3. **Configure OCR Engine:**  
   Ensure Tesseract-OCR is installed on your system path.  
4. **Run the Server:**  
   python app.py  
