from sqlalchemy import select
from uuid import UUID
from collections.abc import Sequence

from models.user import User


class UserRepository:

    def __init__(self, session):
        self.session = session

    # Création d'un user dans la base de données
    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    # Retourne un user de la base de données par uuid
    def get_by_id(self, user_id: str) -> User:
        user = self.session.get(User, UUID(user_id))
        return user

    # Retourne un user de la base de données par email
    def get_by_email(self, email: str) -> User:
        user = self.session.scalars(select(User).where(User.email == email)).first()
        return user

    # Retourne tous les users de la base de données
    def users_list(self) -> Sequence[User]:
        users = self.session.scalars(select(User)).all()
        return users

    # Modification des attributs d'un user dans la base de données
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

    # Suppression d'un user de la base de données
    def delete_user(self, user: User):
        self.session.delete(user)
        self.session.commit()
