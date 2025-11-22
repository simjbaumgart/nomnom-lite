import json
import os
import datetime
from typing import List, Dict, Any

CACHE_FILE = "events_cache.json"
CACHE_DURATION_HOURS = 24

class EventService:
    def __init__(self):
        self.cache_file = CACHE_FILE

    def get_events(self) -> List[Dict[str, Any]]:
        """
        Get events from cache or fetch fresh data if cache is stale.
        Simulates a "once a day" Google Search.
        """
        if self._is_cache_valid():
            return self._load_cache()
        
        events = self._fetch_events_from_source()
        self._save_cache(events)
        return events

    def _is_cache_valid(self) -> bool:
        """Check if cache file exists and is less than 24 hours old."""
        if not os.path.exists(self.cache_file):
            return False
        
        timestamp = os.path.getmtime(self.cache_file)
        cache_time = datetime.datetime.fromtimestamp(timestamp)
        age = datetime.datetime.now() - cache_time
        
        return age.total_seconds() < (CACHE_DURATION_HOURS * 3600)

    def _load_cache(self) -> List[Dict[str, Any]]:
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
            return []

    def _save_cache(self, events: List[Dict[str, Any]]):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(events, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def _fetch_events_from_source(self) -> List[Dict[str, Any]]:
        """
        Simulates a Google Search for 'Events in Copenhagen today'.
        Returns a curated list of realistic events.
        """
        # In a real app, this would use Google Search API or scraping
        # For MVP, we return realistic data for Copenhagen
        
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        
        return [
            {
                "id": "evt_001",
                "name": "Tivoli Gardens Summer Season",
                "description": "Open air concerts and evening illumination",
                "lat": 55.6737,
                "lon": 12.5681,
                "type": "concert",
                "impact_radius": 800,
                "traffic_boost": 30,
                "date": today.isoformat(),
                "time": "18:00"
            },
            {
                "id": "evt_002",
                "name": "Reffen Street Food Market",
                "description": "Busy street food area with live DJ",
                "lat": 55.6938,
                "lon": 12.6082,
                "type": "food",
                "impact_radius": 500,
                "traffic_boost": 25,
                "date": today.isoformat(),
                "time": "12:00"
            },
            {
                "id": "evt_003",
                "name": "Royal Arena Concert",
                "description": "Large international music event",
                "lat": 55.6253,
                "lon": 12.5736,
                "type": "concert",
                "impact_radius": 1000,
                "traffic_boost": 40,
                "date": tomorrow.isoformat(),
                "time": "20:00"
            },
            {
                "id": "evt_004",
                "name": "Torvehallerne Weekend Market",
                "description": "Farmers market and outdoor stalls",
                "lat": 55.6828,
                "lon": 12.5719,
                "type": "market",
                "impact_radius": 300,
                "traffic_boost": 20,
                "date": today.isoformat(),
                "time": "10:00"
            },
            {
                "id": "evt_005",
                "name": "Nyhavn Jazz Festival",
                "description": "Outdoor jazz performances along the canal",
                "lat": 55.6798,
                "lon": 12.5914,
                "type": "festival",
                "impact_radius": 400,
                "traffic_boost": 35,
                "date": tomorrow.isoformat(),
                "time": "15:00"
            }
        ]

# Singleton instance
event_service = EventService()

def get_active_events():
    return event_service.get_events()
