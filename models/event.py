from sqlalchemy import (
    String,
    Integer,
    Float,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Enum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from uuid import UUID, uuid4

from models.base import Base


class Event(Base):
    __tablename__ = "evenements"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
