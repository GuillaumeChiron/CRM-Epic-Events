import sentry_sdk
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from models.user import User
from repositories.user_repository import UserRepository
from permissions.permission import gestion_required

ph = PasswordHasher()


def _log_user_event(action, user):
    sentry_sdk.capture_message(f"Collaborateur {action} : {user.email}", level="info")


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    @gestion_required
    def create_user(self, current_user, email, password, first_name, last_name, role):
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

    def authenticate(self, email, password):
        user = self.repository.get_by_email(email)

        if user is None:
            return None

        try:
            ph.verify(user.password_hash, password)
            return user
        except VerifyMismatchError:
            return None

    def list_users(self):
        return self.repository.users_list()

    @gestion_required
    def update_email(self, current_user, user, email):
        self.repository.update_email(user, email)
        _log_user_event("modifie", user)
        return user

    @gestion_required
    def update_password(self, current_user, user, password):
        password_hash = ph.hash(password)
        self.repository.update_password(user, password_hash)
        _log_user_event("modifie", user)
        return user

    @gestion_required
    def update_first_name(self, current_user, user, first_name):
        self.repository.update_first_name(user, first_name)
        _log_user_event("modifie", user)
        return user

    @gestion_required
    def update_last_name(self, current_user, user, last_name):
        self.repository.update_last_name(user, last_name)
        _log_user_event("modifie", user)
        return user

    @gestion_required
    def update_role(self, current_user, user, role):
        self.repository.update_role(user, role)
        _log_user_event("modifie", user)
        return user

    @gestion_required
    def delete_user(self, current_user, user):
        self.repository.delete_user(user)
