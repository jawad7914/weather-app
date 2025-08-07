from flask import request, jsonify
import requests

API_KEY = "P29G9XPA2WRRNFYRQSB94GARS"

def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={API_KEY}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            current = data["currentConditions"]
            weather_data = {
                "resolvedAddress": data["resolvedAddress"],
                "timezone": data["timezone"],
                "datetime": current["datetime"],
                "temperature": f"{current['temp']}°F",
                "temperature_celsius": f"{int((current['temp'] - 32) * 5 / 9)}°C",
                "humidity": f"{current['humidity']}%",
                "windspeed": f"{current['windspeed']}mph",
                "conditions": current["conditions"]
            }
            return jsonify(weather_data), 200
        else:
            return jsonify({"error": "Invalid city or API call failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
