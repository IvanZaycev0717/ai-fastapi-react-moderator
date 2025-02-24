from contextlib import asynccontextmanager
from fastapi import FastAPI

from models.comments import Base
from database.db_connection import get_engine
from routes import comments


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)


app.include_router(comments.router)
