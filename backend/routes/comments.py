from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
import yandex_cloud_ml_sdk

from crud.comments import (create_comment, delete_comment, get_all_comments,
                           get_one_comment, update_comment)
from database.db_connection import get_db_session
from schemas.comments import CreateCommentRequest, UpdateCommentRequest
from services.utils import compare_comments, get_current_date
from services.yandexgpt_moderator import moderate_comment
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

    - **Параметры:**
        - **db_session (AsyncSession):** Асинхронная сессия базы данных
        для выполнения запросов.

    - **Исключения:**
        - **HTTPException:** Если комментарии отсутствуют,
        будет выброшено исключение
        с кодом статуса 204 и сообщением 'There are NO comments yet'.

    - **Возвращает:**
        - **List[Comment]:** Список комментариев, если они существуют.
    """
    comments = await get_all_comments(db_session)
    if not comments:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
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

    - **Параметры:**
        - **db_session (AsyncSession):** Асинхронная сессия базы данных
        для выполнения запросов.
        - **comment_id (int):** Уникальный идентификатор комментария,
        который необходимо получить.

    - **Исключения:**
        - **HTTPException**: Если комментарий с данным ID не найден,
        будет выброшено исключение
        с кодом статуса 404 и сообщением 'Comment not found'.

    - **Возвращает:**
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
    """
    **Создает новый комментарий в базе данных.**

    Эта функция обрабатывает POST-запросна создание комментария.
    В зависимости от настройки модерации, текст комментария может быть
    подвергнут цензуре. Если модерация включена, комментарий проверяется
    на токсичность и цензурируется при необходимости.

    - **Параметры**:
      - **db_session** : AsyncSession
        Асинхронная сессия базы данных для выполнения операций с базой данных.
    comment : CreateCommentRequest
        Объект, содержащий данные о комментарии, включая имя пользователя
        и оригинальный текст комментария.

    - **Возвращает**:
      - **dict[str, int]**
        Словарь, содержащий идентификатор созданного комментария
        с ключом 'comment_id'.

    - **Исключения**:
      - Возможны исключения, связанные с базой данных или процессом модерации.
    """
    if not IS_AI_MODERATION_ENABLED:
        censored_text = comment.original_text
        was_moderated = False
        is_toxic = True
    else:
        try:
            censored_text = await moderate_comment(comment.original_text)
            is_toxic = compare_comments(comment.original_text, censored_text)
            was_moderated = True
        except yandex_cloud_ml_sdk._exceptions.AioRpcError:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                                detail='YandexGPT server issue')
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
    """
    **Обновляет текст комментария по его ID.**

    Эта функция обрабатывает PATCH-запрос на обновление комментария,
    идентифицированного по его ID. В зависимости от настройки модерации,
    текст комментария может быть подвергнут цензуре. Если модерация включена,
    комментарий проверяется на токсичность и цензурируется при необходимости.

    - **Параметры:**
      - **db_session : AsyncSession**
        Асинхронная сессия базы данных для выполнения операций с базой данных.
      - **comment_id : int**
        Уникальный идентификатор комментария, который требуется обновить.
      - **edited_text : UpdateCommentRequest**
        Объект, содержащий отредактированный текст комментария.

    - **Возвращает:**
      - **dict**
        Словарь с ключом 'detail', который содержит сообщение об успешном
        обновлении комментария.

    - **Исключения:**

      - HTTPException
        Выбрасывается, если комментарий с указанным ID не найден
        (код ошибки 404).
    """
    edited_content = edited_text.model_dump()['edited_text']
    if not IS_AI_MODERATION_ENABLED:
        censored_text = edited_content
        was_moderated = False
        is_toxic = True
    else:
        try:
            censored_text = await moderate_comment(edited_content)
            is_toxic = compare_comments(edited_content, censored_text)
            was_moderated = True
        except yandex_cloud_ml_sdk._exceptions.AioRpcError:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                                detail='YandexGPT server issue')
    updated_comment = await update_comment(
        db_session=db_session,
        comment_id=comment_id,
        original_text=edited_content,
        censored_text=censored_text,
        is_toxic=is_toxic,
        was_moderated=was_moderated,
        )
    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
            )
    return {'detail': 'Comment was updated'}


# DELETE COMMENT ENDPOINT
@router.delete('/{comment_id}',
               name='Удалить комментарий по его ID')
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

    - **Параметры:**
        - **db_session (AsyncSession)**: Асинхронная сессия базы данных
        для выполнения запросов.
        - **comment_id (int)**: Уникальный идентификатор комментария,
        который необходимо удалить.

    - **Исключения:**
        - **HTTPException**: Если комментарий с данным ID не найден,
        будет выброшено исключение
        с кодом статуса 404 и сообщением 'Comment not found'.

    - **Возвращает:**
        - **dict:** Словарь с сообщением о том,
        что комментарий был успешно удален.
    """
    comment = await delete_comment(db_session, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )
    return {'detail': f'Comment with id={comment_id} deleted'}
