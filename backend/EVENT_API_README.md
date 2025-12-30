# GutIQ Event Logging APIs

This document describes the Event Logging APIs implemented for Phase 3 of the GutIQ project.

## Overview

The Event Logging APIs allow you to create and retrieve events for meals, exercise, and symptoms with their associated data.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Create Event

**POST** `/events`

Creates a new event (meal, exercise, or symptom) and associated subtype data.

#### Request Body

The request body follows a generic event wrapper pattern:

```json
{
  "timestamp": "2025-01-02T08:30:00",
  "event_type": "meal|exercise|symptom",
  "data": { ... event-specific data ... }
}
```

#### Examples

**Meal Event:**
```json
{
  "timestamp": "2025-01-02T08:30:00",
  "event_type": "meal",
  "data": {
    "foods": ["oatmeal", "berries", "eggs"],
    "calories": 450,
    "protein": 25,
    "carbohydrates": 55,
    "fats": 15
  }
}
```

**Exercise Event:**
```json
{
  "timestamp": "2025-01-02T07:00:00",
  "event_type": "exercise",
  "data": {
    "type": "running",
    "duration_minutes": 30
  }
}
```

**Symptom Event:**
```json
{
  "timestamp": "2025-01-02T14:30:00",
  "event_type": "symptom",
  "data": {
    "description": "stomach cramps and bloating",
    "severity": "mild|moderate|severe"
  }
}
```

#### Response

```json
{
  "event_id": 1
}
```

### 2. Get All Events

**GET** `/events`

Returns all events with their associated subtype data, ordered by timestamp (most recent first).

#### Response

```json
[
  {
    "event_id": 1,
    "timestamp": "2025-01-02T14:30:00Z",
    "event_type": "meal",
    "data": {
      "foods": ["oatmeal", "berries", "eggs"],
      "calories": 450.0,
      "protein": 25.0,
      "carbohydrates": 55.0,
      "fats": 15.0
    }
  },
  {
    "event_id": 2,
    "timestamp": "2025-01-02T13:00:00Z",
    "event_type": "exercise",
    "data": {
      "type": "running",
      "duration_minutes": 30.0
    }
  }
]
```

### 3. Get Event by ID

**GET** `/events/{event_id}`

Returns one event and its sub-entity data.

#### Response

**Meal Example:**
```json
{
  "event_id": 1,
  "timestamp": "2025-01-02T14:30:00Z",
  "event_type": "meal",
  "data": {
    "foods": ["greek yogurt", "banana", "chia seeds"],
    "calories": 320.0,
    "protein": 18.0,
    "carbohydrates": 42.0,
    "fats": 8.0
  }
}
```

**Exercise Example:**
```json
{
  "event_id": 2,
  "timestamp": "2025-01-02T07:45:00Z",
  "event_type": "exercise",
  "data": {
    "type": "running",
    "duration_minutes": 35.0
  }
}
```

**Symptom Example:**
```json
{
  "event_id": 3,
  "timestamp": "2025-01-02T17:40:00Z",
  "event_type": "symptom",
  "data": {
    "description": "stomach cramps and bloating",
    "severity": "moderate"
  }
}
```

## Running the Server

1. Activate your virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. The API will be available at `http://localhost:8000`

4. View the interactive API documentation at `http://localhost:8000/docs`

## Testing the APIs

### Using curl

```bash
# Create a meal event
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2025-01-02T08:30:00",
    "event_type": "meal",
    "data": {
      "foods": ["oatmeal", "berries", "eggs"],
      "calories": 450,
      "protein": 25,
      "carbohydrates": 55,
      "fats": 15
    }
  }'

# Get all events
curl http://localhost:8000/events

# Get specific event
curl http://localhost:8000/events/1
```

### Using Python

Run the provided test script:
```bash
python test_events_api.py
```

## Data Models

### Event Types
- `meal` - Food consumption events
- `exercise` - Physical activity events
- `symptom` - GI symptom events

### Symptom Severity Levels
- `mild`
- `moderate`
- `severe`

### Required Fields

**Meal:**
- `foods` (list of strings) - required
- `calories`, `protein`, `carbohydrates`, `fats` (floats) - optional

**Exercise:**
- `type` (string) - required
- `duration_minutes` (float) - required, must be > 0

**Symptom:**
- `description` (string) - required
- `severity` (enum) - required

## Error Handling

The API returns appropriate HTTP status codes:
- `201 Created` - Event successfully created
- `200 OK` - Event(s) successfully retrieved
- `404 Not Found` - Event not found
- `400 Bad Request` - Invalid data format or missing required fields
- `422 Unprocessable Entity` - Validation error

## Next Steps

Phase 3 is complete! The following milestones are:
- **Phase 4**: Frontend Event UI - Build React components to log and view events
- **Phase 5**: AI Integration - Add LLM analysis capabilities
- **Phase 6**: Display insights in the UI

## Files Created

- `app/schemas/events.py` - Pydantic schemas for event validation
- `app/api/events.py` - Event API endpoints
- `app/main.py` - Updated to include event router
- `test_events_api.py` - Python test script
- `EVENT_API_README.md` - This documentation
