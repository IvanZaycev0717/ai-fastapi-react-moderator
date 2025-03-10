import json

import pytest
from httpx import ASGITransport, AsyncClient
from mimesis import Generic, Locale
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database.db_connection import get_db_session
from main import app
from models.comments import Base, Comment
from services.utils import get_current_date
from settings import BACKEND_URL, SQLALCHEMY_TEST_DATABASE_URI

generic = Generic(locale=Locale.RU)
generic_number = 5


@pytest.fixture
def db_engine_test():
    return create_async_engine(SQLALCHEMY_TEST_DATABASE_URI)


@pytest.fixture
async def usernames_test(users_number: int = generic_number):
    return [generic.person.username() for _ in range(users_number)]


@pytest.fixture
async def original_texts_test(texts_number: int = generic_number):
    return [generic.text.sentence() for _ in range(texts_number)]


@pytest.fixture
async def db_session_test(
    db_engine_test,
):
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
async def test_client(db_session_test):
    app.dependency_overrides[get_db_session] = (lambda: db_session_test)
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url=BACKEND_URL
        )


@pytest.fixture
async def fill_database_with_comments(db_session_test,
                                      usernames_test,
                                      original_texts_test):
    comments = []
    for i in range(generic_number):
        comment = Comment(
            username=usernames_test[i],
            original_text=original_texts_test[i],
            censored_text=original_texts_test[i],
            is_toxic=False,
            was_moderated=False,
            date=get_current_date())
        comments.append(comment)
    async with db_session_test.begin():
        db_session_test.add_all(comments)
        await db_session_test.commit()


@pytest.fixture
async def get_comment_data_in_json(usernames_test, original_texts_test):
    return json.dumps(
        {'username': usernames_test[0],
         'original_text': original_texts_test[0]}
         )


@pytest.fixture
async def get_empty_json():
    return json.dumps({})


@pytest.fixture
async def get_json_for_comment_updating():
    return json.dumps({'edited_text': generic.text.answer()})
