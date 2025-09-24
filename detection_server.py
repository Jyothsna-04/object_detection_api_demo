# detection_server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/detections', methods=['POST'])
def detections():
    data = request.get_json()
    print("✅ DETECTION:", data)
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(port=5004)
