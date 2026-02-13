# Privacy-First AI Incident Triage System

## 📌 Project Overview
A secure, localized IT support ticketing system that uses **Edge AI** to prioritize urgent incidents. Unlike traditional cloud solutions, this application performs **Sentiment Analysis** and **Data Storage** entirely on the local server, ensuring 100% data privacy and compliance with data residency laws.

## 🚀 Key Features
* **Privacy-First Architecture:** No data is sent to external cloud APIs.
* **Local NLP Engine:** Uses `TextBlob` for offline sentiment analysis.
* **Automated Triage:** Instantly flags "Negative" sentiment tickets for urgent review.
* **Zero Latency:** Real-time processing on the edge.

## 🛠️ Tech Stack
* **Backend:** Python (Flask)
* **AI/ML:** TextBlob (Natural Language Processing)
* **Database:** SQLite (Embedded)
* **Frontend:** HTML5, CSS3, JavaScript

## ⚙️ How to Run Locally
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    python -m textblob.download_corpora
    ```
3.  Start the server:
    ```bash
    python app.py
    ```
4.  Open `frontend/index.html` in your browser.
