from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Union
from app.db.models import EventType, SymptomSeverity


# --- Meal Schemas ---
class MealData(BaseModel):
    foods: List[str] = Field(..., description="List of foods consumed")
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None


class MealResponse(BaseModel):
    foods: List[str]
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None

    class Config:
        from_attributes = True


# --- Exercise Schemas ---
class ExerciseData(BaseModel):
    type: str = Field(..., description="Exercise category (running, lifting, etc.)")
    duration_minutes: float = Field(..., gt=0, description="Duration in minutes")


class ExerciseResponse(BaseModel):
    type: str
    duration_minutes: float

    class Config:
        from_attributes = True


# --- Symptom Schemas ---
class SymptomData(BaseModel):
    description: str = Field(..., description="Free-text description of symptoms")
    severity: SymptomSeverity = Field(..., description="Severity level")


class SymptomResponse(BaseModel):
    description: str
    severity: SymptomSeverity

    class Config:
        from_attributes = True


# --- Event Schemas ---
class EventCreate(BaseModel):
    timestamp: datetime
    event_type: EventType
    data: Union[MealData, ExerciseData, SymptomData] = Field(
        ..., description="Event-specific data based on event_type"
    )


class EventResponse(BaseModel):
    event_id: int
    timestamp: datetime
    event_type: EventType
    data: Union[MealResponse, ExerciseResponse, SymptomResponse]

    class Config:
        from_attributes = True


class EventCreateResponse(BaseModel):
    event_id: int

    class Config:
        from_attributes = True
