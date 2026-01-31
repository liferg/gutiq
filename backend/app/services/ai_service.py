"""
AI Service for generating insights using OpenAI.
Analyzes user events (meals, exercises, symptoms) to provide personalized insights.
"""

from openai import OpenAI
from app.config import get_settings
from app.db.models import Event, AIInsight
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
import json


class AIService:
    """Service for generating AI insights from user events."""

    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4o-mini"

    def format_events_for_analysis(self, events: list[Event]) -> str:
        """
        Format events into a structured text for AI analysis.
        """
        if not events:
            return "No events logged yet."

        formatted_events = []
        for event in events:
            timestamp_str = event.timestamp.strftime("%Y-%m-%d %H:%M")

            if event.event_type.value == "meal" and event.meal:
                meal = event.meal
                nutrition = []
                if meal.calories:
                    nutrition.append(f"{meal.calories} cal")
                if meal.protein:
                    nutrition.append(f"{meal.protein}g protein")
                if meal.carbohydrates:
                    nutrition.append(f"{meal.carbohydrates}g carbs")
                if meal.fats:
                    nutrition.append(f"{meal.fats}g fats")

                nutrition_str = f" ({', '.join(nutrition)})" if nutrition else ""
                formatted_events.append(
                    f"[{timestamp_str}] MEAL: {meal.foods}{nutrition_str}"
                )

            elif event.event_type.value == "exercise" and event.exercise:
                exercise = event.exercise
                formatted_events.append(
                    f"[{timestamp_str}] EXERCISE: {exercise.type} for {exercise.duration_minutes} minutes"
                )

            elif event.event_type.value == "symptom" and event.symptom:
                symptom = event.symptom
                formatted_events.append(
                    f"[{timestamp_str}] SYMPTOM ({symptom.severity.value}): {symptom.description}"
                )

        return "\n".join(formatted_events)

    async def generate_insight(
        self,
        db: AsyncSession,
        time_range_days: int = 7
    ) -> tuple[str, int]:
        """
        Generate AI insight based on recent user events.

        Args:
            db: Database session
            time_range_days: Number of days to look back

        Returns:
            Tuple of (insight_text, events_count)
        """
        # Fetch recent events with eager loading of relationships
        cutoff_date = datetime.now() - timedelta(days=time_range_days)
        result = await db.execute(
            select(Event)
            .options(
                selectinload(Event.meal),
                selectinload(Event.exercise),
                selectinload(Event.symptom)
            )
            .where(Event.timestamp >= cutoff_date)
            .order_by(Event.timestamp.desc())
        )
        events = result.scalars().all()

        if not events:
            return "No recent events to analyze. Start logging meals, exercises, and symptoms!", 0

        # Format events for AI
        events_text = self.format_events_for_analysis(events)

        # Create AI prompt
        system_prompt = """You are a helpful AI assistant specializing in gut health and wellness.
Analyze the user's recent meals, exercises, and symptoms to provide actionable insights.

Focus on:
1. Patterns between meals and symptoms (e.g., certain foods causing issues)
2. Timing of symptoms relative to meals
3. Positive trends (e.g., exercises that correlate with fewer symptoms)
4. Nutritional balance and recommendations
5. Suggestions for tracking or lifestyle changes

Be concise, supportive, and actionable. Limit response to 3-4 sentences."""

        user_prompt = f"""Here are my recent health events from the past {time_range_days} days:

{events_text}

Please analyze these events and provide insights about patterns, potential triggers, and recommendations."""

        # Call OpenAI API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )

            insight_text = response.choices[0].message.content
            return insight_text, len(events)

        except Exception as e:
            raise Exception(f"Error generating AI insight: {str(e)}")

    async def save_insight(
        self,
        db: AsyncSession,
        insight_text: str
    ) -> AIInsight:
        """
        Save generated insight to database.

        Args:
            db: Database session
            insight_text: The insight text to save

        Returns:
            The saved AIInsight object
        """
        new_insight = AIInsight(
            timestamp=datetime.now(),
            description=insight_text
        )

        db.add(new_insight)
        await db.commit()
        await db.refresh(new_insight)

        return new_insight

    async def get_recent_insights(
        self,
        db: AsyncSession,
        limit: int = 10
    ) -> list[AIInsight]:
        """
        Retrieve recent AI insights.

        Args:
            db: Database session
            limit: Maximum number of insights to return

        Returns:
            List of AIInsight objects
        """
        result = await db.execute(
            select(AIInsight)
            .order_by(AIInsight.timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()
