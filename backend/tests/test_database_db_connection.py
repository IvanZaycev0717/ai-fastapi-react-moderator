from typing import AsyncGenerator

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database.db_connection import get_db_session, get_engine


async def test_get_engine():
    engine = get_engine()
    assert isinstance(engine, AsyncEngine) is True


async def test_get_db_session():
    session = get_db_session()
    assert isinstance(session, AsyncGenerator) is True
