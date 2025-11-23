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
        
        # Expanded event list with "smaller" events and coffee opportunities
        events = []
        
        # 1. Major Events (Always present for impact)
        events.append({
            "id": "evt_001",
            "name": "Tivoli Gardens Summer Season",
            "description": "Open air concerts and evening illumination",
            "lat": 55.6737,
            "lon": 12.5681,
            "type": "concert",
            "impact_radius": 800,
            "traffic_boost": 30,
            "date": today.isoformat(),
            "time": "18:00",
            "url": "https://www.google.com/search?q=Tivoli+Gardens+Summer+Season+Copenhagen"
        })
        
        events.append({
            "id": "evt_002",
            "name": "Reffen Street Food Market",
            "description": "Busy street food area with live DJ",
            "lat": 55.6938,
            "lon": 12.6082,
            "type": "food",
            "impact_radius": 500,
            "traffic_boost": 25,
            "date": today.isoformat(),
            "time": "12:00",
            "url": "https://www.google.com/search?q=Reffen+Street+Food+Market+Copenhagen"
        })

        # 2. "Smaller" Events & Coffee Opportunities
        
        # Morning Commuter/Yoga Spots (Good for coffee)
        events.append({
            "id": "evt_small_01",
            "name": "Morning Yoga in King's Garden",
            "description": "Community yoga gathering. Coffee needed after!",
            "lat": 55.6856,
            "lon": 12.5787,
            "type": "gathering",
            "impact_radius": 200,
            "traffic_boost": 15,
            "date": today.isoformat(),
            "time": "08:00",
            "url": "https://www.google.com/search?q=Morning+Yoga+King's+Garden+Copenhagen"
        })
        
        events.append({
            "id": "evt_small_02",
            "name": "Langelinie Runners Meetup",
            "description": "Large running group finishing their route.",
            "lat": 55.6919,
            "lon": 12.5975,
            "type": "gathering",
            "impact_radius": 150,
            "traffic_boost": 20,
            "date": today.isoformat(),
            "time": "09:00",
            "url": "https://www.google.com/search?q=Langelinie+Runners+Meetup+Copenhagen"
        })

        # Mid-day Business/Student Crowds
        if today.weekday() < 5: # Weekdays only
            events.append({
                "id": "evt_small_03",
                "name": "Tech Startup Open House",
                "description": "Networking event in Nørrebro.",
                "lat": 55.6897,
                "lon": 12.5531,
                "type": "conference",
                "impact_radius": 100,
                "traffic_boost": 15,
                "date": today.isoformat(),
                "time": "14:00",
                "url": "https://www.google.com/search?q=Tech+Startup+Open+House+Norrebro+Copenhagen"
            })
            
            events.append({
                "id": "evt_small_04",
                "name": "University Pop-up Lecture",
                "description": "Outdoor student gathering.",
                "lat": 55.6794,
                "lon": 12.5726,
                "type": "gathering",
                "impact_radius": 150,
                "traffic_boost": 10,
                "date": today.isoformat(),
                "time": "13:00",
                "url": "https://www.google.com/search?q=University+Pop-up+Lecture+Copenhagen"
            })

        # Weekend Markets (High value)
        if today.weekday() >= 5: # Weekend only
            events.append({
                "id": "evt_small_05",
                "name": "Vesterbro Flea Market",
                "description": "Local vintage market, high foot traffic.",
                "lat": 55.6682,
                "lon": 12.5510,
                "type": "market",
                "impact_radius": 300,
                "traffic_boost": 25,
                "date": today.isoformat(),
                "time": "10:00",
                "url": "https://www.google.com/search?q=Vesterbro+Flea+Market+Copenhagen"
            })
            
            events.append({
                "id": "evt_small_06",
                "name": "Islands Brygge Harbor Fair",
                "description": "Small stalls and music by the water.",
                "lat": 55.6651,
                "lon": 12.5771,
                "type": "market",
                "impact_radius": 250,
                "traffic_boost": 20,
                "date": today.isoformat(),
                "time": "11:00",
                "url": "https://www.google.com/search?q=Islands+Brygge+Harbor+Fair+Copenhagen"
            })

        # Evening/Afternoon Chill
        events.append({
            "id": "evt_small_07",
            "name": "Outdoor Cinema: Zulu Sommerbio",
            "description": "Free movie screening in the park.",
            "lat": 55.6981,
            "lon": 12.5631,
            "type": "cinema",
            "impact_radius": 400,
            "traffic_boost": 35,
            "date": today.isoformat(),
            "time": "19:00",
            "url": "https://www.google.com/search?q=Zulu+Sommerbio+Copenhagen"
        })

        events.append({
            "id": "evt_small_08",
            "name": "Canal Tour Grand Departure",
            "description": "Large tourist group gathering.",
            "lat": 55.6798,
            "lon": 12.5914,
            "type": "tourist",
            "impact_radius": 100,
            "traffic_boost": 25,
            "date": today.isoformat(),
            "time": "15:00",
            "url": "https://www.google.com/search?q=Canal+Tour+Grand+Departure+Copenhagen"
        })

        # Add some future events
        events.append({
            "id": "evt_003",
            "name": "Royal Arena Concert",
            "description": "Large international music event",
            "lat": 55.6253,
            "lon": 12.5736,
            "type": "concert",
            "impact_radius": 1000,
            "traffic_boost": 40,
            "date": tomorrow.isoformat(),
            "time": "20:00",
            "url": "https://www.google.com/search?q=Royal+Arena+Concert+Copenhagen"
        })
        
        return events

# Singleton instance
event_service = EventService()

def get_active_events():
    return event_service.get_events()
