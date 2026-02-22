# GutIQ Backend Scripts

This directory contains test scripts and utilities for development and validation.

## Test Scripts

### AI Insights Testing
- **`test_ai_insights.py`** - Test AI insights generation and retrieval
  ```bash
  python scripts/test_ai_insights.py
  ```
  Tests:
  - POST /ai-insights/generate (generate new insight)
  - GET /ai-insights/ (get all insights)
  - GET /ai-insights/{id} (get single insight)

### Events API Testing
- **`test_events_api.py`** - Test event logging endpoints
  ```bash
  python scripts/test_events_api.py
  ```
  Tests:
  - POST /events (create meal/exercise/symptom)
  - GET /events (retrieve all events)
  - GET /events/{id} (retrieve single event)
  - DELETE /events/{id} (delete event)

## Utility Scripts

- **`get_all_events.py`** - Fetch and display all logged events
  ```bash
  python scripts/get_all_events.py
  ```

- **`delete_all_events.py`** - Delete all events from database (use with caution!)
  ```bash
  python scripts/delete_all_events.py
  ```

## Documentation

- **`EVENT_API_README.md`** - Detailed documentation for Events API endpoints

## Requirements

All scripts require:
- Backend server running on `http://localhost:8000`
- Python `requests` library (already in requirements.txt)
- Active PostgreSQL database

## Usage

Run scripts from the backend directory:
```bash
cd /Users/laurenferg/Desktop/gutiq/backend
source venv/bin/activate
python scripts/test_ai_insights.py
```
