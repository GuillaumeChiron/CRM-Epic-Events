from sqlalchemy import (
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from uuid import UUID, uuid4
from datetime import datetime

from models.base import Base
from models.user import User
from models.contract import Contract


class Event(Base):
    __tablename__ = "evenements"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    event_name: Mapped[str] = mapped_column(String(255), nullable=False)
    contract_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("contrats.id", ondelete="RESTRICT"),
        nullable=False,
    )
    date_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    attendees: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    support_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("utilisateurs.id", ondelete="SET NULL"),
        nullable=True,
    )

    contract: Mapped["Contract"] = relationship("Contract")
    support: Mapped["User | None"] = relationship("User")
