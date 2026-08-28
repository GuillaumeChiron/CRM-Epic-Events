from models.event import Event
from repositories.event_repository import EventRepository
from repositories.contract_repository import ContractRepository
from repositories.user_repository import UserRepository
from permissions.permission import commercial_required, gestion_required, owner_required

get_event_owner_id = lambda event, *a, **kw: event.support_id


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
        current_user,
        event_name,
        date_start,
        date_end,
        location,
        attendees,
        notes,
        contract_id,
    ):
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
    def assign_support(self, current_user, event, support_email):
        support = self.user_repository.get_by_email(support_email)
        self.repository.update_support_id(event, support.id)
        return event

    def list_events(self):
        return self.repository.event_list()

    def list_events_without_support(self):
        return self.repository.get_events_without_support()

    def list_my_events(self, current_user):
        return self.repository.get_events_by_support_id(current_user.id)

    @owner_required(get_event_owner_id)
    def update_event_name(self, current_user, event, event_name):
        self.repository.update_event_name(event, event_name)
        return event

    @owner_required(get_event_owner_id)
    def update_date_start(self, current_user, event, date_start):
        self.repository.update_date_start(event, date_start)
        return event

    @owner_required(get_event_owner_id)
    def update_date_end(self, current_user, event, date_end):
        self.repository.update_date_end(event, date_end)
        return event

    @owner_required(get_event_owner_id)
    def update_location(self, current_user, event, location):
        self.repository.update_location(event, location)
        return event

    @owner_required(get_event_owner_id)
    def update_attendees(self, current_user, event, attendees):
        self.repository.update_attendees(event, attendees)
        return event

    @owner_required(get_event_owner_id)
    def update_notes(self, current_user, event, notes):
        self.repository.update_notes(event, notes)
        return event
