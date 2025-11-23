import requests
from typing import List, Dict
import json
import os
import time
from ..config import CITIES, DEFAULT_CITY_ID

CACHE_FILE_PREFIX = "cafes_cache_"
CACHE_DURATION = 24 * 60 * 60  # 24 hours

def get_cafes(city_id: str = DEFAULT_CITY_ID) -> List[Dict]:
    """
    Fetch cafe locations for a specific city using Overpass API (OSM).
    Returns a list of cafes with their coordinates and names.
    Uses local caching to avoid hitting API rate limits.
    """
    if city_id not in CITIES:
        return [{"error": f"Invalid city_id: {city_id}"}]
        
    city_config = CITIES[city_id]
    bbox = city_config['bbox']
    cache_file = f"{CACHE_FILE_PREFIX}{city_id}.json"

    # Check cache first
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                cache_data = json.load(f)
                if time.time() - cache_data["timestamp"] < CACHE_DURATION:
                    print(f"Using cached cafe data for {city_id}")
                    return cache_data["cafes"]
        except Exception as e:
            print(f"Cache read error: {e}")

    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Expanded Overpass QL query
    # Strictly coffee-centric: Cafes and Bakeries only.
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="cafe"]({bbox['south']},{bbox['west']},{bbox['north']},{bbox['east']});
      way["amenity"="cafe"]({bbox['south']},{bbox['west']},{bbox['north']},{bbox['east']});
      node["shop"="bakery"]({bbox['south']},{bbox['west']},{bbox['north']},{bbox['east']});
      way["shop"="bakery"]({bbox['south']},{bbox['west']},{bbox['north']},{bbox['east']});
    );
    out center;
    """
    
    try:
        print(f"Fetching fresh cafe data for {city_id} from Overpass API...")
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
            with open(cache_file, "w") as f:
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
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    return json.load(f)["cafes"]
            except:
                pass
        return [{"error": str(e)}]
