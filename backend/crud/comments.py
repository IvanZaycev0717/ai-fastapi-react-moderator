from datetime import datetime


from sqlalchemy import (delete, select, update)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only


from models.comments import Comment


# CREATE
async def create_comment(
        db_session: AsyncSession,
        username: str,
        original_text: str,
        censored_text: str,
        is_toxic: bool,
        was_moderated: bool,
        date: datetime) -> int:
    """Создаёт новый комментарий в базе данных."""
    comment = Comment(
        username=username,
        original_text=original_text,
        censored_text=censored_text,
        is_toxic=is_toxic,
        was_moderated=was_moderated,
        date=date)
    async with db_session.begin():
        db_session.add(comment)
        await db_session.flush()
        comment_id = comment.id
        await db_session.commit()
    return comment_id


# READ
async def get_all_comments(
        db_session: AsyncSession) -> list[Comment | None]:
    """Извлекает все комментарии из базы данных."""
    query = select(Comment).options(
        load_only(Comment.username, Comment.censored_text, Comment.date))
    async with db_session as session:
        return (await session.scalars(query)).all()


async def get_one_comment(
        db_session: AsyncSession,
        comment_id: int) -> Comment | None:
    """Извлекает один комментарий из базы данных по его ID."""
    query = select(Comment).where(Comment.id == comment_id).options(
        load_only(Comment.username, Comment.censored_text))
    async with db_session as session:
        return await session.scalar(query)


# UPDATE
async def update_comment(
        db_session: AsyncSession,
        comment_id: int,
        original_text: str | None,
        censored_text: str | None,
        is_toxic: bool,
        was_moderated: bool) -> bool:
    """Обновляет один комментарий в базе данных по его ID."""
    query = update(Comment).where(Comment.id == comment_id).values(
        original_text=original_text,
        censored_text=censored_text,
        is_toxic=is_toxic,
        was_moderated=was_moderated,
        )
    async with db_session as session:
        comment_updated = await session.execute(query)
        await session.commit()
        if comment_updated.rowcount == 0:
            return False
        return True


# DELETE
async def delete_comment(db_session: AsyncSession, comment_id: int) -> bool:
    """Удаляет один комментарий из базы данных по его ID."""
    async with db_session as session:
        query = delete(Comment).where(Comment.id == comment_id)
        comment_deleted = await session.execute(query)
        await session.commit()
        if comment_deleted.rowcount == 0:
            return False
        return True
