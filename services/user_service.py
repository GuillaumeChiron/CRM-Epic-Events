from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from models.user import User
from repositories.user_repository import UserRepository

ph = PasswordHasher()


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, email, password, first_name, last_name, role):

        password_hash = ph.hash(password)
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        return self.repository.create(user)

    def authenticate(self, email, password):
        user = self.repository.get_by_email(email)

        if user is None:
            return None

        try:
            ph.verify(user.password_hash, password)
            return user
        except VerifyMismatchError:
            return None
