"""
Pydantic schemas for AI Insights API endpoints.
"""

from pydantic import BaseModel
from datetime import datetime


class AIInsightCreate(BaseModel):
    """Schema for creating an AI insight (internal use, for testing purposes)."""
    timestamp: datetime
    description: str


class AIInsightResponse(BaseModel):
    """Schema for AI insight response."""
    id: int
    timestamp: datetime
    description: str

    class Config:
        from_attributes = True


class GenerateInsightRequest(BaseModel):
    """Schema for requesting AI insight generation."""
    time_range_days: int = 7  # Look back 7 days by default


class GenerateInsightResponse(BaseModel):
    """Schema for AI insight generation response."""
    insight: str
    saved_insight_id: int
    events_analyzed: int
    timestamp: datetime
