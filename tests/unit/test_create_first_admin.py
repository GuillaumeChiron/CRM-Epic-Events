import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models.base import Base
from models.user import UserRole
from scripts.create_first_admin import create_first_admin
from tests.factories import build_user


@pytest.fixture()
def session_factory():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    test_session_local = sessionmaker(bind=engine)

    try:
        yield test_session_local
    finally:
        engine.dispose()


def test_creates_gestion_user_when_table_is_empty(session_factory):
    user = create_first_admin(
        "admin@example.com", "s3cret!", "Ada", "Lovelace", session_factory=session_factory
    )

    assert user is not None
    assert user.email == "admin@example.com"
    assert user.role == UserRole.gestion
    assert user.password_hash != "s3cret!"


def test_refuses_when_a_user_already_exists(session_factory):
    session = session_factory()
    session.add(build_user())
    session.commit()
    session.close()

    result = create_first_admin(
        "admin@example.com", "s3cret!", "Ada", "Lovelace", session_factory=session_factory
    )

    assert result is None
