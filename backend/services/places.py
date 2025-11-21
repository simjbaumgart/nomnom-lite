import requests
from typing import List, Dict

# Copenhagen bounding box (approximate)
COPENHAGEN_BBOX = {
    "south": 55.615,
    "west": 12.45,
    "north": 55.73,
    "east": 12.65
}

def get_cafes() -> List[Dict]:
    """
    Fetch cafe locations in Copenhagen using Overpass API (OSM).
    Returns a list of cafes with their coordinates and names.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Overpass QL query for cafes in Copenhagen
    query = f"""
    [out:json];
    (
      node["amenity"="cafe"]({COPENHAGEN_BBOX['south']},{COPENHAGEN_BBOX['west']},{COPENHAGEN_BBOX['north']},{COPENHAGEN_BBOX['east']});
      way["amenity"="cafe"]({COPENHAGEN_BBOX['south']},{COPENHAGEN_BBOX['west']},{COPENHAGEN_BBOX['north']},{COPENHAGEN_BBOX['east']});
    );
    out center;
    """
    
    try:
        response = requests.post(overpass_url, data={"data": query}, timeout=30)
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
            
            # Get name
            name = element.get("tags", {}).get("name", "Unnamed Cafe")
            
            cafes.append({
                "id": element.get("id"),
                "name": name,
                "lat": lat,
                "lon": lon,
                "type": "competitor"
            })
        
        return cafes
    except Exception as e:
        return [{"error": str(e)}]
