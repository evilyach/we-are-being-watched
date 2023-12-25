import uuid
from datetime import datetime
from typing import Self

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.visits.models import Visit


class TestVisitModel:
    def test_create_instance(self: Self) -> None:
        visit = Visit()
        assert isinstance(visit, Visit)

    def test_repr(self: Self) -> None:
        visit = Visit(link="https://sber.ru")
        assert repr(visit) == "Visit to 'https://sber.ru'"

    @pytest.mark.asyncio
    async def test_fields(self: Self, session: AsyncSession) -> None:
        # Act
        visit = Visit(link="https://sber.ru")
        session.add(visit)
        await session.flush()

        # Assert
        assert isinstance(visit.id, uuid.UUID)
        assert isinstance(visit.link, str)
        assert isinstance(visit.created_at, datetime)
