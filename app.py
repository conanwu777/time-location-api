from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
from timezonefinder import TimezoneFinder

import pytz
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session support
tf = TimezoneFinder()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/location", methods=["POST"])
def receive_location():
    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")

    print(f"Received lat/lng: {lat}, {lng}")

    try:
        # ✅ Create geolocator here
        geolocator = Nominatim(user_agent="psy-location")
        location = geolocator.reverse((lat, lng), language='en').raw

        address = location.get("address", {})
        city = address.get("city") or address.get("town") or address.get("village")
        country = address.get("country")

        timezone = tf.timezone_at(lat=lat, lng=lng) or "UTC"

        result = {
            "lat": lat,
            "lng": lng,
            "city": city,
            "country": country,
            "timezone": timezone
        }

        session["location"] = result
        return jsonify(result)

    except Exception as e:
        print("Error in /api/location:", e)
        return jsonify({"error": "Failed to resolve location"}), 500

@app.route("/api/location", methods=["GET"])
def get_location():
    location = session.get("location")
    if location:
        return jsonify(location)
    else:
        return jsonify({"error": "No location stored in session"}), 404

@app.route("/api/time", methods=["GET"])
def get_time():
    # Retrieve timezone from session if available, otherwise default to UTC
    timezone = session.get("location", {}).get("timezone", "UTC")

    try:
        now = datetime.now(pytz.timezone(timezone))
    except Exception as e:
        print("Invalid timezone, falling back to UTC:", e)
        now = datetime.utcnow()
        timezone = "UTC"

    return jsonify({
        "timestamp": now.isoformat(),
        "timezone": timezone
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
