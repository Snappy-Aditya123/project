from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = "api_database.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        action TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                      )''')
    conn.commit()
    conn.close()

# API: Register User
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"error": "Username and email are required."}), 400

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
        conn.commit()
        return jsonify({"message": "User registered successfully.", "user_id": cursor.lastrowid}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

# API: Log Action
@app.route('/log', methods=['POST'])
def log_action():
    data = request.json
    user_id = data.get("user_id")
    action = data.get("action")

    if not user_id or not action:
        return jsonify({"error": "User ID and action are required."}), 400

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (user_id, action) VALUES (?, ?)", (user_id, action))
        conn.commit()
        return jsonify({"message": "Action logged successfully."}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

# API: Get Logs for a User
@app.route('/logs/<int:user_id>', methods=['GET'])
def get_logs(user_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
        logs = cursor.fetchall()
        return jsonify({"logs": logs}), 200
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()  # Initialize the database tables
    app.run(debug=True)
