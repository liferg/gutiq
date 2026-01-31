from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://localhost/gutiq"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # logs SQL for learning/debugging
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


# Dependency to get database session
async def get_db():
    """
    FastAPI dependency that provides a database session.
    Automatically closes the session when the request is complete.
    """
    async with AsyncSessionLocal() as session:
        yield session
