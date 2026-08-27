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

    def get_by_email(self, email) -> User:
        user = self.session.scalars(select(User).where(User.email == email)).first()
        return user

    def users_list(self):
        users = self.session.scalars(select(User)).all()
        return users

    def update_email(self, user, email):
        user.email = email
        self.session.commit()
        self.session.refresh(user)

    def update_password(self, user, password_hash):
        user.password_hash = password_hash
        self.session.commit()
        self.session.refresh(user)

    def update_first_name(self, user, first_name):
        user.first_name = first_name
        self.session.commit()
        self.session.refresh(user)

    def update_last_name(self, user, last_name):
        user.last_name = last_name
        self.session.commit()
        self.session.refresh(user)

    def update_role(self, user, role):
        user.role = role
        self.session.commit()
        self.session.refresh(user)

    def delete_user(self, user):
        self.session.delete(user)
        self.session.commit()
