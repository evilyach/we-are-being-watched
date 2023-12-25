from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class VisitSchema(BaseModel):
    link: HttpUrl
    created_at: datetime


class VisitPayload(BaseModel):
    links: list[HttpUrl] = Field(min_length=1)


class VisitGetAllResponse(BaseModel):
    domains: list[str]
    status: str
