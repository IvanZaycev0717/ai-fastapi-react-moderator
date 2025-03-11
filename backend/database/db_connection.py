from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import SQLAlCHEMY_DATABASE_URI


def get_engine():
    """Создаёт асинхронный движок для работы с базой данных."""
    return create_async_engine(SQLAlCHEMY_DATABASE_URI)


AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine(),
    class_=AsyncSession,
)


async def get_db_session():
    """Генерирует сесссии для работы с базой данных."""
    async with AsyncSessionLocal() as session:
        yield session
