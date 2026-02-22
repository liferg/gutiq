"""
Test script for AI Insights API
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_generate_insight():
    """Test generating an AI insight"""
    print("\nTesting AI Insight Generation...")

    url = f"{BASE_URL}/ai-insights/generate"
    payload = {"time_range_days": 7}

    print(f"POST {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=60)

        print(f"\nStatus Code: {response.status_code}")

        if response.status_code == 201:
            data = response.json()
            print(f"\n Success! Insight generated:")
            print(f"   - Insight ID: {data['saved_insight_id']}")
            print(f"   - Events Analyzed: {data['events_analyzed']}")
            print(f"   - Timestamp: {data['timestamp']}")
            print(f"\n   AI Insight:")
            print(f"   {data['insight']}")
            return data['saved_insight_id']
        else:
            print(f"❌ Error: {response.text}")
            return None

    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_get_insights():
    """Test retrieving all insights"""
    print("\n Testing Get All Insights...")

    url = f"{BASE_URL}/ai-insights/"

    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=10)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"\n Success! Retrieved {len(data)} insights. Here are the first 3:")
            for i, insight in enumerate(data[:3], 1):  # Show first 3
                print(f"\n   Insight {i}:")
                print(f"   - ID: {insight['id']}")
                print(f"   - Timestamp: {insight['timestamp']}")
                print(f"   - Description: {insight['description'][:100]}...")
        else:
            print(f"❌ Error: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")


def test_get_single_insight(insight_id):
    """Test retrieving a single insight"""
    if not insight_id:
        print("\n  Skipping single insight test (no ID)")
        return

    print(f"\n Testing Get Single Insight (ID: {insight_id})...")

    url = f"{BASE_URL}/ai-insights/{insight_id}"

    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=10)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"\n Success!")
            print(f"   - ID: {data['id']}")
            print(f"   - Timestamp: {data['timestamp']}")
            print(f"   - Description: {data['description']}")
        else:
            print(f" Error: {response.text}")

    except Exception as e:
        print(f" Error: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("AI Insights API Tests")
    print("=" * 60)

    # Test generating insight
    insight_id = test_generate_insight()

    # Test retrieving all insights
    test_get_insights()

    # Test retrieving single insight
    test_get_single_insight(insight_id)

    print("\n" + "=" * 60)
    print("Tests Complete!")
    print("=" * 60)
