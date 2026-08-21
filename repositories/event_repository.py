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

    def event_list(self):
        events = self.session.scalars(select(Event)).all()
        return events

    def update(self):
        pass

    def delete(self, event):
        self.session.delete(event)
        self.session.commit()
