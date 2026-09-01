import pytest
from click.testing import CliRunner
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models.base import Base


@pytest.fixture()
def cli_sessionmaker():
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


@pytest.fixture()
def cli_persist(cli_sessionmaker):
    def _persist(instance):
        session = cli_sessionmaker()
        session.add(instance)
        session.commit()
        session.refresh(instance)
        session.expunge(instance)
        session.close()
        return instance

    return _persist


@pytest.fixture()
def cli_runner(monkeypatch, cli_sessionmaker, tmp_path):
    monkeypatch.setattr("cli.context.SessionLocal", cli_sessionmaker)
    monkeypatch.setattr("cli.session.SESSION_FILE", tmp_path / "session.json")
    return CliRunner()
