"""
Hotspot definitions for NomNom Lite supported cities.
"""

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

GHENT_HOTSPOTS = [
    # Tourist Areas
    {"name": "Graslei", "lat": 51.0536, "lon": 3.7207, "type": "tourist"},
    {"name": "Korenlei", "lat": 51.0539, "lon": 3.7202, "type": "tourist"},
    {"name": "Gravensteen", "lat": 51.0577, "lon": 3.7208, "type": "tourist"},
    {"name": "Saint Bavo's Cathedral", "lat": 51.0529, "lon": 3.7250, "type": "tourist"},
    {"name": "Belfry of Ghent", "lat": 51.0536, "lon": 3.7249, "type": "tourist"},
    {"name": "Saint Nicholas' Church", "lat": 51.0539, "lon": 3.7228, "type": "tourist"},
    {"name": "Vrijdagmarkt", "lat": 51.0563, "lon": 3.7256, "type": "tourist"},
    
    # Transport Hubs
    {"name": "Gent-Sint-Pieters Station", "lat": 51.0359, "lon": 3.7106, "type": "transport"},
    {"name": "Gent-Dampoort Station", "lat": 51.0565, "lon": 3.7416, "type": "transport"},
    {"name": "Korenmarkt", "lat": 51.0542, "lon": 3.7218, "type": "transport"}, # Tram hub
    
    # Shopping & Business
    {"name": "Veldstraat", "lat": 51.0519, "lon": 3.7214, "type": "shopping"},
    {"name": "Langemunt", "lat": 51.0556, "lon": 3.7236, "type": "shopping"},
    {"name": "Dok Noord", "lat": 51.0661, "lon": 3.7336, "type": "shopping"},
    
    # Parks & Recreation
    {"name": "Citadelpark", "lat": 51.0372, "lon": 3.7233, "type": "park"},
    {"name": "Blaarmeersen", "lat": 51.0461, "lon": 3.6853, "type": "park"},
    {"name": "Muinkpark", "lat": 51.0436, "lon": 3.7308, "type": "park"},
    {"name": "Keizerpark", "lat": 51.0428, "lon": 3.7436, "type": "park"},
    
    # Neighborhoods
    {"name": "Patershol", "lat": 51.0583, "lon": 3.7231, "type": "neighborhood"},
    {"name": "Ledeberg", "lat": 51.0383, "lon": 3.7450, "type": "neighborhood"},
    
    # Universities & Cultural
    {"name": "Ghent University (Rectoraat)", "lat": 51.0467, "lon": 3.7275, "type": "cultural"},
    {"name": "KASK & Conservatorium", "lat": 51.0422, "lon": 3.7189, "type": "cultural"},
    {"name": "STAM Ghent City Museum", "lat": 51.0425, "lon": 3.7172, "type": "cultural"},
]

def get_hotspots(city_id: str):
    if city_id == "ghent":
        return GHENT_HOTSPOTS
    return COPENHAGEN_HOTSPOTS
