from datetime import datetime

from sqlalchemy import select

from app.database.queries import add_all
from app.database.session import session_manager
from app.visits.models import Visit
from app.visits.schema import VisitPayload


async def create_visit(visit_data: VisitPayload) -> list[Visit]:
    visits = [Visit(link=str(link)) for link in visit_data.links]

    return await add_all(visits)


async def get_visited_domains_list(
    unique: bool = False,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
) -> list[str]:
    async with session_manager.session() as session:
        stmt = select(Visit.link)

        if from_date:
            stmt = stmt.filter(Visit.created_at > from_date)

        if to_date:
            stmt = stmt.filter(Visit.created_at < to_date)

        if unique:
            stmt = stmt.distinct()

        return list((await session.execute(stmt)).scalars().all())
