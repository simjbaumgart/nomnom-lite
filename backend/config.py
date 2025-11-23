"""
Configuration for supported cities in NomNom Lite.
"""

CITIES = {
    "copenhagen": {
        "name": "Copenhagen",
        "coords": {"lat": 55.6761, "lon": 12.5683},
        "bbox": {
            "south": 55.60,
            "west": 12.42,
            "north": 55.75,
            "east": 12.68
        },
        "default_zoom": 13
    },
    "ghent": {
        "name": "Ghent",
        "coords": {"lat": 51.0543, "lon": 3.7174},
        "bbox": {
            "south": 51.01,
            "west": 3.66,
            "north": 51.09,
            "east": 3.78
        },
        "default_zoom": 14
    }
}

DEFAULT_CITY_ID = "copenhagen"
