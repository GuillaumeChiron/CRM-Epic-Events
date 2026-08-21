from sqlalchemy import (
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    Uuid,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal

from models.base import Base
from models.client import Client


class Contract(Base):
    __tablename__ = "contrats"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    remaining_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        CheckConstraint("remaing_amount >= 0 AND remaining_amount <= total_amount"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    signed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    client_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("clients.id", ondelete="RESTRICT"),
        nullable=False,
    )

    client: Mapped["Client"] = relationship("Client")
