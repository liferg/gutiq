from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import AsyncSessionLocal
from app.db.models import Event, Meal, Exercise, Symptom, EventType
from app.schemas.events import (
    EventCreate,
    EventCreateResponse,
    EventResponse,
    MealData,
    MealResponse,
    ExerciseData,
    ExerciseResponse,
    SymptomData,
    SymptomResponse,
)

router = APIRouter(prefix="/events", tags=["events"])


# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("", response_model=EventCreateResponse, status_code=201)
async def create_event(
    event_data: EventCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Creates a new event (meal, exercise, or symptom) and associated subtype data.
    """
    # Create the Event record
    event = Event(
        timestamp=event_data.timestamp,
        event_type=event_data.event_type,
    )
    db.add(event)
    await db.flush()  # Get the event_id without committing

    # Create the appropriate subtype record based on event_type
    if event_data.event_type == EventType.meal:
        if not isinstance(event_data.data, MealData):
            raise HTTPException(
                status_code=400,
                detail="Invalid data format for meal event",
            )
        meal = Meal(
            event_id=event.event_id,
            foods=",".join(event_data.data.foods),  # Store as comma-separated string
            calories=event_data.data.calories,
            protein=event_data.data.protein,
            carbohydrates=event_data.data.carbohydrates,
            fats=event_data.data.fats,
        )
        db.add(meal)

    elif event_data.event_type == EventType.exercise:
        if not isinstance(event_data.data, ExerciseData):
            raise HTTPException(
                status_code=400,
                detail="Invalid data format for exercise event",
            )
        exercise = Exercise(
            event_id=event.event_id,
            type=event_data.data.type,
            duration_minutes=event_data.data.duration_minutes,
        )
        db.add(exercise)

    elif event_data.event_type == EventType.symptom:
        if not isinstance(event_data.data, SymptomData):
            raise HTTPException(
                status_code=400,
                detail="Invalid data format for symptom event",
            )
        symptom = Symptom(
            event_id=event.event_id,
            description=event_data.data.description,
            severity=event_data.data.severity,
        )
        db.add(symptom)

    await db.commit()
    await db.refresh(event)

    return EventCreateResponse(event_id=event.event_id)


@router.get("", response_model=List[EventResponse])
async def get_all_events(db: AsyncSession = Depends(get_db)):
    """
    Returns all events with their associated subtype data.
    """
    # Query all events with their relationships eagerly loaded
    result = await db.execute(
        select(Event).order_by(Event.timestamp.desc())
    )
    events = result.scalars().all()

    response = []
    for event in events:
        # Load the appropriate relationship based on event_type
        if event.event_type == EventType.meal:
            await db.refresh(event, ["meal"])
            if event.meal:
                data = MealResponse(
                    foods=event.meal.foods.split(",") if event.meal.foods else [],
                    calories=event.meal.calories,
                    protein=event.meal.protein,
                    carbohydrates=event.meal.carbohydrates,
                    fats=event.meal.fats,
                )
            else:
                continue
        elif event.event_type == EventType.exercise:
            await db.refresh(event, ["exercise"])
            if event.exercise:
                data = ExerciseResponse(
                    type=event.exercise.type,
                    duration_minutes=event.exercise.duration_minutes,
                )
            else:
                continue
        elif event.event_type == EventType.symptom:
            await db.refresh(event, ["symptom"])
            if event.symptom:
                data = SymptomResponse(
                    description=event.symptom.description,
                    severity=event.symptom.severity,
                )
            else:
                continue
        else:
            continue

        response.append(
            EventResponse(
                event_id=event.event_id,
                timestamp=event.timestamp,
                event_type=event.event_type,
                data=data,
            )
        )

    return response


@router.get("/{event_id}", response_model=EventResponse)
async def get_event_by_id(event_id: int, db: AsyncSession = Depends(get_db)):
    """
    Returns one event and its sub-entity data.
    """
    # Query the event by ID
    result = await db.execute(
        select(Event).where(Event.event_id == event_id)
    )
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Load the appropriate relationship based on event_type
    if event.event_type == EventType.meal:
        await db.refresh(event, ["meal"])
        if not event.meal:
            raise HTTPException(
                status_code=404,
                detail="Meal data not found for this event",
            )
        data = MealResponse(
            foods=event.meal.foods.split(",") if event.meal.foods else [],
            calories=event.meal.calories,
            protein=event.meal.protein,
            carbohydrates=event.meal.carbohydrates,
            fats=event.meal.fats,
        )
    elif event.event_type == EventType.exercise:
        await db.refresh(event, ["exercise"])
        if not event.exercise:
            raise HTTPException(
                status_code=404,
                detail="Exercise data not found for this event",
            )
        data = ExerciseResponse(
            type=event.exercise.type,
            duration_minutes=event.exercise.duration_minutes,
        )
    elif event.event_type == EventType.symptom:
        await db.refresh(event, ["symptom"])
        if not event.symptom:
            raise HTTPException(
                status_code=404,
                detail="Symptom data not found for this event",
            )
        data = SymptomResponse(
            description=event.symptom.description,
            severity=event.symptom.severity,
        )
    else:
        raise HTTPException(status_code=400, detail="Unknown event type")

    return EventResponse(
        event_id=event.event_id,
        timestamp=event.timestamp,
        event_type=event.event_type,
        data=data,
    )
