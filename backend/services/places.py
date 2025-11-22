import requests
from typing import List, Dict

# Copenhagen bounding box (approximate)
import json
import os
import time

# Copenhagen bounding box (expanded)
COPENHAGEN_BBOX = {
    "south": 55.60,
    "west": 12.42,
    "north": 55.75,
    "east": 12.68
}

CACHE_FILE = "cafes_cache.json"
CACHE_DURATION = 24 * 60 * 60  # 24 hours

def get_cafes() -> List[Dict]:
    """
    Fetch cafe locations in Copenhagen using Overpass API (OSM).
    Returns a list of cafes with their coordinates and names.
    Uses local caching to avoid hitting API rate limits.
    """
    # Check cache first
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cache_data = json.load(f)
                if time.time() - cache_data["timestamp"] < CACHE_DURATION:
                    print("Using cached cafe data")
                    return cache_data["cafes"]
        except Exception as e:
            print(f"Cache read error: {e}")

    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Expanded Overpass QL query
    # Includes cafes, bakeries, ice cream shops, and restaurants/bars/fast_food
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"~"cafe|bar|restaurant|fast_food|ice_cream"]({COPENHAGEN_BBOX['south']},{COPENHAGEN_BBOX['west']},{COPENHAGEN_BBOX['north']},{COPENHAGEN_BBOX['east']});
      way["amenity"~"cafe|bar|restaurant|fast_food|ice_cream"]({COPENHAGEN_BBOX['south']},{COPENHAGEN_BBOX['west']},{COPENHAGEN_BBOX['north']},{COPENHAGEN_BBOX['east']});
      node["shop"="bakery"]({COPENHAGEN_BBOX['south']},{COPENHAGEN_BBOX['west']},{COPENHAGEN_BBOX['north']},{COPENHAGEN_BBOX['east']});
      way["shop"="bakery"]({COPENHAGEN_BBOX['south']},{COPENHAGEN_BBOX['west']},{COPENHAGEN_BBOX['north']},{COPENHAGEN_BBOX['east']});
    );
    out center;
    """
    
    try:
        print("Fetching fresh cafe data from Overpass API...")
        response = requests.post(overpass_url, data={"data": query}, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        cafes = []
        for element in data.get("elements", []):
            # Get coordinates
            if element.get("type") == "node":
                lat = element.get("lat")
                lon = element.get("lon")
            elif element.get("type") == "way" and "center" in element:
                lat = element["center"].get("lat")
                lon = element["center"].get("lon")
            else:
                continue
            
            # Get name and type
            tags = element.get("tags", {})
            name = tags.get("name", "Unnamed Place")
            amenity = tags.get("amenity", tags.get("shop", "unknown"))
            
            cafes.append({
                "id": element.get("id"),
                "name": name,
                "lat": lat,
                "lon": lon,
                "type": "competitor",
                "amenity": amenity
            })
        
        # Save to cache
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump({
                    "timestamp": time.time(),
                    "cafes": cafes
                }, f)
        except Exception as e:
            print(f"Cache write error: {e}")
            
        return cafes
    except Exception as e:
        print(f"Error fetching cafes: {e}")
        # Try to return stale cache if available
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    return json.load(f)["cafes"]
            except:
                pass
        return [{"error": str(e)}]
