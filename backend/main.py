from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from services.weather import get_weather
from services.places import get_cafes
from services.popular_times import get_popular_times
from services.business_score import calculate_business_score, find_nearest_cafe, calculate_cafe_density, get_density_label
from services.activity_zones import calculate_zone_scores
from services.permit_info import get_permit_status, PERMIT_REGULATIONS
from services.events import get_active_events
from typing import Optional

app = FastAPI(title="NomNom Lite API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Static Files (Frontend)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Mount static files if directory exists (it will after build)
static_dir = "static"
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="assets")



# Expanded hotspots - 30+ areas across Copenhagen
COPENHAGEN_HOTSPOTS = [
    # Tourist Areas
    {"name": "Nyhavn", "lat": 55.6798, "lon": 12.5914, "type": "tourist"},
    {"name": "Strøget", "lat": 55.6788, "lon": 12.5711, "type": "tourist"},
    {"name": "Tivoli Gardens", "lat": 55.6737, "lon": 12.5681, "type": "tourist"},
    {"name": "The Little Mermaid", "lat": 55.6929, "lon": 12.5994, "type": "tourist"},
    {"name": "Amalienborg Palace", "lat": 55.6840, "lon": 12.5930, "type": "tourist"},
    {"name": "Kongens Nytorv", "lat": 55.6803, "lon": 12.5858, "type": "tourist"},
    {"name": "Christiansborg Palace", "lat": 55.6761, "lon": 12.5801, "type": "tourist"},
    {"name": "The Round Tower", "lat": 55.6813, "lon": 12.5755, "type": "tourist"},
    {"name": "Rosenborg Castle", "lat": 55.6858, "lon": 12.5773, "type": "tourist"},
    {"name": "Kastellet", "lat": 55.6914, "lon": 12.5940, "type": "tourist"},
    
    # Transport Hubs
    {"name": "Nørreport Station", "lat": 55.6833, "lon": 12.5717, "type": "transport"},
    {"name": "Copenhagen Central Station", "lat": 55.6726, "lon": 12.5643, "type": "transport"},
    {"name": "Østerport Station", "lat": 55.6924, "lon": 12.5875, "type": "transport"},
    {"name": "Forum Station", "lat": 55.6846, "lon": 12.5438, "type": "transport"},
    {"name": "Christianshavn Metro", "lat": 55.6732, "lon": 12.5916, "type": "transport"},
    
    # Shopping & Business
    {"name": "Fisketorvet Shopping Center", "lat": 55.6661, "lon": 12.5605, "type": "shopping"},
    {"name": "Magasin du Nord", "lat": 55.6796, "lon": 12.5863, "type": "shopping"},
    {"name": "Frederiksberg Centret", "lat": 55.6775, "lon": 12.5302, "type": "shopping"},
    {"name": "Torvehallerne Market", "lat": 55.6828, "lon": 12.5719, "type": "shopping"},
    
    # Parks & Recreation
    {"name": "The King's Garden", "lat": 55.6856, "lon": 12.5787, "type": "park"},
    {"name": "Frederiksberg Gardens", "lat": 55.6753, "lon": 12.5336, "type": "park"},
    {"name": "Fælled Park", "lat": 55.6981, "lon": 12.5631, "type": "park"},
    {"name": "Amager Strandpark", "lat": 55.6550, "lon": 12.6543, "type": "park"},
    
    # Neighborhoods
    {"name": "Nørrebro", "lat": 55.6897, "lon": 12.5531, "type": "neighborhood"},
    {"name": "Vesterbro", "lat": 55.6682, "lon": 12.5510, "type": "neighborhood"},
    {"name": "Østerbro", "lat": 55.7042, "lon": 12.5770, "type": "neighborhood"},
    {"name": "Frederiksberg", "lat": 55.6789, "lon": 12.5342, "type": "neighborhood"},
    {"name": "Christianshavn", "lat": 55.6732, "lon": 12.5943, "type": "neighborhood"},
    {"name": "Islands Brygge", "lat": 55.6651, "lon": 12.5771, "type": "neighborhood"},
    
    # Universities & Cultural
    {"name": "University of Copenhagen", "lat": 55.6794, "lon": 12.5726, "type": "cultural"},
    {"name": "IT University", "lat": 55.6596, "lon": 12.5908, "type": "cultural"},
    {"name": "National Gallery", "lat": 55.6889, "lon": 12.5783, "type": "cultural"},
    
    # Strategic High-Traffic Paths & Low-Competition Areas
    {"name": "Langelinie Promenade", "lat": 55.6919, "lon": 12.5975, "type": "park"},  # Path to Little Mermaid
    {"name": "Islands Brygge Havnebadet", "lat": 55.6635, "lon": 12.5805, "type": "park"},  # Harbor bath, outdoor activity
    {"name": "Superkilen Park", "lat": 55.7006, "lon": 12.5419, "type": "park"},  # Trendy Nørrebro park, less cafes
    {"name": "Assistens Cemetery", "lat": 55.6907, "lon": 12.5526, "type": "park"},  # Popular walking area
    {"name": "Reffen Street Food", "lat": 55.6882, "lon": 12.6032, "type": "shopping"},  # Street food market area
    {"name": "Carlsberg City", "lat": 55.6665, "lon": 12.5397, "type": "neighborhood"},  # New development, less competition
    {"name": "Trianglen", "lat": 55.7007, "lon": 12.5762, "type": "transport"},  # Transport hub, Østerbro connector
    {"name": "Langebro Bridge", "lat": 55.6685, "lon": 12.5738, "type": "neighborhood"},  # Connects islands, foot traffic
    {"name": "Nørrebro Park", "lat": 55.6952, "lon": 12.5509, "type": "park"},  # Large green space, few cafes
    {"name": "Amager Strand Metro", "lat": 55.6578, "lon": 12.6181, "type": "transport"},  # Beach access point
]

@app.get("/")
async def read_root():
    # Serve index.html if it exists (Production)
    if os.path.exists(f"{static_dir}/index.html"):
        return FileResponse(f"{static_dir}/index.html")
    return {"message": "NomNom Lite API", "status": "running"}

@app.get("/api/weather")
def weather():
    """Get current weather data for Copenhagen"""
    return get_weather()

@app.get("/api/cafes")
def cafes():
    """Get cafe locations in Copenhagen"""
    return get_cafes()

@app.get("/api/hotspots")
def hotspots():
    """Get all hotspots with default traffic levels"""
    result = []
    for spot in COPENHAGEN_HOTSPOTS:
        spot_copy = spot.copy()
        spot_copy["traffic_level"] = estimate_traffic(spot["name"], spot["type"])
        result.append(spot_copy)
    return result

@app.get("/api/popular-times/{place_name}")
def popular_times(place_name: str):
    """Get Popular Times data for a specific place"""
    return get_popular_times(place_name, "Copenhagen")

@app.get("/api/hotspots-live")
def hotspots_live():
    """Get hotspots with LIVE busyness data from Google Maps (slow)"""
    result = []
    for spot in COPENHAGEN_HOTSPOTS:
        popular_data = get_popular_times(spot["name"], "Copenhagen")
        spot_copy = spot.copy()
        spot_copy["traffic_level"] = popular_data.get("current_popularity", 50)
        spot_copy["data_available"] = popular_data.get("data_available", False)
        result.append(spot_copy)
    return result

@app.get("/api/events")
def events():
    """Get active events in Copenhagen (cached daily)"""
    return get_active_events()

@app.get("/api/hotspots-scored")
def hotspots_scored(
    min_traffic: Optional[int] = Query(0, ge=0, le=100),
    max_competition_distance: Optional[int] = Query(1000, ge=0, le=5000),
    require_suitable_weather: Optional[bool] = Query(False),
    use_live_data: Optional[bool] = Query(False),
    simulated_hour: Optional[int] = Query(None, ge=0, le=23)
):
    """
    Get hotspots with business scores and filtering options.
    
    Args:
        min_traffic: Minimum traffic level (0-100)
        max_competition_distance: Maximum acceptable distance to nearest cafe (meters)
        require_suitable_weather: Only show spots with suitable weather
        use_live_data: Use live Popular Times data (slow)
    """
    # Get weather data
    weather_data = get_weather()
    weather_suitable = weather_data.get("is_suitable", True)
    
    # Get cafe data for competition analysis
    cafes_data = get_cafes()
    
    # Get active events
    active_events = get_active_events()
    
    result = []
    for spot in COPENHAGEN_HOTSPOTS:
        # Get traffic level
        if use_live_data:
            popular_data = get_popular_times(spot["name"], "Copenhagen")
            traffic_level = popular_data.get("current_popularity", 50)
            data_available = popular_data.get("data_available", False)
        else:
            traffic_level = estimate_traffic(spot["name"], spot["type"], simulated_hour)
            data_available = False
        
        # Calculate Event Boost
        nearby_events = []
        event_boost = 0
        
        from math import radians, sin, cos, sqrt, atan2
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            R = 6371000 # Earth radius in meters
            phi1, phi2 = radians(lat1), radians(lat2)
            dphi = radians(lat2 - lat1)
            dlambda = radians(lon2 - lon1)
            a = sin(dphi/2)**2 + cos(phi1)*cos(phi2) * sin(dlambda/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            return R * c

        for event in active_events:
            dist = calculate_distance(spot["lat"], spot["lon"], event["lat"], event["lon"])
            if dist <= event["impact_radius"]:
                nearby_events.append({
                    "name": event["name"],
                    "distance": int(dist),
                    "boost": event["traffic_boost"]
                })
                event_boost = max(event_boost, event["traffic_boost"]) # Take max boost if multiple events
        
        # Apply boost to traffic level (cap at 100)
        original_traffic = traffic_level
        traffic_level = min(100, traffic_level + event_boost)
        
        # Filter by minimum traffic
        if traffic_level < min_traffic:
            continue
        
        # Calculate distance to nearest cafe (keep for info)
        nearest_cafe_dist = find_nearest_cafe(spot["lat"], spot["lon"], cafes_data)
        
        # Calculate Cafe Density
        cafe_density = calculate_cafe_density(spot["lat"], spot["lon"], cafes_data)
        density_info = get_density_label(cafe_density)
        
        # Filter by weather suitability
        if require_suitable_weather and not weather_suitable:
            continue
        
        # Calculate business score using Density
        score_data = calculate_business_score(traffic_level, cafe_density, weather_suitable)
        
        # Build result
        spot_result = spot.copy()
        spot_result["traffic_level"] = traffic_level
        spot_result["nearest_cafe_distance"] = round(nearest_cafe_dist, 1)
        spot_result["cafe_density"] = cafe_density
        spot_result["density_label"] = density_info["label"]
        spot_result["density_color"] = density_info["color"]
        spot_result["weather_suitable"] = weather_suitable
        spot_result["data_available"] = data_available
        spot_result.update(score_data)
        
        # Add permit info
        permit_info = get_permit_status(spot["name"])
        spot_result["permit_status"] = permit_info["status"]
        spot_result["permit_label"] = permit_info["label"]
        spot_result["permit_color"] = permit_info["color"]
        
        # Add event info
        spot_result["nearby_events"] = nearby_events
        spot_result["event_boost"] = event_boost
        spot_result["original_traffic"] = original_traffic
        
        result.append(spot_result)
    
    # Sort by business score (descending)
    result.sort(key=lambda x: x["business_score"], reverse=True)
    
    return result

def estimate_traffic(name: str, spot_type: str, simulated_hour: Optional[int] = None) -> int:
    """Estimate traffic level based on spot type and name"""
    import datetime
    
    if simulated_hour is not None:
        hour = simulated_hour
        # Assume weekday for simulation unless we want to get fancy
        day = 0 
    else:
        now = datetime.datetime.now()
        hour = now.hour
        day = now.weekday()
    
    # Base traffic by type
    base_traffic = {
        "tourist": 75,
        "transport": 80,
        "shopping": 70,
        "park": 60,
        "neighborhood": 50,
        "cultural": 55
    }
    
    base = base_traffic.get(spot_type, 50)
    
    # Time multiplier profiles
    multiplier = 0.3 # Default low
    
    if spot_type == "park":
        # Parks: High during day, very low at night
        if 6 <= hour < 10: multiplier = 0.6
        elif 10 <= hour < 18: multiplier = 1.1 # Peak
        elif 18 <= hour < 21: multiplier = 0.5 # Sunset/Evening
        else: multiplier = 0.1 # Night
        
    elif spot_type == "shopping":
        # Shopping: High during business hours
        if 9 <= hour < 11: multiplier = 0.7
        elif 11 <= hour < 17: multiplier = 1.0
        elif 17 <= hour < 19: multiplier = 0.8
        else: multiplier = 0.2 # Closed
        
    elif spot_type == "transport":
        # Transport: Rush hours
        if 7 <= hour < 10: multiplier = 1.2 # Morning Rush
        elif 10 <= hour < 15: multiplier = 0.8
        elif 15 <= hour < 19: multiplier = 1.2 # Evening Rush
        elif 19 <= hour < 23: multiplier = 0.6
        else: multiplier = 0.3
        
    elif spot_type == "tourist":
        # Tourist: Steady day, good evening
        if 9 <= hour < 12: multiplier = 0.8
        elif 12 <= hour < 18: multiplier = 1.1
        elif 18 <= hour < 23: multiplier = 0.9 # Evening dining/walking
        else: multiplier = 0.2
        
    elif spot_type == "neighborhood":
        # Neighborhood: Morning coffee + Evening
        if 7 <= hour < 10: multiplier = 1.0 # Morning coffee
        elif 10 <= hour < 16: multiplier = 0.6 # Work hours
        elif 16 <= hour < 20: multiplier = 0.9 # After work
        else: multiplier = 0.4
        
    else:
        # General fallback
        if 8 <= hour < 18: multiplier = 0.9
        elif 18 <= hour < 22: multiplier = 0.6
        else: multiplier = 0.2
    
    # Weekend boost for tourist/park areas
    if day >= 5 and spot_type in ["tourist", "park", "shopping"]:
        multiplier *= 1.3
    
    return min(100, int(base * multiplier))



@app.get("/api/activity-zones")
def activity_zones(
    min_traffic: Optional[int] = Query(0, ge=0, le=100),
    max_competition_distance: Optional[int] = Query(5000, ge=0, le=5000),
    require_suitable_weather: Optional[bool] = Query(False),
    use_live_data: Optional[bool] = Query(False)
):
    """
    Get aggregated activity zones showing overall business potential.
    Much faster than individual hotspot scoring.
    """
    # Get scored hotspots (reuse existing logic)
    weather_data = get_weather()
    weather_suitable = weather_data.get("is_suitable", True)
    cafes_data = get_cafes()
    
    if require_suitable_weather and not weather_suitable:
        return []
    
    hotspots_scored = []
    for spot in COPENHAGEN_HOTSPOTS:
        if use_live_data:
            popular_data = get_popular_times(spot["name"], "Copenhagen")
            traffic_level = popular_data.get("current_popularity", 50)
        else:
            traffic_level = estimate_traffic(spot["name"], spot["type"])
        
        if traffic_level < min_traffic:
            continue
        
        nearest_cafe_dist = find_nearest_cafe(spot["lat"], spot["lon"], cafes_data)
        cafe_density = calculate_cafe_density(spot["lat"], spot["lon"], cafes_data)
        
        score_data = calculate_business_score(traffic_level, cafe_density, weather_suitable)
        
        spot_result = spot.copy()
        spot_result["traffic_level"] = traffic_level
        spot_result["nearest_cafe_distance"] = round(nearest_cafe_dist, 1)
        spot_result["cafe_density"] = cafe_density
        spot_result["weather_suitable"] = weather_suitable
        spot_result.update(score_data)
        
        hotspots_scored.append(spot_result)
    
    # Calculate zone aggregates
    zones = calculate_zone_scores(hotspots_scored)
    
    return zones

@app.get("/api/permit-info")
def get_permit_info():
    """Get Copenhagen permit regulations and information"""
    return PERMIT_REGULATIONS

@app.get("/api/hotspots-with-permits")
def hotspots_with_permits():
    """Get all hotspots with permit status included"""
    result = []
    for spot in COPENHAGEN_HOTSPOTS:
        spot_copy = spot.copy()
        permit_info = get_permit_status(spot["name"])
        spot_copy["permit_status"] = permit_info["status"]
        spot_copy["permit_label"] = permit_info["label"]
        spot_copy["permit_color"] = permit_info["color"]
        result.append(spot_copy)
    return result

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """Serve the React frontend for any unmatched route"""
    # Allow API routes to pass through (handled by FastAPI priority)
    if full_path.startswith("api/"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Check if a specific file exists in static (e.g. favicon.ico, manifest.json)
    file_path = f"{static_dir}/{full_path}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
        
    # Otherwise serve index.html for SPA routing
    if os.path.exists(f"{static_dir}/index.html"):
        return FileResponse(f"{static_dir}/index.html")
    
    return {"message": "Frontend not built. Run build.sh to generate static files."}
