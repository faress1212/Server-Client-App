from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

messages = []

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    room_id = data.get('room_id', '').strip()
    sender  = data.get('sender', '').strip()
    content = data.get('content', '').strip()
    if not room_id or not sender or not content:
        return jsonify({'error': 'missing fields'}), 400
    msg = {
        'id': len(messages) + 1,
        'room_id': room_id,
        'sender': sender,
        'content': content,
        'timestamp': datetime.utcnow().isoformat()
    }
    messages.append(msg)
    return jsonify({'status': 'sent'}), 201

@app.route('/messages/<room_id>', methods=['GET'])
def get_messages(room_id):
    room_msgs = [m for m in messages if m['room_id'] == room_id]
    return jsonify(room_msgs), 200

@app.route('/new-room', methods=['GET'])
def new_room():
    return jsonify({'room_id': str(uuid.uuid4())[:8]}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)