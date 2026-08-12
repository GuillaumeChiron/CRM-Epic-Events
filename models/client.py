from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from uuid import UUID, uuid4
from datetime import datetime, date

from models.base import Base
from models.user import User


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(100), nullable=False)
    company: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    last_contact_at: Mapped[datetime] = mapped_column(DateTime)
    commercial_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("utilisateurs.id"))

    commercial: Mapped["User"] = relationship("User")
