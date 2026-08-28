from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from models.user import UserRole
from services.contract_service import ContractService
from tests.factories import build_client, build_contract, build_user


@pytest.fixture()
def repository():
    return MagicMock()


@pytest.fixture()
def client_repository():
    return MagicMock()


@pytest.fixture()
def service(repository, client_repository):
    return ContractService(repository, client_repository)


class TestCreateContract:
    def test_gestion_can_create_contract(self, service, repository, client_repository):
        current_user = build_user(role=UserRole.gestion)
        client = build_client()
        client_repository.get_by_email.return_value = client

        contract = service.create_contract(
            current_user, Decimal("1000.00"), Decimal("1000.00"), client.email
        )

        assert contract.client_id == client.id
        repository.create.assert_called_once_with(contract)

    @pytest.mark.parametrize("role", [UserRole.commercial, UserRole.support])
    def test_non_gestion_cannot_create_contract(
        self, service, repository, client_repository, role
    ):
        current_user = build_user(role=role)

        result = service.create_contract(
            current_user, Decimal("1000.00"), Decimal("1000.00"), "client@example.com"
        )

        assert result is False
        repository.create.assert_not_called()


def test_list_contracts_delegates(service, repository):
    repository.contract_list.return_value = ["c1"]
    assert service.list_contracts() == ["c1"]


def test_list_unsigned_contracts_delegates(service, repository):
    repository.unsigned.return_value = ["c1"]
    assert service.list_unsigned_contracts() == ["c1"]


def test_list_contracts_with_remaining_amount_delegates(service, repository):
    repository.remaining_amount.return_value = ["c1"]
    assert service.list_contracts_with_remaining_amount() == ["c1"]


@pytest.mark.parametrize(
    "method, args",
    [
        ("update_total_amount", (Decimal("2000.00"),)),
        ("update_remaining_amount", (Decimal("500.00"),)),
        ("update_signed", (True,)),
    ],
)
class TestOwnerOrGestionActions:
    def test_owner_can_update(self, service, repository, method, args):
        current_user = build_user(role=UserRole.commercial)
        owned_client = build_client(commercial_id=current_user.id)
        contract = build_contract(client=owned_client)

        getattr(service, method)(current_user, contract, *args)

        assert getattr(repository, method).call_count == 1

    def test_gestion_bypasses_ownership(self, service, repository, method, args):
        current_user = build_user(role=UserRole.gestion)
        other_client = build_client(commercial_id=uuid4())
        contract = build_contract(client=other_client)

        getattr(service, method)(current_user, contract, *args)

        assert getattr(repository, method).call_count == 1

    def test_non_owner_commercial_cannot_update(self, service, repository, method, args):
        current_user = build_user(role=UserRole.commercial)
        other_client = build_client(commercial_id=uuid4())
        contract = build_contract(client=other_client)

        result = getattr(service, method)(current_user, contract, *args)

        assert result is False
        getattr(repository, method).assert_not_called()
