import pytest

from repositories.event_repository import EventRepository
from tests.factories import build_client, build_contract, build_event, build_user


@pytest.fixture()
def repository(db_session):
    return EventRepository(db_session)


def _persisted_contract(persist):
    client = persist(build_client())
    return persist(build_contract(client_id=client.id))


def test_create_persists_event(repository, persist):
    contract = _persisted_contract(persist)
    event = build_event(contract_id=contract.id)

    repository.create(event)

    assert repository.get_by_id(str(event.id)) is not None


def test_get_events_without_support_excludes_assigned_events(repository, persist):
    contract = _persisted_contract(persist)
    support = persist(build_user())
    unassigned = persist(build_event(contract_id=contract.id, support_id=None))
    persist(build_event(contract_id=contract.id, support_id=support.id))

    result = repository.get_events_without_support()

    assert [e.id for e in result] == [unassigned.id]


def test_get_events_by_support_id_filters_correctly(repository, persist):
    contract = _persisted_contract(persist)
    support = persist(build_user())
    mine = persist(build_event(contract_id=contract.id, support_id=support.id))
    persist(build_event(contract_id=contract.id, support_id=None))

    result = repository.get_events_by_support_id(support.id)

    assert [e.id for e in result] == [mine.id]


def test_update_support_id_persists_change(repository, persist):
    contract = _persisted_contract(persist)
    support = persist(build_user())
    event = persist(build_event(contract_id=contract.id))

    repository.update_support_id(event, support.id)

    assert repository.get_by_id(str(event.id)).support_id == support.id


def test_delete_event_removes_record(repository, persist):
    contract = _persisted_contract(persist)
    event = persist(build_event(contract_id=contract.id))

    repository.delete(event)

    assert repository.get_by_id(str(event.id)) is None
