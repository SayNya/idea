from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import settings

_async_engine = create_async_engine(
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:5432/{settings.DB_NAME}",
    echo=True,
)
async_session = sessionmaker(_async_engine, class_=AsyncSession, expire_on_commit=False)


db_session: ContextVar[AsyncSession] = ContextVar("db_session")
