from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from schemas.comments import CommentsRequest
from database.db_connection import get_db_session
from crud.comments import (
    get_all_comments,
    get_one_comment,
    create_comment,
    delete_comment
    )
from services.utils import get_current_date

router = APIRouter(prefix='/comments', tags=['comments'])


# FETCH COMMENT(S) ENDPOINTS
@router.get('/')
async def get_all_comments_endpoint(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
        ):
    comments = await get_all_comments(db_session)
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail='There are NO comments yet'
            )
    return comments


@router.get('/{comment_id}')
async def get_one_comment_endpoint(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    comment_id: int
        ):
    comment = await get_one_comment(db_session, comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
            )
    return comment


# CREATE COMMENT ENDPOINT
@router.post('/', response_model=dict[str, int])
async def create_comment_endpoint(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    comment: CommentsRequest
        ):
    censored_text = "ERROR"
    is_toxic = True
    comment_id = await create_comment(
        db_session=db_session,
        username=comment.username,
        original_text=comment.original_text,
        censored_text=censored_text,
        is_toxic=is_toxic,
        date=get_current_date()
    )
    return {'comment_id': comment_id}

# UPDATE


# DELETE
@router.delete('/{comment_id}')
async def delete_comment_endpoint(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    comment_id: int
        ):
    comment = await delete_comment(db_session, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )
    return {'detail': f'Comment with id={comment_id} deleted'}
