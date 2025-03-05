from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

from settings import MAX_COMMENT_LENGTH, MAX_USERNAME_LENGTH


class Base(DeclarativeBase):
    pass


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(MAX_USERNAME_LENGTH),
        nullable=False,
        index=True)
    original_text: Mapped[str] = mapped_column(
        String(MAX_COMMENT_LENGTH),
        nullable=False)
    censored_text: Mapped[str] = mapped_column(
        String(MAX_COMMENT_LENGTH),
        nullable=True)
    is_toxic: Mapped[bool] = mapped_column(index=True)
    was_moderated: Mapped[bool] = mapped_column(index=True)
    date: Mapped[datetime] = mapped_column(index=True)
