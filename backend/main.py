from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.db_connection import get_engine
from models.comments import Base
from routes import comments
from services.log_handlers import client_logger
from settings import (APP_CONTACT, APP_DESCRIPTION,
                      APP_TITLE, FRONTEND_URL, OPEN_API_ACCESS)


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
    lifespan=lifespan,
    openapi_url=OPEN_API_ACCESS)

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
    """Обрабатывает исключения в приложении."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail})


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Логирует все события в консоль и в файл."""
    client_logger.info(
        f"method: {request.method}, "
        f"call: {request.url.path}, "
        f"ip: {request.client.host}"
    )
    response = await call_next(request)
    return response
