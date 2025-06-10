from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Time & Location API is running."

@app.route("/api/time-location", methods=["GET"])
def time_location():
    ip_data = requests.get("http://ip-api.com/json/").json()
    timestamp = datetime.utcnow().isoformat()
    return jsonify({
        "timestamp": timestamp,
        "city": ip_data.get("city"),
        "region": ip_data.get("regionName"),
        "country": ip_data.get("country"),
        "timezone": ip_data.get("timezone")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
