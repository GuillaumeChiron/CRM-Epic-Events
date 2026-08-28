from models.event import Event
from repositories.event_repository import EventRepository


class EventService:

    def __init__(self, repository: EventRepository):
        self.repository = repository

    def create_event(
        self,
        event_name,
        date_start,
        date_end,
        location,
        attendees,
        notes,
        contract_id,
    ):
        event = Event(
            event_name=event_name,
            contract_id=contract_id,
            date_start=date_start,
            date_end=date_end,
            location=location,
            attendees=attendees,
            notes=notes,
        )
        self.repository.create(event)
        return event

    def assign_support(self, event, support_id):
        self.repository.update_support_id(event, support_id)
