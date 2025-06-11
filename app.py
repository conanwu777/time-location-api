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
    x_forwarded_for = request.headers.get("X-Forwarded-For", request.remote_addr)
    ip_list = [ip.strip() for ip in x_forwarded_for.split(",")]

    # Filter out private or internal IPs
    public_ip = next((ip for ip in ip_list if not ip.startswith("10.") and not ip.startswith("172.") and not ip.startswith("192.168.")), request.remote_addr)

    try:
        ip_data = requests.get(f"http://ip-api.com/json/{public_ip}").json()
        print(f"Using IP: {public_ip}")
        print("IP-API response:", ip_data)

        city = ip_data.get("city")
        country = ip_data.get("country")

    except Exception as e:
        print(f"Failed to fetch IP data: {e}")
        city = country = None

    return jsonify({
        "ip": public_ip,
        "city": city,
        "country": country
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
