from datetime import datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from models.user import UserRole
from services.event_service import EventService
from tests.factories import build_client, build_contract, build_event, build_user


@pytest.fixture()
def repository():
    return MagicMock()


@pytest.fixture()
def contract_repository():
    return MagicMock()


@pytest.fixture()
def user_repository():
    return MagicMock()


@pytest.fixture()
def service(repository, contract_repository, user_repository):
    return EventService(repository, contract_repository, user_repository)


def _payload():
    now = datetime(2026, 1, 1, 20, 0)
    return dict(
        event_name="Soiree",
        date_start=now,
        date_end=now + timedelta(hours=2),
        location="Paris",
        attendees=50,
        notes=None,
        contract_id=str(uuid4()),
    )


class TestCreateEvent:
    def test_commercial_owner_with_signed_contract_can_create_event(
        self, service, repository, contract_repository
    ):
        current_user = build_user(role=UserRole.commercial)
        client = build_client(commercial_id=current_user.id)
        contract = build_contract(client=client, signed=True)
        contract_repository.get_by_id.return_value = contract

        event = service.create_event(current_user, **_payload())

        assert event is not None
        repository.create.assert_called_once_with(event)

    def test_non_commercial_cannot_create_event(self, service, repository, contract_repository):
        current_user = build_user(role=UserRole.support)

        result = service.create_event(current_user, **_payload())

        assert result is False
        repository.create.assert_not_called()

    def test_unsigned_contract_blocks_creation(self, service, repository, contract_repository):
        current_user = build_user(role=UserRole.commercial)
        client = build_client(commercial_id=current_user.id)
        contract = build_contract(client=client, signed=False)
        contract_repository.get_by_id.return_value = contract

        result = service.create_event(current_user, **_payload())

        assert result is None
        repository.create.assert_not_called()

    def test_commercial_not_owning_client_cannot_create_event(
        self, service, repository, contract_repository
    ):
        current_user = build_user(role=UserRole.commercial)
        client = build_client(commercial_id=uuid4())
        contract = build_contract(client=client, signed=True)
        contract_repository.get_by_id.return_value = contract

        result = service.create_event(current_user, **_payload())

        assert result is None
        repository.create.assert_not_called()


def test_assign_support_by_gestion(service, repository, user_repository):
    current_user = build_user(role=UserRole.gestion)
    support = build_user(role=UserRole.support, email="support@example.com")
    event = build_event()
    user_repository.get_by_email.return_value = support

    result = service.assign_support(current_user, event, support.email)

    assert result is event
    repository.update_support_id.assert_called_once_with(event, support.id)


def test_assign_support_blocked_for_non_gestion(service, repository, user_repository):
    current_user = build_user(role=UserRole.commercial)
    event = build_event()

    result = service.assign_support(current_user, event, "support@example.com")

    assert result is False
    repository.update_support_id.assert_not_called()


def test_list_events_delegates(service, repository):
    repository.event_list.return_value = ["e1"]
    assert service.list_events() == ["e1"]


def test_list_events_without_support_delegates(service, repository):
    repository.get_events_without_support.return_value = ["e1"]
    assert service.list_events_without_support() == ["e1"]


def test_list_my_events_delegates(service, repository):
    current_user = build_user(role=UserRole.support)
    repository.get_events_by_support_id.return_value = ["e1"]

    result = service.list_my_events(current_user)

    assert result == ["e1"]
    repository.get_events_by_support_id.assert_called_once_with(current_user.id)


@pytest.mark.parametrize(
    "method, args",
    [
        ("update_event_name", ("Nouveau nom",)),
        ("update_date_start", (datetime(2026, 1, 1, 20, 0),)),
        ("update_date_end", (datetime(2026, 1, 1, 23, 0),)),
        ("update_location", ("Lyon",)),
        ("update_attendees", (100,)),
        ("update_notes", ("note",)),
    ],
)
class TestSupportOwnerActions:
    def test_owner_support_can_update(self, service, repository, method, args):
        support = build_user(role=UserRole.support)
        event = build_event(support_id=support.id)

        getattr(service, method)(support, event, *args)

        assert getattr(repository, method).call_count == 1

    def test_non_owner_support_cannot_update(self, service, repository, method, args):
        support = build_user(role=UserRole.support)
        event = build_event(support_id=uuid4())

        result = getattr(service, method)(support, event, *args)

        assert result is False
        getattr(repository, method).assert_not_called()
