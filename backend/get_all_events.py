import requests
import json

BASE_URL = "http://localhost:8000"

def get_all_events():
    """Get all events"""
    response = requests.get(f"{BASE_URL}/events")
    events = response.json()
    return events

if __name__ == "__main__":
    print("=== Retrieving All Events ===\n")
    all_events = get_all_events()
    print(json.dumps(all_events, indent=2))
    print("=== All Events Retrieved ===\n")