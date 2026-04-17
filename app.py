from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import uuid
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_PATH = 'messages.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    room_id = data.get('room_id', '').strip()
    sender  = data.get('sender', '').strip()
    content = data.get('content', '').strip()
    if not room_id or not sender or not content:
        return jsonify({'error': 'missing fields'}), 400
    timestamp = datetime.utcnow().isoformat()
    conn = get_db()
    conn.execute('INSERT INTO messages (room_id, sender, content, timestamp) VALUES (?, ?, ?, ?)',
                 (room_id, sender, content, timestamp))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sent', 'timestamp': timestamp}), 201

@app.route('/messages/<room_id>', methods=['GET'])
def get_messages(room_id):
    after = request.args.get('after')
    conn = get_db()
    if after:
        rows = conn.execute('SELECT * FROM messages WHERE room_id = ? AND timestamp > ? ORDER BY id ASC', (room_id, after)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM messages WHERE room_id = ? ORDER BY id ASC', (room_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200

@app.route('/new-room', methods=['GET'])
def new_room():
    return jsonify({'room_id': str(uuid.uuid4())[:8]}), 200

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)