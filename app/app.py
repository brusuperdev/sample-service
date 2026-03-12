from flask import Flask, jsonify
import os
import socket

PREFIX = os.getenv("SERVICE_NAME", "sample-service")
app = Flask(__name__)

@app.route("/")
@app.route(f"/{PREFIX}")
@app.route(f"/{PREFIX}/")
def index():
    return jsonify({
        "service": PREFIX,
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "hostname": socket.gethostname(),
        "status": "healthy"
    })

@app.route("/health")
@app.route(f"/{PREFIX}/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
