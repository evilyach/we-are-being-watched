from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.session import session_manager
from app.main import init_app


@pytest_asyncio.fixture()
async def session() -> AsyncGenerator[AsyncSession, None]:
    session_manager.init(settings.TEST_DB_CONFIG)

    async with session_manager.connect() as connection:
        await session_manager.drop_all(connection)
        await session_manager.create_all(connection)

    async with session_manager.session() as session:
        yield session

    await session_manager.close()


@pytest.fixture()
def test_app() -> FastAPI:
    app = init_app(init_db=False)
    return app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=test_app, base_url="http://test.com") as client:
        yield client
