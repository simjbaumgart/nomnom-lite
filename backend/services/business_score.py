import math
from typing import Dict, List

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates in meters using Haversine formula.
    """
    R = 6371000  # Earth radius in meters
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def find_nearest_cafe(hotspot_lat: float, hotspot_lon: float, cafes: List[Dict]) -> float:
    """
    Find distance to nearest cafe from a hotspot.
    Returns distance in meters.
    """
    min_distance = float('inf')
    
    for cafe in cafes:
        if cafe.get('error'):
            continue
        distance = calculate_distance(hotspot_lat, hotspot_lon, cafe['lat'], cafe['lon'])
        min_distance = min(min_distance, distance)
    
    return min_distance if min_distance != float('inf') else 500  # Default 500m if no cafes

def calculate_cafe_density(hotspot_lat: float, hotspot_lon: float, cafes: List[Dict], radius_meters: int = 400) -> int:
    """
    Calculate number of cafes within a specific radius.
    """
    count = 0
    for cafe in cafes:
        if cafe.get('error'):
            continue
        distance = calculate_distance(hotspot_lat, hotspot_lon, cafe['lat'], cafe['lon'])
        if distance <= radius_meters:
            count += 1
    return count

def get_density_label(count: int) -> Dict:
    """Return label and color for density count"""
    if count >= 5:
        return {"label": "High", "color": "#22c55e", "score_boost": 20}
    elif count >= 2:
        return {"label": "Medium", "color": "#eab308", "score_boost": 10}
    else:
        return {"label": "Low", "color": "#94a3b8", "score_boost": 0}

def calculate_business_score(
    traffic_level: int,
    cafe_density_count: int,
    weather_suitable: bool
) -> Dict:
    """
    Calculate business profitability score for a coffee cart location.
    
    Args:
        traffic_level: 0-100, from Popular Times or estimation
        cafe_density_count: number of cafes within 400m
        weather_suitable: boolean from weather service
    
    Returns:
        Dict with score and breakdown
    """
    # Traffic component (50% weight)
    traffic_score = traffic_level * 0.5
    
    # Competition/Density component (30% weight)
    # Clustering Strategy: More cafes = Better hotspot
    density_info = get_density_label(cafe_density_count)
    competition_score = density_info["score_boost"] * 1.5 # Scale to max 30 points (20 * 1.5 = 30)
    
    # Weather component (20% weight)
    weather_score = 100 * 0.2 if weather_suitable else 0
    
    # Total business score
    business_score = traffic_score + competition_score + weather_score
    
    # Determine recommendation level
    if business_score >= 80:
        recommendation = "excellent"
        color = "#22c55e"  # Green
    elif business_score >= 60:
        recommendation = "good"
        color = "#eab308"  # Yellow
    elif business_score >= 40:
        recommendation = "moderate"
        color = "#f59e0b"  # Orange
    else:
        recommendation = "poor"
        color = "#ef4444"  # Red
    
    return {
        "business_score": round(business_score, 1),
        "recommendation": recommendation,
        "color": color,
        "breakdown": {
            "traffic_contribution": round(traffic_score, 1),
            "competition_contribution": round(competition_score, 1),
            "weather_contribution": round(weather_score, 1)
        }
    }
