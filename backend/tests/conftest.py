import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


from db_connection import get_db_session
from main import app
from models import Base, Comment
from settings import SQLALCHEMY_TEST_DATABASE_URL
from tests.fixtures import NOT_TOXIC_COMMENTS_LIST
from utils import get_current_date


@pytest.fixture
def db_engine_test():
    engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)
    return engine


@pytest.fixture
async def db_session_test(db_engine_test):
    TestingAsynSessionLocal = sessionmaker(
        bind=db_engine_test, class_=AsyncSession
    )
    async with db_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        async with TestingAsynSessionLocal() as session:
            yield session

        await conn.run_sync(Base.metadata.drop_all)
    await db_engine_test.dispose()


@pytest.fixture
def test_client(db_session_test):
    client = TestClient(app=app)
    app.dependency_overrides[get_db_session] = (
        lambda: db_session_test
    )
    return client


@pytest.fixture
async def fill_database_with_NOT_toxic_comments(db_session_test):
    comments = [
        Comment(
            username=f'user{i}',
            original_text=NOT_TOXIC_COMMENTS_LIST[i],
            is_toxic=False,
            date=get_current_date()) for i in range(5)
        ]
    async with db_session_test.begin():
        db_session_test.add_all(comments)
        await db_session_test.commit()


@pytest.fixture
async def fill_database_with_toxic_comments(db_session_test):
    pass
