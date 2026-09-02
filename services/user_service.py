import sentry_sdk
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from models.user import User
from repositories.user_repository import UserRepository
from permissions.permission import gestion_required

from collections.abc import Sequence

ph = PasswordHasher()


def _log_user_event(action, user):
    sentry_sdk.capture_message(f"Collaborateur {action} : {user.email}", level="info")


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    # Créer et retourne une instance de User
    @gestion_required
    def create_user(
        self,
        current_user: User,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: str,
    ) -> User:
        password_hash = ph.hash(password)
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        self.repository.create(user)
        _log_user_event("cree", user)
        return user

    # Authentifie un User: compare password avec celui en base de données
    def authenticate(self, email: str, password: str) -> User:
        user = self.repository.get_by_email(email)

        if user is None:
            return None

        try:
            ph.verify(user.password_hash, password)
            return user
        except VerifyMismatchError:
            return None

    def list_users(self) -> Sequence[User]:
        return self.repository.users_list()

    # Retourne un User avec les modifications effectuées
    @gestion_required
    def update_email(self, current_user: User, user: User, email: str) -> User:
        self.repository.update_email(user, email)
        _log_user_event("modifie", user)
        return user

    @gestion_required
    def update_password(self, current_user: User, user: User, password: str) -> User:
        password_hash = ph.hash(password)
        self.repository.update_password(user, password_hash)
        _log_user_event("modifie", user)
        return user

    @gestion_required
    def update_first_name(
        self, current_user: User, user: User, first_name: str
    ) -> User:
        self.repository.update_first_name(user, first_name)
        _log_user_event("modifie", user)
        return user

    @gestion_required
    def update_last_name(self, current_user: User, user: User, last_name: str) -> User:
        self.repository.update_last_name(user, last_name)
        _log_user_event("modifie", user)
        return user

    @gestion_required
    def update_role(self, current_user: User, user: User, role: str) -> User:
        self.repository.update_role(user, role)
        _log_user_event("modifie", user)
        return user

    # Supprime un User
    @gestion_required
    def delete_user(self, current_user: User, user: User):
        self.repository.delete_user(user)
