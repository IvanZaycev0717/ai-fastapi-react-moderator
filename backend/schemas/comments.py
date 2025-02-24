from datetime import datetime

from typing import Optional
from pydantic import BaseModel, Field

from settings import (
    MAX_COMMENT_LENGTH,
    MAX_USERNAME_LENGTH,
    MIN_COMMENT_LENGTH,
    MIN_USERNAME_LENGTH
    )
from services.utils import get_current_date


class CommentsRequest(BaseModel):
    username: str = Field(
        ...,
        max_length=MAX_USERNAME_LENGTH,
        min_length=MIN_USERNAME_LENGTH)
    original_text: str = Field(
        ...,
        max_length=MAX_COMMENT_LENGTH,
        min_length=MIN_COMMENT_LENGTH
        )


class CommentSchema(CommentsRequest):
    censored_text: Optional[str] = Field(
        None,
        max_length=MAX_COMMENT_LENGTH,
        min_length=MIN_COMMENT_LENGTH
        )
    is_toxic: bool
    date: datetime = Field(default_factory=get_current_date)
