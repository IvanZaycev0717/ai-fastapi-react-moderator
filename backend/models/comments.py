from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

from settings import COMMENT_LENGTH, USERNAME_LENGTH


class Base(DeclarativeBase):
    pass


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(USERNAME_LENGTH),
        nullable=False,
        index=True)
    original_text: Mapped[str] = mapped_column(
        String(COMMENT_LENGTH),
        nullable=False)
    censored_text: Mapped[str] = mapped_column(
        String(COMMENT_LENGTH),
        nullable=True)
    is_toxic: Mapped[bool] = mapped_column(index=True)
    date: Mapped[datetime] = mapped_column(index=True)
