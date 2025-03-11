from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.comments import (create_comment, delete_comment, get_all_comments,
                           get_one_comment, update_comment)
from models.comments import Comment
from services.utils import get_current_date
from tests.conftest import generic, generic_number


async def assert_comments_table_is_emplty(db_session: AsyncSession):
    async with db_session as session:
        result = await session.execute(select(Comment))
    assert result.all() == []


async def test_create_comment_successful(
        db_session_test,
        usernames_test,
        original_texts_test):
    await assert_comments_table_is_emplty(db_session_test)
    comment_id = await create_comment(
        db_session=db_session_test,
        username=usernames_test[0],
        original_text=original_texts_test[0],
        censored_text=original_texts_test[0],
        is_toxic=True,
        was_moderated=False,
        date=get_current_date()
    )
    async with db_session_test as session:
        comment = await session.scalar(select(Comment))

    assert comment_id == 1
    assert isinstance(comment, Comment) is True


async def test_create_comment_failed(
        db_session_test,
        usernames_test):
    await assert_comments_table_is_emplty(db_session_test)
    try:
        await create_comment(
            db_session=db_session_test,
            username=usernames_test[0],
        )
    except TypeError as e:
        assert isinstance(e, TypeError) is True
        async with db_session_test as session:
            result = (await session.scalars(select(Comment))).all()
            assert result == []


async def test_get_all_comments(db_session_test, fill_database_with_comments):
    comments = await get_all_comments(db_session_test)
    assert len(comments) == generic_number
    for comment in comments:
        assert isinstance(comment, Comment) is True


async def test_get_one_comment(db_session_test, fill_database_with_comments):
    comment_id = 1
    comment = await get_one_comment(db_session_test, comment_id)
    assert isinstance(comment, Comment) is True
    assert comment.id == 1


async def test_update_comment(db_session_test, fill_database_with_comments):
    is_toxic = True
    was_moderated = True
    comment_id = 1
    edited_text = generic.text.sentence()
    before_updating_comment = await get_one_comment(
        db_session_test, comment_id)
    updated_comment = await update_comment(
        db_session=db_session_test,
        comment_id=comment_id,
        original_text=edited_text,
        censored_text=edited_text,
        is_toxic=is_toxic,
        was_moderated=was_moderated)
    after_updating_comment = await get_one_comment(db_session_test, comment_id)
    assert updated_comment is True
    assert before_updating_comment.id == after_updating_comment.id
    assert before_updating_comment.username == after_updating_comment.username
    assert before_updating_comment != after_updating_comment


async def test_delete_all_comments(db_session_test):
    for id_ in range(generic_number):
        await delete_comment(db_session_test, id_ + 1)
    comments = await get_all_comments(db_session_test)
    assert comments == []
