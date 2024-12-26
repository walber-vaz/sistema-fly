from collections.abc import AsyncIterator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

from app.config import settings
from app.constants import DB_NAMING_CONVENTION, Environment

metadata: MetaData = MetaData(naming_convention=DB_NAMING_CONVENTION)
table_registry = registry(metadata=metadata)
engine = create_async_engine(
    settings.DATABASE_URL, echo=settings.ENVIRONMENT == Environment.LOCAL, future=True
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
