from mimesis import Generic, Locale
from pydantic import BaseModel, Field


from settings import (
    MAX_COMMENT_LENGTH,
    MAX_USERNAME_LENGTH,
    MIN_COMMENT_LENGTH,
    MIN_USERNAME_LENGTH
    )

generic = Generic(Locale.RU)


class CreateCommentRequest(BaseModel):
    username: str = Field(
        ...,
        max_length=MAX_USERNAME_LENGTH,
        min_length=MIN_USERNAME_LENGTH,
        title='Имя пользователя',
        examples=[generic.person.username()])
    original_text: str = Field(
        ...,
        max_length=MAX_COMMENT_LENGTH,
        min_length=MIN_COMMENT_LENGTH,
        title='Оригинальный текст комментария',
        description='Текст нового комментарий до модерации ИИ',
        examples=[generic.text.sentence()]
        )


class UpdateCommentRequest(BaseModel):
    edited_text: str = Field(
        ...,
        max_length=MAX_COMMENT_LENGTH,
        min_length=MIN_COMMENT_LENGTH,
        title='Отредактированный текст комментария',
        description='Отредактированный текст комментария до модерации ИИ',
        examples=[generic.text.sentence()]
        )
