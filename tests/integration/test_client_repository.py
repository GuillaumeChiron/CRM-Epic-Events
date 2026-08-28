import pytest
from sqlalchemy.exc import IntegrityError

from repositories.client_repository import ClientRepository
from tests.factories import build_client, build_user


@pytest.fixture()
def repository(db_session):
    return ClientRepository(db_session)


def test_create_persists_client(repository):
    client = build_client(email="marie@example.com")

    repository.create(client)

    assert repository.get_by_id(str(client.id)) is not None


def test_get_by_last_name_returns_matching_client(repository, persist):
    persist(build_client(last_name="Curie"))

    result = repository.get_by_last_name("Curie")

    assert result is not None
    assert result.last_name == "Curie"


def test_get_by_email_returns_none_when_not_found(repository):
    assert repository.get_by_email("missing@example.com") is None


def test_client_list_returns_all_clients(repository, persist):
    persist(build_client(email="c1@example.com"))
    persist(build_client(email="c2@example.com"))

    assert len(repository.client_list()) == 2


def test_update_commercial_id_persists_change(repository, persist):
    commercial = persist(build_user())
    client = persist(build_client())

    repository.update_commercial_id(client, commercial.id)

    assert repository.get_by_id(str(client.id)).commercial_id == commercial.id


def test_delete_client_removes_record(repository, persist):
    client = persist(build_client())

    repository.delete(client)

    assert repository.get_by_id(str(client.id)) is None


def test_create_duplicate_email_raises_integrity_error(repository, persist):
    persist(build_client(email="dup@example.com"))

    with pytest.raises(IntegrityError):
        repository.create(build_client(email="dup@example.com"))
