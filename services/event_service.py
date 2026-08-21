from models.event import Event
from repositories.event_repository import EventRepository
from repositories.user_repository import UserRepository


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
        support_email,
    ):

        support = UserRepository().get_by_email(support_email)

        event = Event(
            event_name=event_name,
            contract_id=contract_id,
            date_start=date_start,
            date_end=date_end,
            location=location,
            attendees=attendees,
            notes=notes,
            suuport_id=support.id,
        )
        return self.repository.create(event)
