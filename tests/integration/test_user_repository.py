import pytest
from sqlalchemy.exc import IntegrityError

from repositories.user_repository import UserRepository
from tests.factories import build_user


@pytest.fixture()
def repository(db_session):
    return UserRepository(db_session)


def test_create_persists_user(repository):
    user = build_user(email="new@example.com")

    repository.create(user)

    assert repository.get_by_id(str(user.id)) is not None


def test_get_by_email_returns_matching_user(repository, persist):
    user = persist(build_user(email="find-me@example.com"))

    result = repository.get_by_email("find-me@example.com")

    assert result.id == user.id


def test_get_by_email_returns_none_when_not_found(repository):
    assert repository.get_by_email("missing@example.com") is None


def test_users_list_returns_all_users(repository, persist):
    persist(build_user(email="a@example.com"))
    persist(build_user(email="b@example.com"))

    result = repository.users_list()

    assert len(result) == 2


def test_update_email_persists_change(repository, persist):
    user = persist(build_user(email="old@example.com"))

    repository.update_email(user, "updated@example.com")

    assert repository.get_by_email("updated@example.com") is not None
    assert repository.get_by_email("old@example.com") is None


def test_create_duplicate_email_raises_integrity_error(repository, persist):
    persist(build_user(email="dup@example.com"))

    with pytest.raises(IntegrityError):
        repository.create(build_user(email="dup@example.com"))


def test_delete_user_removes_record(repository, persist):
    user = persist(build_user(email="todelete@example.com"))

    repository.delete_user(user)

    assert repository.get_by_id(str(user.id)) is None
