from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from repositories.contract_repository import ContractRepository
from tests.factories import build_client, build_contract


@pytest.fixture()
def repository(db_session):
    return ContractRepository(db_session)


def test_create_persists_contract(repository, persist):
    client = persist(build_client())
    contract = build_contract(client_id=client.id)

    repository.create(contract)

    assert repository.get_by_id(str(contract.id)) is not None


def test_remaining_amount_exceeding_total_violates_check_constraint(repository, persist):
    client = persist(build_client())
    contract = build_contract(
        client_id=client.id, total_amount=Decimal("100.00"), remaining_amount=Decimal("200.00")
    )

    with pytest.raises(IntegrityError):
        repository.create(contract)


def test_unsigned_returns_only_unsigned_contracts(repository, persist):
    client = persist(build_client())
    persist(build_contract(client_id=client.id, signed=True))
    unsigned = persist(build_contract(client_id=client.id, signed=False))

    result = repository.unsigned()

    assert [c.id for c in result] == [unsigned.id]


def test_remaining_amount_returns_contracts_with_balance_due(repository, persist):
    client = persist(build_client())
    persist(
        build_contract(
            client_id=client.id,
            remaining_amount=Decimal("0.00"),
            total_amount=Decimal("100.00"),
        )
    )
    due = persist(
        build_contract(
            client_id=client.id,
            remaining_amount=Decimal("50.00"),
            total_amount=Decimal("100.00"),
        )
    )

    result = repository.remaining_amount()

    assert [c.id for c in result] == [due.id]


def test_update_signed_persists_change(repository, persist):
    client = persist(build_client())
    contract = persist(build_contract(client_id=client.id, signed=False))

    repository.update_signed(contract, True)

    assert repository.get_by_id(str(contract.id)).signed is True
