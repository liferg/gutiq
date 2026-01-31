"""
API endpoints for AI insights generation and retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.ai_insights import (
    AIInsightResponse,
    GenerateInsightRequest,
    GenerateInsightResponse
)
from app.services.ai_service import AIService
from datetime import datetime


router = APIRouter(prefix="/ai-insights", tags=["AI Insights"])


@router.post("/generate", response_model=GenerateInsightResponse, status_code=201)
async def generate_insight(
    request: GenerateInsightRequest = GenerateInsightRequest(),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate an AI insight based on recent user events.

    Analyzes meals, exercises, and symptoms to identify patterns and provide recommendations.
    The insight is automatically saved to the database.
    """
    ai_service = AIService()

    try:
        # Generate insight using AI
        insight_text, events_count = await ai_service.generate_insight(
            db=db,
            time_range_days=request.time_range_days
        )

        # Save insight to database
        saved_insight = await ai_service.save_insight(
            db=db,
            insight_text=insight_text
        )

        return GenerateInsightResponse(
            insight=insight_text,
            saved_insight_id=saved_insight.id,
            events_analyzed=events_count,
            timestamp=saved_insight.timestamp
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate insight: {str(e)}"
        )


@router.get("/", response_model=list[AIInsightResponse])
async def get_insights(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve recent AI insights.

    Args:
        limit: Maximum number of insights to return (default: 10)
    """
    ai_service = AIService()

    try:
        insights = await ai_service.get_recent_insights(db=db, limit=limit)
        return insights

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve insights: {str(e)}"
        )


@router.get("/{insight_id}", response_model=AIInsightResponse)
async def get_insight(
    insight_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a specific AI insight by ID.
    """
    from sqlalchemy import select
    from app.db.models import AIInsight

    result = await db.execute(
        select(AIInsight).where(AIInsight.id == insight_id)
    )
    insight = result.scalar_one_or_none()

    if not insight:
        raise HTTPException(
            status_code=404,
            detail=f"Insight with ID {insight_id} not found"
        )

    return insight
