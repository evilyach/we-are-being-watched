import logging
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.visits.helpers import timestamp_to_datetime
from app.visits.models import Visit
from app.visits.queries import create_visit, get_visited_domains_list
from app.visits.schema import VisitGetAllResponse, VisitPayload, VisitSchema

logger = logging.getLogger()


visits_router = APIRouter(tags=["visits"])


@visits_router.post(
    "/visited_links",
    response_model=list[VisitSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_visit_entrypoint(payload: VisitPayload) -> list[Visit]:
    return await create_visit(payload)


@visits_router.get(
    "/visited_links",
    response_model=VisitGetAllResponse,
    status_code=status.HTTP_200_OK,
)
async def get_visits_entrypoint(
    from_date_timestamp: Annotated[
        int | None,
        Query(
            alias="from",
            title="From date param",
            description="Timestamp from which you want to search",
        ),
    ] = None,
    to_date_timestamp: Annotated[
        int | None,
        Query(
            alias="to",
            title="To date param",
            description="Timestamp until which you want to search",
        ),
    ] = None,
) -> VisitGetAllResponse:
    from_date: datetime | None = timestamp_to_datetime(from_date_timestamp)
    to_date: datetime | None = timestamp_to_datetime(to_date_timestamp)

    try:
        domains = await get_visited_domains_list(
            unique=True, from_date=from_date, to_date=to_date
        )
    except Exception as error:
        logger.error(error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error",
        )

    return VisitGetAllResponse(domains=domains, status="ok")
