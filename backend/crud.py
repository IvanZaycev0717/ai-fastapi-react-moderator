from datetime import datetime
from typing import Any
from sqlalchemy import (delete, select, update)
from sqlalchemy.ext.asyncio import AsyncSession

from models import Comment


# CREATE
async def create_comment(
        db_session: AsyncSession,
        username: str,
        original: str,
        censored: str,
        is_toxic: bool,
        date: datetime) -> str:
    comment = Comment(
        username=username,
        original=original,
        censored=censored,
        is_toxic=is_toxic,
        date=date)
    async with db_session.begin():
        db_session.add(comment)
        await db_session.flush()
        comment_id = comment.id
        await db_session.commit()
    return f'Comment with id={comment_id} was successfully created'


# READ
async def get_all_comments(db_session: AsyncSession) -> list[tuple[Comment]] | Any:
    query = select(Comment)
    async with db_session as session:
        comments = await session.execute(query)
        return comments.scalars().all()


async def get_one_comment(
        db_session: AsyncSession,
        comment_id: int) -> Comment | None:
    query = select(Comment).where(Comment.id == comment_id)
    async with db_session as session:
        comments = await session.execute(query)
        return comments.scalars().first()


# UPDATE
async def update_comment(
        db_session: AsyncSession,
        comment_id: int,
        original: str | None,
        censored: str | None,
        is_toxic: bool) -> str:
    query = update(Comment).where(Comment.id == comment_id).values(
        original=original,
        censored=censored,
        is_toxic=is_toxic
        )
    async with db_session as session:
        comment_updated = await session.execute(query)
        await session.commit()
        if comment_updated.rowcount == 0:
            return f'FAILED to update comment with id={comment_id}'
        return f'SUCCESS! Comment with id={comment_id} updated'


# DELETE
async def delete_comment(db_session: AsyncSession, comment_id: int) -> str:
    async with db_session as session:
        query = delete(Comment).where(Comment.id == comment_id)
        comment_deleted = await session.execute(query)
        await session.commit()
        if comment_deleted.rowcount == 0:
            return f'FAILED to delete comment with id={comment_id}'
        return f'SUCCESS! Comment with id={comment_id} deleted'
