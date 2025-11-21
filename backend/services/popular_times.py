from playwright.sync_api import sync_playwright
import re
import json
from typing import Dict, Optional
import time

def get_popular_times(place_name: str, location: str = "Copenhagen") -> Dict:
    """
    Scrape Google Maps Popular Times data for a given place.
    
    Args:
        place_name: Name of the place (e.g., "Nyhavn")
        location: City/location context (e.g., "Copenhagen")
    
    Returns:
        Dict with current_popularity and popular_times data
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Search for the place on Google Maps
            search_query = f"{place_name} {location}"
            maps_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            page.goto(maps_url, timeout=30000)
            time.sleep(3)  # Wait for page to load
            
            # Try to find popular times data
            current_popularity = None
            popular_times = {}
            
            # Look for "Popular times" section
            try:
                # Check if "Popular times" text exists
                popular_section = page.locator('text="Popular times"').first
                if popular_section.is_visible(timeout=5000):
                    # Try to extract current busyness
                    # Google shows this as "Usually X% as busy as it gets"
                    page_content = page.content()
                    
                    # Look for percentage indicators
                    percentage_matches = re.findall(r'(\d+)%', page_content)
                    if percentage_matches:
                        # Take the first reasonable percentage (0-100)
                        for match in percentage_matches:
                            val = int(match)
                            if 0 <= val <= 100:
                                current_popularity = val
                                break
                    
                    # Look for live indicator
                    if 'Live' in page_content or 'live' in page_content:
                        # Extract live busyness if available
                        live_matches = re.findall(r'Live.*?(\d+)%', page_content, re.DOTALL)
                        if live_matches:
                            current_popularity = int(live_matches[0])
            except Exception as e:
                print(f"Could not find popular times section: {e}")
            
            browser.close()
            
            # If we found data, return it
            if current_popularity is not None:
                return {
                    "place_name": place_name,
                    "current_popularity": current_popularity,
                    "data_available": True,
                    "timestamp": time.time()
                }
            else:
                # Return default/estimated data
                return {
                    "place_name": place_name,
                    "current_popularity": estimate_busyness(place_name),
                    "data_available": False,
                    "timestamp": time.time(),
                    "note": "Using estimated data - Popular Times not available"
                }
                
    except Exception as e:
        print(f"Error scraping popular times for {place_name}: {e}")
        return {
            "place_name": place_name,
            "current_popularity": estimate_busyness(place_name),
            "data_available": False,
            "error": str(e)
        }

def estimate_busyness(place_name: str) -> int:
    """
    Estimate busyness based on place name and current time.
    Fallback when scraping fails.
    """
    import datetime
    
    # Get current hour (Copenhagen time - UTC+1)
    now = datetime.datetime.now()
    hour = now.hour
    day_of_week = now.weekday()  # 0=Monday, 6=Sunday
    
    # Base busyness levels for known tourist spots
    base_levels = {
        "Nyhavn": 85,
        "Strøget": 80,
        "Nørreport Station": 75,
        "Tivoli Gardens": 80,
        "Kongens Nytorv": 70,
        "Christiansborg": 65,
        "The Round Tower": 60,
    }
    
    base = base_levels.get(place_name, 50)
    
    # Time-based adjustments
    if hour < 7 or hour > 22:  # Early morning / late night
        multiplier = 0.2
    elif 7 <= hour < 10:  # Morning
        multiplier = 0.5
    elif 10 <= hour < 14:  # Midday
        multiplier = 0.9
    elif 14 <= hour < 18:  # Afternoon
        multiplier = 1.0
    elif 18 <= hour < 22:  # Evening
        multiplier = 0.8
    else:
        multiplier = 0.3
    
    # Weekend boost
    if day_of_week >= 5:  # Saturday or Sunday
        multiplier *= 1.2
    
    return min(100, int(base * multiplier))
