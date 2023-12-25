from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from app.config import settings
from app.database.session import session_manager
from app.visits.api import visits_router


@asynccontextmanager
async def get_lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    yield

    if session_manager.engine:
        await session_manager.close()


def init_app(init_db: bool = True) -> FastAPI:
    lifespan = None

    if init_db:
        session_manager.init(settings.DB_CONFIG)
        lifespan = get_lifespan

    server = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
    server.include_router(visits_router)

    return server
