from sqlalchemy import select
from uuid import UUID
from collections.abc import Sequence

from models.user import User


class UserRepository:

    def __init__(self, session):
        self.session = session

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    def get_by_id(self, user_id: str) -> User:
        user = self.session.get(User, UUID(user_id))
        return user

    def get_by_email(self, email: str) -> User:
        user = self.session.scalars(select(User).where(User.email == email)).first()
        return user

    def users_list(self) -> Sequence[User]:
        users = self.session.scalars(select(User)).all()
        return users

    def update_email(self, user: User, email: str):
        user.email = email
        self.session.commit()
        self.session.refresh(user)

    def update_password(self, user: User, password_hash: str):
        user.password_hash = password_hash
        self.session.commit()
        self.session.refresh(user)

    def update_first_name(self, user: User, first_name: str):
        user.first_name = first_name
        self.session.commit()
        self.session.refresh(user)

    def update_last_name(self, user: User, last_name: str):
        user.last_name = last_name
        self.session.commit()
        self.session.refresh(user)

    def update_role(self, user: User, role: str):
        user.role = role
        self.session.commit()
        self.session.refresh(user)

    def delete_user(self, user: User):
        self.session.delete(user)
        self.session.commit()
