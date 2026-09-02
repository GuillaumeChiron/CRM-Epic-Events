from models.event import Event
from models.user import User
from repositories.event_repository import EventRepository
from repositories.contract_repository import ContractRepository
from repositories.user_repository import UserRepository
from permissions.permission import commercial_required, gestion_required, owner_required

from collections.abc import Sequence
from datetime import datetime
from uuid import UUID


def get_event_owner_id(event, *a, **kw):
    return event.support_id


class EventService:

    def __init__(
        self,
        repository: EventRepository,
        contract_repository: ContractRepository,
        user_repository: UserRepository,
    ):
        self.repository = repository
        self.contract_repository = contract_repository
        self.user_repository = user_repository

    @commercial_required
    def create_event(
        self,
        current_user: User,
        event_name: str,
        date_start: datetime,
        date_end: datetime,
        location: str,
        attendees: int,
        notes: str,
        contract_id: UUID,
    ) -> Event:
        contract = self.contract_repository.get_by_id(contract_id)

        if not contract.signed or contract.client.commercial_id != current_user.id:
            return None

        event = Event(
            event_name=event_name,
            contract_id=contract.id,
            date_start=date_start,
            date_end=date_end,
            location=location,
            attendees=attendees,
            notes=notes,
        )
        self.repository.create(event)
        return event

    @gestion_required
    def assign_support(
        self, current_user: User, event: Event, support_email: str
    ) -> Event:
        support = self.user_repository.get_by_email(support_email)
        if support is None:
            return None
        self.repository.update_support_id(event, support.id)
        return event

    def list_events(self) -> Sequence[Event]:
        return self.repository.event_list()

    def list_events_without_support(self) -> Sequence[Event]:
        return self.repository.get_events_without_support()

    def list_my_events(self, current_user: User) -> Sequence[Event]:
        return self.repository.get_events_by_support_id(current_user.id)

    @owner_required(get_event_owner_id)
    def update_event_name(
        self, current_user: User, event: Event, event_name: str
    ) -> Event:
        self.repository.update_event_name(event, event_name)
        return event

    @owner_required(get_event_owner_id)
    def update_date_start(
        self, current_user: User, event: Event, date_start: datetime
    ) -> Event:
        self.repository.update_date_start(event, date_start)
        return event

    @owner_required(get_event_owner_id)
    def update_date_end(
        self, current_user: User, event: Event, date_end: datetime
    ) -> Event:
        self.repository.update_date_end(event, date_end)
        return event

    @owner_required(get_event_owner_id)
    def update_location(self, current_user: User, event: Event, location: str) -> Event:
        self.repository.update_location(event, location)
        return event

    @owner_required(get_event_owner_id)
    def update_attendees(
        self, current_user: User, event: Event, attendees: int
    ) -> Event:
        self.repository.update_attendees(event, attendees)
        return event

    @owner_required(get_event_owner_id)
    def update_notes(self, current_user: User, event: Event, notes: str) -> Event:
        self.repository.update_notes(event, notes)
        return event
