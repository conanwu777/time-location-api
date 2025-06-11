from flask import Flask, request, jsonify
import requests
from datetime import datetime
import pytz  # or use zoneinfo if you're on 3.9+

app = Flask(__name__)

@app.route("/")
def home():
    return "Time & Location API is running"
    
@app.route("/api/location", methods=["GET"])
def location():
    # Get the client IP, considering proxy headers
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    # Use the IP to get location info
    ip_data = requests.get(f"http://ip-api.com/json/{client_ip}").json()

    return jsonify({
        "ip": client_ip,
        "city": ip_data.get("city"),
        "country": ip_data.get("country")
    })

@app.route("/api/time", methods=["GET"])
def time():
    ip_data = requests.get("http://ip-api.com/json/").json()
    tz_name = ip_data.get("timezone", "UTC")
    local_tz = pytz.timezone(tz_name)
    local_time = datetime.now(local_tz).isoformat()
    
    return jsonify({
        "timestamp": local_time,
        "timezone": tz_name
    })

@app.route("/api/time-location", methods=["GET"])
def time_location():
    ip_data = requests.get("http://ip-api.com/json/").json()
    tz_name = ip_data.get("timezone", "UTC")
    local_tz = pytz.timezone(tz_name)
    local_time = datetime.now(local_tz).isoformat()

    return jsonify({
        "timestamp": local_time,
        "city": ip_data.get("city"),
        "region": ip_data.get("regionName"),
        "country": ip_data.get("country"),
        "timezone": tz_name
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
