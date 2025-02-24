from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker

from settings import SQLAlCHEMY_DATABASE_URL


def get_engine():
    return create_async_engine(SQLAlCHEMY_DATABASE_URL)


AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine(),
    class_=AsyncSession,
)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
