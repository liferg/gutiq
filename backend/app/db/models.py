from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Float,
    Enum,
    Text,
    Integer
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from datetime import datetime
from app.db.database import Base

class EventType(str, enum.Enum):
    meal = "meal"
    exercise = "exercise"
    symptom = "symptom"


class SymptomSeverity(str, enum.Enum):
    mild = "mild"
    moderate = "moderate"
    severe = "severe"


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    event_type = Column(Enum(EventType), nullable=False)

    # One-to-one relationships - Each meal has at most one meal, exercise, and symptom
    meal = relationship("Meal", back_populates="event", uselist=False)
    exercise = relationship("Exercise", back_populates="event", uselist=False)
    symptom = relationship("Symptom", back_populates="event", uselist=False)


class Meal(Base):
    __tablename__ = "meals"

    event_id = Column(
        Integer,
        ForeignKey("events.event_id", ondelete="CASCADE"),
        primary_key=True,
    )

    foods = Column(Text, nullable=False)  # stored as comma-separated string
    calories = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    carbohydrates = Column(Float, nullable=True)
    fats = Column(Float, nullable=True)

    event = relationship("Event", back_populates="meal")


class Exercise(Base):
    __tablename__ = "exercises"

    event_id = Column(
        Integer,
        ForeignKey("events.event_id", ondelete="CASCADE"),
        primary_key=True,
    )

    type = Column(String, nullable=False)
    duration_minutes = Column(Float, nullable=False)

    event = relationship("Event", back_populates="exercise")


class Symptom(Base):
    __tablename__ = "symptoms"

    event_id = Column(
        Integer,
        ForeignKey("events.event_id", ondelete="CASCADE"),
        primary_key=True,
    )

    description = Column(Text, nullable=False)
    severity = Column(Enum(SymptomSeverity), nullable=False)

    event = relationship("Event", back_populates="symptom")


class AIInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    description = Column(Text, nullable=False)
