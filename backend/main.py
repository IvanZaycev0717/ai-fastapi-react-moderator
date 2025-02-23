from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schema import CommentSchema
from models import Base
from db_connection import get_engine, get_db_session
from crud import (get_all_comments,
                  get_one_comment,
                  create_comment,
                  delete_comment)
from utils import get_current_date


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)


# FETCH COMMENT(S) ENDPOINTS
@app.get('/comments')
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


@app.get('/comments/{comment_id}')
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
@app.post('/comments', response_model=dict[str, int])
async def create_comment_endpoint(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    comment: CommentSchema
        ):
    comment_id = await create_comment(
        db_session=db_session,
        username=comment.username,
        original_text=comment.original_text,
        censored_text=comment.censored_text,
        is_toxic=comment.is_toxic,
        date=get_current_date()
    )
    return {'comment_id': comment_id}

# UPDATE


# DELETE
@app.delete('/comments/{comment_id}')
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
