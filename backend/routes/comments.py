from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession


from schemas.comments import CreateCommentRequest, UpdateCommentRequest
from database.db_connection import get_db_session
from crud.comments import (
    get_all_comments,
    get_one_comment,
    create_comment,
    delete_comment,
    update_comment
    )
from services.utils import get_current_date
from settings import IS_AI_MODERATION_ENABLED

router = APIRouter(prefix='/comments', tags=['comments'])


# FETCH COMMENT(S) ENDPOINTS
@router.get('/', name='Получить все комментарии')
async def get_all_comments_endpoint(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
        ):
    """
    **Получить все комментарии.**

    Этот эндпоинт возвращает список всех комментариев из базы данных.
    Если комментариев нет, будет возвращен статус 204 (Нет содержимого).

    - **Args:**
        - **db_session (AsyncSession):** Асинхронная сессия базы данных
        для выполнения запросов.

    - **Raises:**
        - **HTTPException:** Если комментарии отсутствуют,
        будет выброшено исключение
        с кодом статуса 204 и сообщением 'There are NO comments yet'.

    - **Returns:**
        - **List[Comment]:** Список комментариев, если они существуют.
    """
    comments = await get_all_comments(db_session)
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail='There are NO comments yet'
            )
    return comments


@router.get('/{comment_id}', name='Получить один комментарий по его ID')
async def get_one_comment_endpoint(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    comment_id: int = Path(
        description='Введите ID комментария, который хотите получить')
        ):
    """
    **Получить один комментарий по его ID.**

    Этот эндпоинт возвращает комментарий из базы данных по указанному ID.
    Если комментарий с данным ID не найден,
    будет возвращен статус 404 (Не найдено).

    - **Args:**
        - **db_session (AsyncSession):** Асинхронная сессия базы данных
        для выполнения запросов.
        - **comment_id (int):** Уникальный идентификатор комментария,
        который необходимо получить.

    - **Raises:**
        - **HTTPException**: Если комментарий с данным ID не найден,
        будет выброшено исключение
        с кодом статуса 404 и сообщением 'Comment not found'.

    - **Returns:**
        - **Comment:** Комментарий с указанным ID, если он существует.
    """
    comment = await get_one_comment(db_session, comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
            )
    return comment


# CREATE COMMENT ENDPOINT
@router.post('/',
             response_model=dict[str, int],
             status_code=status.HTTP_201_CREATED,
             name='Создать новый комментарий')
async def create_comment_endpoint(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    comment: CreateCommentRequest = Body()
        ):
    if not IS_AI_MODERATION_ENABLED:
        censored_text = comment.original_text
        was_moderated = False
    is_toxic = True
    comment_id = await create_comment(
        db_session=db_session,
        username=comment.username,
        original_text=comment.original_text,
        censored_text=censored_text,
        is_toxic=is_toxic,
        was_moderated=was_moderated,
        date=get_current_date()
    )
    return {'comment_id': comment_id}


# UPDATE COMMENT ENDPOINT
@router.patch('/{comment_id}', name='Обновить текст комментария по его ID')
async def update_comment_endpoint(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    comment_id: int = Path(
        description='Введите ID комментария для редактирования'),
    edited_text: UpdateCommentRequest = Body(
        description='Напишите отредактированный текст комментария'
        )
        ):
    edited_content = edited_text.model_dump()['edited_text']
    if not IS_AI_MODERATION_ENABLED:
        censored_text = edited_content
        was_moderated = False
    updated_comment = await update_comment(
        db_session=db_session,
        comment_id=comment_id,
        original_text=edited_content,
        censored_text=censored_text,
        is_toxic=True,
        was_moderated=was_moderated,
        )
    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
            )
    return {'detail': 'Comment was updated'}


# DELETE COMMENT ENDPOINT
@router.delete('/{comment_id}', name='Удалить комментарий по его ID')
async def delete_comment_endpoint(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    comment_id: int = Path(
        title='ID комментария на удаление',
        description='Удаляет комментарий по его ID')
        ):
    """
    **Удалить комментарий по его ID.**

    Этот эндпоинт позволяет удалить комментарий
    из базы данных по указанному ID.
    Если комментарий с данным ID не найден,
    будет возвращен статус 404 (Не найдено).

    - **Args:**
        - **db_session (AsyncSession)**: Асинхронная сессия базы данных
        для выполнения запросов.
        - **comment_id (int)**: Уникальный идентификатор комментария,
        который необходимо удалить.

    - **Raises:**
        - **HTTPException**: Если комментарий с данным ID не найден,
        будет выброшено исключение 
        с кодом статуса 404 и сообщением 'Comment not found'.

    - **Returns:**
        - **dict:** Словарь с сообщением о том, что комментарий был успешно удален.
    """
    comment = await delete_comment(db_session, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )
    return {'detail': f'Comment with id={comment_id} deleted'}
