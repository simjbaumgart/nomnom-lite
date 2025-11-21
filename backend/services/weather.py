import requests
from typing import Dict

# Copenhagen coordinates
COPENHAGEN_LAT = 55.6761
COPENHAGEN_LON = 12.5683

def get_weather() -> Dict:
    """
    Fetch current weather data for Copenhagen using Open-Meteo API.
    Returns temperature, wind speed, and precipitation probability.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": COPENHAGEN_LAT,
        "longitude": COPENHAGEN_LON,
        "current": "temperature_2m,wind_speed_10m,precipitation",
        "timezone": "Europe/Copenhagen"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        
        return {
            "temperature": current.get("temperature_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "precipitation": current.get("precipitation"),
            "timestamp": current.get("time"),
            "is_suitable": assess_weather_suitability(
                current.get("temperature_2m", 0),
                current.get("wind_speed_10m", 0),
                current.get("precipitation", 0)
            )
        }
    except Exception as e:
        return {"error": str(e)}

def assess_weather_suitability(temp: float, wind: float, precip: float) -> bool:
    """
    Assess if weather is suitable for coffee cart operation.
    Returns True if suitable, False otherwise.
    """
    # Poor conditions: temp < 5°C, wind > 25 km/h, or precipitation > 0.5mm
    if temp < 5 or wind > 25 or precip > 0.5:
        return False
    return True
