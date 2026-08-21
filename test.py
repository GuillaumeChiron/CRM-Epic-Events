from database.database import SessionLocal

from views.user_view import UserView
from services.user_service import UserService
from repositories.user_repository import UserRepository

session = SessionLocal()
user_view = UserView()
user_repository = UserRepository(session)
user_service = UserService(user_repository)

email, password = user_view.login()
current_user = user_service.authenticate(email, password)

user_view.display_user(current_user)
