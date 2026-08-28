import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models.base import Base
from models.user import UserRole
from tests.factories import build_user


@pytest.fixture()
def db_session():
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
    session = sessionmaker(bind=engine)()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture()
def persist(db_session):
    def _persist(instance):
        db_session.add(instance)
        db_session.commit()
        db_session.refresh(instance)
        return instance

    return _persist


@pytest.fixture()
def gestion_user(persist):
    return persist(build_user(role=UserRole.gestion, email="gestion@example.com"))


@pytest.fixture()
def commercial_user(persist):
    return persist(build_user(role=UserRole.commercial, email="commercial@example.com"))


@pytest.fixture()
def support_user(persist):
    return persist(build_user(role=UserRole.support, email="support@example.com"))
