from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.db_connection import get_engine
from models.comments import Base
from routes import comments
from settings import APP_CONTACT, APP_DESCRIPTION, APP_TITLE, FRONTEND_URL


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управляет жизненным циклом приложения FastAPI."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    contact=APP_CONTACT,
    lifespan=lifespan)

app.include_router(comments.router)

origins = [FRONTEND_URL, ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Перехватывает исключения типа HTTPException и возвращает
    JSON-ответ с соответствующим статусом и сообщением.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail})
