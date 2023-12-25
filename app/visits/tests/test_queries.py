from datetime import datetime, timedelta
from typing import Self
from unittest.mock import patch

import pytest
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app.visits.models import Visit
from app.visits.queries import create_visit, get_visited_domains_list
from app.visits.schema import VisitPayload


class TestCreateVisit:
    @pytest.mark.asyncio
    async def test_success(self: Self, session: AsyncSession) -> None:
        # Arrange
        visit_data = VisitPayload(
            links=[
                HttpUrl("https://sber.ru"),
                HttpUrl("https://ya.ru"),
                HttpUrl("https://habr.com"),
            ]
        )

        # Act
        with patch("app.visits.queries.session_manager.session") as patched:
            patched.return_value = session

            visits = await create_visit(visit_data)

        # Assert
        assert len(visits) == 3
        assert all(isinstance(visit, Visit) for visit in visits)


class TestGetVisitedDomainsList:
    @pytest.mark.asyncio
    async def test_success(self: Self, session: AsyncSession) -> None:
        with patch("app.visits.queries.session_manager.session") as patched:
            # Arrange
            patched.return_value = session

            await create_visit(
                VisitPayload(
                    links=[
                        HttpUrl("https://sber.ru/"),
                        HttpUrl("https://ya.ru/"),
                    ]
                )
            )

            # Act
            links = await get_visited_domains_list()

            # Assert
            assert sorted(links) == sorted(
                ["https://sber.ru/", "https://ya.ru/"]
            )

    @pytest.mark.asyncio
    async def test_success_with_from_date_filter(
        self: Self, session: AsyncSession
    ) -> None:
        with patch("app.visits.queries.session_manager.session") as patched:
            # Arrange
            patched.return_value = session

            now = datetime.now()

            visit1 = Visit(
                link="https://sber.ru/", created_at=now - timedelta(days=1)
            )
            visit2 = Visit(
                link="https://ya.ru/", created_at=now + timedelta(days=1)
            )
            session.add_all([visit1, visit2])
            await session.flush()

            # Act
            links = await get_visited_domains_list(from_date=now)

            # Assert
            assert links == ["https://ya.ru/"]

    @pytest.mark.asyncio
    async def test_success_with_to_date_filter(
        self: Self, session: AsyncSession
    ) -> None:
        with patch("app.visits.queries.session_manager.session") as patched:
            # Arrange
            patched.return_value = session

            now = datetime.now()

            visit1 = Visit(
                link="https://sber.ru/", created_at=now - timedelta(days=1)
            )
            visit2 = Visit(
                link="https://ya.ru/", created_at=now + timedelta(days=1)
            )
            session.add_all([visit1, visit2])
            await session.flush()

            # Act
            links = await get_visited_domains_list(to_date=now)

            # Assert
            assert links == ["https://sber.ru/"]

    @pytest.mark.asyncio
    async def test_success_with_unique_filter(
        self: Self, session: AsyncSession
    ) -> None:
        with patch("app.visits.queries.session_manager.session") as patched:
            # Arrange
            patched.return_value = session

            session.add_all([Visit(link="https://sber.ru/") for _ in range(90)])
            await session.flush()

            # Act
            links = await get_visited_domains_list(unique=True)

            # Assert
            assert links == ["https://sber.ru/"]
