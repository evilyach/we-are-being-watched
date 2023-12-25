from datetime import datetime
from typing import Self
from unittest.mock import patch

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.visits.models import Visit


class TestCreateVisitEntrypoint:
    @pytest.mark.asyncio
    async def test_success(
        self: Self, client: AsyncClient, session: AsyncSession
    ) -> None:
        # Arrange
        body = {"links": ["https://sber.ru/"]}

        # Act
        response = await client.post("/visited_links", json=body)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

        in_db = list((await session.execute(select(Visit))).scalars().all())
        assert len(in_db) == 1

        visit = in_db[0]
        assert visit.link == "https://sber.ru/"

    @pytest.mark.asyncio
    async def test_success_for_multiple_links(
        self: Self, client: AsyncClient, session: AsyncSession
    ) -> None:
        # Arrange
        body = {"links": [f"https://link{i}.ru/" for i in range(100)]}

        # Act
        response = await client.post("/visited_links", json=body)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

        in_db = list((await session.execute(select(Visit))).scalars().all())
        assert len(in_db) == 100

    @pytest.mark.asyncio
    async def test_fail_if_no_links_were_privided(
        self: Self, client: AsyncClient
    ) -> None:
        # Arrange
        body = {"links": []}

        # Act
        response = await client.post("/visited_links", json=body)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_fail_if_no_body_were_privided(
        self: Self, client: AsyncClient
    ) -> None:
        # Act
        response = await client.post("/visited_links")

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetVisitsEntrypoint:
    @pytest.mark.asyncio
    async def test_success(
        self: Self, client: AsyncClient, session: AsyncSession
    ) -> None:
        # Arrange
        visit = Visit(link="https://sber.ru/")
        session.add(visit)
        await session.flush()

        # Act
        with patch("app.visits.queries.session_manager.session") as patched:
            patched.return_value = session

            response = await client.get("/visited_links")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("domains") == ["https://sber.ru/"]
        assert response.json().get("status") == "ok"

    @pytest.mark.asyncio
    async def test_success_for_multiple_links(
        self: Self, client: AsyncClient, session: AsyncSession
    ) -> None:
        # Arrange
        session.add_all(
            [Visit(link=f"https://link{i}.ru/") for i in range(100)]
        )
        await session.flush()

        # Act
        with patch("app.visits.queries.session_manager.session") as patched:
            patched.return_value = session

            response = await client.get("/visited_links")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("domains")) == 100

    @pytest.mark.asyncio
    async def test_success_if_no_links_are_present(
        self: Self, client: AsyncClient, session: AsyncSession
    ) -> None:
        # Act
        with patch("app.visits.queries.session_manager.session") as patched:
            patched.return_value = session

            response = await client.get("/visited_links")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("domains") == []
        assert response.json().get("status") == "ok"

    @pytest.mark.asyncio
    async def test_success_if_from_date_provided(
        self: Self, client: AsyncClient, session: AsyncSession
    ) -> None:
        # Arrange
        timestamp = 1545221231

        visit1 = Visit(
            link="https://link1.ru/",
            created_at=datetime.fromtimestamp(timestamp - 1000),
        )
        visit2 = Visit(
            link="https://link2.ru/",
            created_at=datetime.fromtimestamp(timestamp + 1000),
        )
        session.add_all([visit1, visit2])
        await session.flush()

        # Act
        with patch("app.visits.queries.session_manager.session") as patched:
            patched.return_value = session

            response = await client.get(f"/visited_links?from={timestamp}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("domains") == ["https://link2.ru/"]
        assert response.json().get("status") == "ok"

    @pytest.mark.asyncio
    async def test_success_if_to_date_provided(
        self: Self, client: AsyncClient, session: AsyncSession
    ) -> None:
        # Arrange
        timestamp = 1545221231

        visit1 = Visit(
            link="https://link1.ru/",
            created_at=datetime.fromtimestamp(timestamp - 1000),
        )
        visit2 = Visit(
            link="https://link2.ru/",
            created_at=datetime.fromtimestamp(timestamp + 1000),
        )
        session.add_all([visit1, visit2])
        await session.flush()

        # Act
        with patch("app.visits.queries.session_manager.session") as patched:
            patched.return_value = session

            response = await client.get(f"/visited_links?to={timestamp}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("domains") == ["https://link1.ru/"]
        assert response.json().get("status") == "ok"
