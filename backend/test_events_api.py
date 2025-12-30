"""
Test script for GutIQ Event Logging APIs

This script demonstrates how to use the event logging endpoints:
- POST /events - Create new events (meals, exercise, symptoms)
- GET /events - Get all events
- GET /events/{event_id} - Get a specific event

Run this script with the FastAPI server running:
    uvicorn app.main:app --reload
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"


def create_meal_event():
    """Create a meal event"""
    meal_data = {
        "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(),
        "event_type": "meal",
        "data": {
            "foods": ["greek yogurt", "banana", "chia seeds"],
            "calories": 320,
            "protein": 18,
            "carbohydrates": 42,
            "fats": 8
        }
    }
    response = requests.post(f"{BASE_URL}/events", json=meal_data)
    print(f"Created meal event: {response.json()}")
    return response.json()["event_id"]


def create_exercise_event():
    """Create an exercise event"""
    exercise_data = {
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        "event_type": "exercise",
        "data": {
            "type": "weight lifting",
            "duration_minutes": 45
        }
    }
    response = requests.post(f"{BASE_URL}/events", json=exercise_data)
    print(f"Created exercise event: {response.json()}")
    return response.json()["event_id"]


def create_symptom_event():
    """Create a symptom event"""
    symptom_data = {
        "timestamp": datetime.now().isoformat(),
        "event_type": "symptom",
        "data": {
            "description": "mild nausea after lunch",
            "severity": "mild"
        }
    }
    response = requests.post(f"{BASE_URL}/events", json=symptom_data)
    print(f"Created symptom event: {response.json()}")
    return response.json()["event_id"]


def get_all_events():
    """Get all events"""
    response = requests.get(f"{BASE_URL}/events")
    events = response.json()
    print(f"\nAll events ({len(events)} total):")
    print(json.dumps(events, indent=2))
    return events


def get_event_by_id(event_id):
    """Get a specific event by ID"""
    response = requests.get(f"{BASE_URL}/events/{event_id}")
    event = response.json()
    print(f"\nEvent {event_id}:")
    print(json.dumps(event, indent=2))
    return event


if __name__ == "__main__":
    print("=== Testing GutIQ Event Logging APIs ===\n")

    # Create events
    print("1. Creating events...")
    meal_id = create_meal_event()
    exercise_id = create_exercise_event()
    symptom_id = create_symptom_event()

    # Get all events
    print("\n2. Fetching all events...")
    get_all_events()

    # Get specific event
    print(f"\n3. Fetching specific meal event (ID: {meal_id})...")
    get_event_by_id(meal_id)

    print("\n=== Testing complete! ===")
