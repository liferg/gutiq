import asyncio
from datetime import datetime
from app.db.database import AsyncSessionLocal
from app.db.models import Event

async def test_insert():
    async with AsyncSessionLocal() as session:
        event = Event(
            timestamp=datetime.utcnow(),
            event_type="Meal",
        )
        session.add(event)
        await session.commit()
        print("Inserted event:", event.event_id)

asyncio.run(test_insert())
