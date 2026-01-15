import requests

BASE_URL = "http://localhost:8000"

def get_all_events():
    """Get all events"""
    response = requests.get(f"{BASE_URL}/events")
    events = response.json()
    return events

def delete_event(event_id):
    """Delete a specific event by ID"""
    response = requests.delete(f"{BASE_URL}/events/{event_id}")
    if response.status_code != 204:
        print(f"Failed to delete event {event_id}: {response.status_code}")
    return response.status_code

if __name__ == "__main__":
    print("=== Deleting All Events ===\n")
    all_events = get_all_events()
    all_events_ids = [event["event_id"] for event in all_events]
    print(f"{len(all_events)} events to delete: {all_events_ids}")
    for event in all_events:
        delete_event(event["event_id"])
    print("=== All Events Deleted ===\n")