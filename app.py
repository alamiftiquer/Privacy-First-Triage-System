import sqlite3
import uuid
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob

app = Flask(__name__)
CORS(app)  # Enables the frontend to talk to this backend

# --- DATABASE SETUP ---
# This creates a local file 'tickets.db' to store data
def init_db():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            email TEXT,
            description TEXT,
            sentiment TEXT,
            score REAL,
            tags TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB immediately when app starts
init_db()

# --- LOCAL AI ENGINE ---
def analyze_local_ai(text):
    blob = TextBlob(text)
    # Polarity is a float between -1.0 (Negative) and 1.0 (Positive)
    polarity = blob.sentiment.polarity
    
    if polarity < -0.1:
        sentiment = "negative"
    elif polarity > 0.1:
        sentiment = "positive"
    else:
        sentiment = "neutral"
        
    # Extract Noun Phrases (Simple Keyphrase Extraction)
    tags = list(blob.noun_phrases)
    
    return sentiment, polarity, tags

# --- API 1: CREATE TICKET ---
@app.route('/api/create_ticket', methods=['POST'])
def create_ticket():
    data = request.json
    email = data.get('email')
    description = data.get('description')

    if not email or not description:
        return jsonify({"error": "Missing fields"}), 400

    # 1. Run AI Analysis locally
    sentiment, score, tags = analyze_local_ai(description)

    # 2. Save to SQLite
    ticket_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute('INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?)', 
              (ticket_id, email, description, sentiment, score, ",".join(tags), timestamp))
    conn.commit()
    conn.close()

    print(f"✅ Ticket Created: {sentiment} ({score})") # Log to terminal

    return jsonify({
        "message": "Ticket created successfully",
        "id": ticket_id,
        "sentiment": sentiment,
        "tags": tags
    }), 201

# --- API 2: GET TICKETS ---
@app.route('/api/get_tickets', methods=['GET'])
def get_tickets():
    conn = sqlite3.connect('tickets.db')
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    c = conn.cursor()
    c.execute('SELECT * FROM tickets ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "email": row["email"],
            "description": row["description"],
            "sentiment": row["sentiment"],
            "tags": row["tags"].split(",") if row["tags"] else [],
            "timestamp": row["timestamp"]
        })

    return jsonify(results), 200

if __name__ == '__main__':
    print("🚀 Local AI Server running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)