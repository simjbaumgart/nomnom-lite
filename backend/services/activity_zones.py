from typing import Dict, List, Tuple

# Define activity zones with geographic boundaries
ACTIVITY_ZONES = [
    {
        "name": "City Center",
        "center": [55.6761, 12.5683],
        "radius": 1000,  # meters
        "hotspots": ["Nyhavn", "Strøget", "Tivoli Gardens", "Kongens Nytorv", 
                     "Christiansborg Palace", "The Round Tower", "Torvehallerne Market",
                     "Magasin du Nord", "Copenhagen Central Station"]
    },
    {
        "name": "Nørrebro District",
        "center": [55.6897, 12.5531],
        "radius": 800,
        "hotspots": ["Nørrebro", "Nørreport Station", "Fælled Park"]
    },
    {
        "name": "Vesterbro District",
        "center": [55.6682, 12.5510],
        "radius": 700,
        "hotspots": ["Vesterbro", "Fisketorvet Shopping Center"]
    },
    {
        "name": "Østerbro & Waterfront",
        "center": [55.6950, 12.5870],
        "radius": 900,
        "hotspots": ["Østerbro", "The Little Mermaid", "Kastellet", "Østerport Station"]
    },
    {
        "name": "Frederiksberg Area",
        "center": [55.6775, 12.5320],
        "radius": 750,
        "hotspots": ["Frederiksberg", "Frederiksberg Centret", "Frederiksberg Gardens", 
                     "Forum Station"]
    },
    {
        "name": "Islands & Amager",
        "center": [55.6691, 12.5857],
        "radius": 850,
        "hotspots": ["Christianshavn", "Islands Brygge", "Christianshavn Metro", 
                     "IT University", "Amager Strandpark"]
    },
    {
        "name": "Cultural Quarter",
        "center": [55.6850, 12.5780],
        "radius": 600,
        "hotspots": ["University of Copenhagen", "Rosenborg Castle", "The King's Garden",
                     "National Gallery", "Amalienborg Palace"]
    }
]

def calculate_zone_scores(hotspots_with_scores: List[Dict]) -> List[Dict]:
    """
    Aggregate hotspot scores into activity zones.
    
    Args:
        hotspots_with_scores: List of hotspots with business scores
    
    Returns:
        List of zones with aggregated scores
    """
    zones_result = []
    
    for zone in ACTIVITY_ZONES:
        # Find hotspots in this zone
        zone_hotspots = [
            h for h in hotspots_with_scores 
            if h["name"] in zone["hotspots"]
        ]
        
        if not zone_hotspots:
            continue
        
        # Calculate average scores
        avg_traffic = sum(h["traffic_level"] for h in zone_hotspots) / len(zone_hotspots)
        avg_business_score = sum(h["business_score"] for h in zone_hotspots) / len(zone_hotspots)
        avg_competition = sum(h["nearest_cafe_distance"] for h in zone_hotspots) / len(zone_hotspots)
        
        # Determine zone color based on business score
        if avg_business_score >= 80:
            color = "#22c55e"  # Green
            recommendation = "excellent"
        elif avg_business_score >= 60:
            color = "#eab308"  # Yellow
            recommendation = "good"
        elif avg_business_score >= 40:
            color = "#f59e0b"  # Orange
            recommendation = "moderate"
        else:
            color = "#ef4444"  # Red
            recommendation = "poor"
        
        zones_result.append({
            "name": zone["name"],
            "center_lat": zone["center"][0],
            "center_lon": zone["center"][1],
            "radius": zone["radius"],
            "avg_traffic": round(avg_traffic, 1),
            "avg_business_score": round(avg_business_score, 1),
            "avg_competition_distance": round(avg_competition, 1),
            "hotspot_count": len(zone_hotspots),
            "color": color,
            "recommendation": recommendation
        })
    
    # Sort by business score
    zones_result.sort(key=lambda x: x["avg_business_score"], reverse=True)
    
    return zones_result
