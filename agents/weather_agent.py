import requests

def get_weather():
    try:
        # Using free API (no key needed for demo)
        url = "https://api.open-meteo.com/v1/forecast?latitude=12.97&longitude=77.59&current_weather=true"
        res = requests.get(url)
        data = res.json()

        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]

        return f"Temperature: {temp}°C, Wind Speed: {wind} km/h"

    except:
        return "Weather data unavailable"