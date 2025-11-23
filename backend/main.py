from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.services.weather import get_weather
from backend.services.places import get_cafes
from backend.services.popular_times import get_popular_times
from backend.services.business_score import calculate_business_score, find_nearest_cafe, calculate_cafe_density, get_density_label
from backend.services.activity_zones import calculate_zone_scores
from backend.services.permit_info import get_permit_status, PERMIT_REGULATIONS
from backend.services.events import get_active_events
from typing import Optional
from backend.config import CITIES, DEFAULT_CITY_ID
from backend.hotspots import get_hotspots

app = FastAPI(title="NomNom Lite API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Logging Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nomnom_api")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log format: METHOD PATH STATUS_CODE DURATION_MS
        logger.info(
            f"{request.method} {request.url.path} "
            f"{response.status_code} {process_time:.4f}s"
        )
        return response

app.add_middleware(RequestLoggingMiddleware)

# Serve Static Files (Frontend)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Mount static files if directory exists (it will after build)
# Mount static files if directory exists (it will after build)
# Use absolute path relative to this file to ensure it works regardless of CWD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="assets")

@app.get("/")
async def read_root():
    # Serve index.html if it exists (Production)
    if os.path.exists(f"{static_dir}/index.html"):
        return FileResponse(f"{static_dir}/index.html")
    return {"message": "NomNom Lite API", "status": "running"}

@app.get("/api/cities")
def get_cities():
    """Get list of supported cities"""
    return CITIES

@app.get("/api/weather")
def weather(city_id: str = DEFAULT_CITY_ID):
    """Get current weather data for a specific city"""
    # TODO: Update weather service to accept city_id (currently hardcoded to Copenhagen)
    # For now, we'll just return Copenhagen weather as a placeholder for Ghent if needed,
    # or ideally update the weather service.
    return get_weather()

@app.get("/api/cafes")
def cafes(city_id: str = DEFAULT_CITY_ID):
    """Get cafe locations in a specific city"""
    return get_cafes(city_id)

@app.get("/api/hotspots")
def hotspots(city_id: str = DEFAULT_CITY_ID):
    """Get all hotspots with default traffic levels for a city"""
    city_hotspots = get_hotspots(city_id)
    result = []
    for spot in city_hotspots:
        spot_copy = spot.copy()
        spot_copy["traffic_level"] = estimate_traffic(spot["name"], spot["type"])
        result.append(spot_copy)
    return result

@app.get("/api/popular-times/{place_name}")
def popular_times(place_name: str, city_id: str = DEFAULT_CITY_ID):
    """Get Popular Times data for a specific place"""
    city_name = CITIES.get(city_id, {}).get("name", "Copenhagen")
    return get_popular_times(place_name, city_name)

@app.get("/api/hotspots-live")
def hotspots_live(city_id: str = DEFAULT_CITY_ID):
    """Get hotspots with LIVE busyness data from Google Maps (slow)"""
    city_hotspots = get_hotspots(city_id)
    city_name = CITIES.get(city_id, {}).get("name", "Copenhagen")
    result = []
    for spot in city_hotspots:
        popular_data = get_popular_times(spot["name"], city_name)
        spot_copy = spot.copy()
        spot_copy["traffic_level"] = popular_data.get("current_popularity", 50)
        spot_copy["data_available"] = popular_data.get("data_available", False)
        result.append(spot_copy)
    return result

@app.get("/api/events")
def events(city_id: str = DEFAULT_CITY_ID):
    """Get active events in a city (cached daily)"""
    # TODO: Update event service to support multiple cities
    return get_active_events()

@app.get("/api/hotspots-scored")
def hotspots_scored(
    city_id: str = DEFAULT_CITY_ID,
    min_traffic: Optional[int] = Query(0, ge=0, le=100),
    max_competition_distance: Optional[int] = Query(1000, ge=0, le=5000),
    require_suitable_weather: Optional[bool] = Query(False),
    use_live_data: Optional[bool] = Query(False),
    simulated_hour: Optional[int] = Query(None, ge=0, le=23)
):
    """
    Get hotspots with business scores and filtering options.
    """
    # Get weather data
    weather_data = get_weather() # TODO: Pass city_id
    weather_suitable = weather_data.get("is_suitable", True)
    
    # Get cafe data for competition analysis
    cafes_data = get_cafes(city_id)
    
    # Get active events
    active_events = get_active_events() # TODO: Pass city_id
    
    city_hotspots = get_hotspots(city_id)
    city_name = CITIES.get(city_id, {}).get("name", "Copenhagen")
    
    result = []
    for spot in city_hotspots:
        # Get traffic level
        if use_live_data:
            popular_data = get_popular_times(spot["name"], city_name)
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
            # Simple distance check - assumes events are in the same city for now
            # TODO: Filter events by city first
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
        permit_info = get_permit_status(spot["name"], city_id)
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
    city_id: str = DEFAULT_CITY_ID,
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
    weather_data = get_weather() # TODO: Pass city_id
    weather_suitable = weather_data.get("is_suitable", True)
    cafes_data = get_cafes(city_id)
    
    if require_suitable_weather and not weather_suitable:
        return []
    
    city_hotspots = get_hotspots(city_id)
    city_name = CITIES.get(city_id, {}).get("name", "Copenhagen")
    
    hotspots_scored = []
    for spot in city_hotspots:
        if use_live_data:
            popular_data = get_popular_times(spot["name"], city_name)
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
def get_permit_info(city_id: str = DEFAULT_CITY_ID):
    """Get permit regulations and information for a city"""
    return PERMIT_REGULATIONS.get(city_id, PERMIT_REGULATIONS[DEFAULT_CITY_ID])

@app.get("/api/hotspots-with-permits")
def hotspots_with_permits(city_id: str = DEFAULT_CITY_ID):
    """Get all hotspots with permit status included"""
    city_hotspots = get_hotspots(city_id)
    result = []
    for spot in city_hotspots:
        spot_copy = spot.copy()
        permit_info = get_permit_status(spot["name"], city_id)
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
