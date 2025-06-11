from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import pytz
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session support

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/api/location", methods=["GET"])
def get_location():
    if "location" in session:
        return jsonify(session["location"])

    x_forwarded_for = request.headers.get("X-Forwarded-For", request.remote_addr)
    ip_list = [ip.strip() for ip in x_forwarded_for.split(",")]
    public_ip = next(
        (ip for ip in ip_list if not ip.startswith("10.") and not ip.startswith("172.") and not ip.startswith("192.168.")),
        request.remote_addr
    )

    try:
        ip_data = requests.get(f"http://ip-api.com/json/{public_ip}").json()
        location = {
            "ip": public_ip,
            "city": ip_data.get("city"),
            "country": ip_data.get("country"),
            "timezone": ip_data.get("timezone") or "UTC"
        }
        session["location"] = location
    except Exception as e:
        print(f"Location fetch failed: {e}")
        location = {"ip": public_ip, "city": None, "country": None, "timezone": "UTC"}
        session["location"] = location

    return jsonify(location)

@app.route("/api/time", methods=["GET"])
def get_time():
    location = session.get("location", {})
    timezone = location.get("timezone", "UTC")

    try:
        now = datetime.now(pytz.timezone(timezone))
    except Exception:
        now = datetime.utcnow()

    return jsonify({
        "timestamp": now.isoformat(),
        "timezone": timezone
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
