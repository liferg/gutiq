"""
Configuration settings for GutIQ backend application.
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str

    # Database Configuration (for future use)
    database_url: str = "postgresql+asyncpg://localhost/gutiq"

    # API Configuration
    api_title: str = "GutIQ API"
    api_version: str = "1.0.0"

    # CORS Configuration
    frontend_url: str = "http://localhost:5173"

    # AI Insights Configuration
    insight_meal_threshold: int = 3  # Generate insight after every N meal events

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to create a singleton pattern - settings are loaded once.
    """
    return Settings()
