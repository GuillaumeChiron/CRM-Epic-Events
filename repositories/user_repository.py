from sqlalchemy import select
from uuid import UUID

from models.user import User


class UserRepository:

    def __init__(self, session):
        self.session = session

    def add(self, client):
        self.session.add(client)
        self.session.commit()

    def get_by_id(self, user_id):
        user = self.session.get(User, UUID(user_id))
        return user

    def get_by_email(self, email):
        user = self.session.scalars(select(User).where(User.email == email)).first()
        return user

    def users_list(self):
        users = self.session.scalars(select(User)).all()
        return users
