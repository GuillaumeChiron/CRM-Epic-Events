from sqlalchemy import select
from uuid import UUID

from models.event import Event


class EventRepository:

    def __init__(self, session):
        self.session = session

    def create(self, event):
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)

    def get_by_id(self, event_id):
        event = self.session.get(Event, UUID(event_id))
        return event

    def event_list(self):
        events = self.session.scalars(select(Event)).all()
        return events

    def update_event_name(self, event, event_name):
        event.event_name = event_name
        self.session.commit()
        self.session.refresh(event)

    def update_contract_id(self, event, contract_id):
        event.contract_id = contract_id
        self.session.commit()
        self.session.refresh(event)

    def update_date_start(self, event, date_start):
        event.date_start = date_start
        self.session.commit()
        self.session.refresh(event)

    def update_date_end(self, event, date_end):
        event.date_end = date_end
        self.session.commit()
        self.session.refresh(event)

    def update_location(self, event, location):
        event.location = location
        self.session.commit()
        self.session.refresh(event)

    def update_attendees(self, event, attendees):
        event.attendees = attendees
        self.session.commit()
        self.session.refresh(event)

    def update_notes(self, event, notes):
        event.notes = notes
        self.session.commit()
        self.session.refresh(event)

    def update_support_id(self, event, support_id):
        event.support_id = support_id
        self.session.commit()
        self.session.refresh(event)

    def delete(self, event):
        self.session.delete(event)
        self.session.commit()

    def get_events_without_support(self):
        pass

    def get_events_by_support_id(self):
        pass

    def get_upcoming_events(self):
        pass

    def search_events_by_client_or_contract(self):
        pass
