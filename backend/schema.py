from datetime import datetime

from typing import Optional
from pydantic import BaseModel, Field

from settings import COMMENT_LENGTH, USERNAME_LENGTH
from utils import get_current_date


class CommentSchema(BaseModel):
    id: int
    username: str = Field(..., max_length=USERNAME_LENGTH)
    original: str = Field(..., max_length=COMMENT_LENGTH)
    censored: Optional[str] = Field(None, max_length=COMMENT_LENGTH)
    is_toxic: bool
    date: datetime = Field(default_factory=get_current_date)