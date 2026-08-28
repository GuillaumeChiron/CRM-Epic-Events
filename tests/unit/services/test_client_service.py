from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from models.user import UserRole
from services.client_service import ClientService
from tests.factories import build_client, build_user


@pytest.fixture()
def repository():
    return MagicMock()


@pytest.fixture()
def service(repository):
    return ClientService(repository)


class TestCreateClient:
    def test_commercial_can_create_client(self, service, repository):
        current_user = build_user(role=UserRole.commercial)

        client = service.create_client(
            current_user, "Marie", "Curie", "marie@example.com", "0600000000", "ACME"
        )

        assert client.commercial_id == current_user.id
        repository.create.assert_called_once_with(client)

    @pytest.mark.parametrize("role", [UserRole.gestion, UserRole.support])
    def test_non_commercial_cannot_create_client(self, service, repository, role):
        current_user = build_user(role=role)

        result = service.create_client(
            current_user, "Marie", "Curie", "marie@example.com", "0600000000", "ACME"
        )

        assert result is False
        repository.create.assert_not_called()


def test_list_clients_delegates_to_repository(service, repository):
    repository.client_list.return_value = ["c1"]

    assert service.list_clients() == ["c1"]


@pytest.mark.parametrize(
    "method, args",
    [
        ("update_first_name", ("Paul",)),
        ("update_last_name", ("Martin",)),
        ("update_email", ("paul@example.com",)),
        ("update_phone", ("0700000000",)),
        ("update_company", ("NewCo",)),
        ("update_last_contact_at", (None,)),
    ],
)
class TestOwnerOnlyActions:
    def test_owner_can_update(self, service, repository, method, args):
        current_user = build_user(role=UserRole.commercial)
        client = build_client(commercial_id=current_user.id)

        getattr(service, method)(current_user, client, *args)

        assert getattr(repository, method).call_count == 1

    def test_non_owner_cannot_update(self, service, repository, method, args):
        current_user = build_user(role=UserRole.commercial)
        client = build_client(commercial_id=uuid4())

        result = getattr(service, method)(current_user, client, *args)

        assert result is False
        getattr(repository, method).assert_not_called()

    def test_gestion_cannot_bypass_ownership(self, service, repository, method, args):
        current_user = build_user(role=UserRole.gestion)
        client = build_client(commercial_id=uuid4())

        result = getattr(service, method)(current_user, client, *args)

        assert result is False
        getattr(repository, method).assert_not_called()
