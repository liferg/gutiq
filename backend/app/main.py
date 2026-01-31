from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import events, ai_insights
from app.config import get_settings

# Load settings
settings = get_settings()

app = FastAPI(title=settings.api_title, version=settings.api_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(events.router)
app.include_router(ai_insights.router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "openai_configured": bool(settings.openai_api_key)
    }
