import contextlib
import logging
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database.exceptions import DatabaseSessionManagerError
from app.database.models import Base


class DatabaseSessionManager:
    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.sessionmaker: async_sessionmaker | None = None

    def init(self, host: str) -> None:
        self.engine = create_async_engine(host)
        self.sessionmaker = async_sessionmaker(
            autocommit=False, bind=self.engine
        )

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if not self.engine:
            raise DatabaseSessionManagerError("Engine is not initialized")

        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception as error:
                logging.error(error)

                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self.sessionmaker:
            raise DatabaseSessionManagerError("Sessionmaker is not initialized")

        session = self.sessionmaker()

        try:
            yield session
        except Exception as error:
            logging.error(error)

            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self) -> None:
        if not self.engine:
            raise DatabaseSessionManagerError("Engine is not initialized")

        await self.engine.dispose()

        self.engine = None
        self.sessionmaker = None

    async def create_all(self, connection: AsyncConnection) -> None:
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection) -> None:
        await connection.run_sync(Base.metadata.drop_all)

    @staticmethod
    def get_instance() -> "DatabaseSessionManager":
        if not hasattr(DatabaseSessionManager, "_instance"):
            DatabaseSessionManager._instance = DatabaseSessionManager()
        return DatabaseSessionManager._instance


session_manager = DatabaseSessionManager()
