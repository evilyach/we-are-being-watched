import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.database.models import Base


class Visit(Base):
    __tablename__ = "visit"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    link: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )

    def __repr__(self) -> str:
        return f"Visit to '{self.link}'"
