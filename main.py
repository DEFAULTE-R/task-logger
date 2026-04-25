from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import src.database as db
from src.exporter import export_dataset

app = Flask(__name__)
db.init_db()

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/api/stats')
def stats():
    return jsonify(db.get_stats())

@app.route('/api/sessions')
def sessions():
    return jsonify({"sessions": db.get_sessions()})

@app.route('/api/actions')
def actions():
    session_id = request.args.get('session_id')
    limit = int(request.args.get('limit', 100))
    return jsonify({"actions": db.get_actions(session_id=session_id, limit=limit)})

@app.route('/api/actions/<int:action_id>/approve', methods=['POST'])
def approve(action_id):
    data = request.json
    label = data.get('label', 'approved')
    db.approve_action(action_id, label)
    return jsonify({"ok": True})

@app.route('/api/export', methods=['POST'])
def export():
    session_id = request.args.get('session_id')
    file, count = export_dataset(session_id=session_id)
    return jsonify({"ok": True, "file": file, "count": count})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
