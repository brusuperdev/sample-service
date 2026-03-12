from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "service": "sample-service",
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "hostname": socket.gethostname(),
        "status": "healthy"
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
