from sqlalchemy import (
    String,
    DateTime,
    Enum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum as PyEnum

from models.base import Base


class UserRole(PyEnum):
    commercial = "commercial"
    gestion = "gestion"
    support = "support"


class User(Base):
    __tablename__ = "utilisateurs"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
