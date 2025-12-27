from sqlalchemy import Column, String, DateTime
from app.db.database import Base
import uuid
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False)
    event_type = Column(String, nullable=False)
