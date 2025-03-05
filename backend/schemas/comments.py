
from pydantic import BaseModel, Field


from settings import (
    MAX_COMMENT_LENGTH,
    MAX_USERNAME_LENGTH,
    MIN_COMMENT_LENGTH,
    MIN_USERNAME_LENGTH
    )


class CreateCommentRequest(BaseModel):
    username: str = Field(
        ...,
        max_length=MAX_USERNAME_LENGTH,
        min_length=MIN_USERNAME_LENGTH)
    original_text: str = Field(
        ...,
        max_length=MAX_COMMENT_LENGTH,
        min_length=MIN_COMMENT_LENGTH
        )


class UpdateCommentRequest(BaseModel):
    edited_text: str = Field(
        ...,
        max_length=MAX_COMMENT_LENGTH,
        min_length=MIN_COMMENT_LENGTH
        )
