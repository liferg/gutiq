"""
Example of how to use OpenAI API with the loaded configuration.
This demonstrates accessing the API key from settings.
"""

from app.config import get_settings
from openai import OpenAI


def example_openai_client():
    """Create an OpenAI client using settings from config."""
    settings = get_settings()

    # Initialize OpenAI client with API key from settings
    client = OpenAI(api_key=settings.openai_api_key)

    return client


def example_chat_completion():
    """Example of generating a chat completion."""
    client = example_openai_client()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello!"}
            ],
            max_tokens=50
        )

        print("Response:", response.choices[0].message.content)
        return response

    except Exception as e:
        print(f"Error: {e}")
        return None


def example_with_event_data():
    """Example of using OpenAI to analyze GutIQ event data."""
    client = example_openai_client()

    # Example event data
    event_description = """
    User logged:
    - Meal: greek yogurt, banana, granola (350 calories, 15g protein)
    - Symptom 2 hours later: moderate bloating
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant analyzing gut health patterns."
                },
                {
                    "role": "user",
                    "content": f"Analyze this event and provide a brief insight:\n\n{event_description}"
                }
            ],
            max_tokens=150
        )

        print("AI Insight:", response.choices[0].message.content)
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    print("Testing OpenAI integration...")
    print("\n1. Simple chat completion:")
    example_chat_completion()

    print("\n2. Event analysis:")
    example_with_event_data()
