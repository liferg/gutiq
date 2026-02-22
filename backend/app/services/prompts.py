"""
AI prompt templates for GutIQ.
Centralized location for all OpenAI prompts to make them easy to iterate on.
"""

# System prompt for insight generation
INSIGHT_GENERATION_SYSTEM_PROMPT = """You are a helpful AI assistant specializing in gut health and wellness.
Analyze the user's recent meals, exercises, and symptoms to provide actionable insights.

Focus on:
1. Patterns between meals and symptoms (e.g., certain foods causing issues)
2. Timing of symptoms relative to meals
3. Positive trends (e.g., exercises that correlate with fewer symptoms)
4. Nutritional balance and recommendations
5. Suggestions for tracking or lifestyle changes

Be concise, supportive, and actionable. Limit response to 3-4 sentences."""


def get_insight_generation_user_prompt(events_text: str, time_range_days: int) -> str:
    """
    Generate user prompt for insight generation.

    Args:
        events_text: Formatted string of user events
        time_range_days: Number of days analyzed

    Returns:
        Formatted user prompt
    """
    return f"""Here are my recent health events from the past {time_range_days} days:

{events_text}

Please analyze these events and provide insights about patterns, potential triggers, and recommendations."""
