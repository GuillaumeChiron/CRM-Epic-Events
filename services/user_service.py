from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from models.user import User
from repositories.user_repository import UserRepository
from permissions.permission import gestion_required

ph = PasswordHasher()


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
        return user

    @gestion_required
    def update_password(self, current_user, user, password):
        password_hash = ph.hash(password)
        self.repository.update_password(user, password_hash)
        return user

    @gestion_required
    def update_first_name(self, current_user, user, first_name):
        self.repository.update_first_name(user, first_name)
        return user

    @gestion_required
    def update_last_name(self, current_user, user, last_name):
        self.repository.update_last_name(user, last_name)
        return user

    @gestion_required
    def update_role(self, current_user, user, role):
        self.repository.update_role(user, role)
        return user

    @gestion_required
    def delete_user(self, current_user, user):
        self.repository.delete_user(user)
