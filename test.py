from database.database import SessionLocal

from services.user_service import UserService
from repositories.user_repository import UserRepository

session = SessionLocal()
repository = UserRepository(session)
service = UserService(repository)

email = input("email: ")
# password = input("mot de passe: ")
# first_name = input("prenom: ")
# last_name = input("nom: ")
# role = input("role (gestion, support, commercial): ")

# users = UserRepository(session).users_list()
# for u in users:
#     print(u.first_name)
#     print(u.email)
#     print("")

# try:
#     service.create_user(email, password, first_name, last_name, role)
#     print("user created")
# except Exception as error:
#     session.rollback()
#     print(f"Erreur : {error}")
# finally:
#     session.close()

# if service.authenticate(email, password) is not None:
#     current_user = service.authenticate(email, password)
#     print("Connecté")
# else:
#     print("Mot de passe incorrect")

# print(current_user.first_name)
