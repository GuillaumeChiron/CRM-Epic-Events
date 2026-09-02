from sqlalchemy import select
from uuid import UUID
from collections.abc import Sequence
from datetime import datetime

from models.event import Event


class EventRepository:

    def __init__(self, session):
        self.session = session

    def create(self, event: Event):
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)

    def get_by_id(self, event_id: str) -> Event:
        event = self.session.get(Event, UUID(event_id))
        return event

    def event_list(self) -> Sequence[Event]:
        events = self.session.scalars(select(Event)).all()
        return events

    def update_event_name(self, event: Event, event_name: str):
        event.event_name = event_name
        self.session.commit()
        self.session.refresh(event)

    def update_contract_id(self, event: Event, contract_id: UUID):
        event.contract_id = contract_id
        self.session.commit()
        self.session.refresh(event)

    def update_date_start(self, event: Event, date_start: datetime):
        event.date_start = date_start
        self.session.commit()
        self.session.refresh(event)

    def update_date_end(self, event: Event, date_end: datetime):
        event.date_end = date_end
        self.session.commit()
        self.session.refresh(event)

    def update_location(self, event: Event, location: str):
        event.location = location
        self.session.commit()
        self.session.refresh(event)

    def update_attendees(self, event: Event, attendees: int):
        event.attendees = attendees
        self.session.commit()
        self.session.refresh(event)

    def update_notes(self, event: Event, notes: str):
        event.notes = notes
        self.session.commit()
        self.session.refresh(event)

    def update_support_id(self, event: Event, support_id: UUID):
        event.support_id = support_id
        self.session.commit()
        self.session.refresh(event)

    def delete(self, event: Event):
        self.session.delete(event)
        self.session.commit()

    def get_events_without_support(self) -> Sequence[Event]:
        events = self.session.scalars(
            select(Event).where(Event.support_id.is_(None))
        ).all()
        return events

    def get_events_by_support_id(self, support_id) -> Sequence[Event]:
        events = self.session.scalars(
            select(Event).where(Event.support_id == support_id)
        ).all()
        return events
