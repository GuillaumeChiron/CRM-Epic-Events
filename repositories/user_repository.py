from sqlalchemy import select
from uuid import UUID

from models.user import User


class UserRepository:

    def __init__(self, session):
        self.session = session

    def create(self, user):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    def get_by_id(self, user_id):
        user = self.session.get(User, UUID(user_id))
        return user

    def get_by_email(self, email):
        user = self.session.scalars(select(User).where(User.email == email)).first()
        return user

    def users_list(self):
        users = self.session.scalars(select(User)).all()
        return users

    def update(self, user, data):
        pass

    def delete_user(self, user):
        self.session.delete(user)
        self.session.commit()

    def get_events_without_support(self):
        pass

    def get_events_by_support_id(self):
        pass

    def get_upcoming_events(self):
        pass

    def search_events_by_client_or_contract(self):
        pass
