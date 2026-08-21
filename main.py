from sqlalchemy import select
from uuid import UUID

from database.database import SessionLocal
from models.user import User
from repositories.user_repository import UserRepository

session = SessionLocal()

# user = User(
#     email="blabla@hotmail.fr",
#     password_hash="motdepasse",
#     first_name="marie",
#     last_name="broje",
#     role="support",
# )

# try:
#     UserRepository(session).create(user)
#     print("user créé")
# except:
#     print("erreur: user non créé")


# users = session.scalars(select(User))
# users = users.all()
# for user in users:
#     print(
#         f"{user.first_name} {user.last_name} "
#         f"{user.email} "
#         f"{user.password_hash} "
#         f"{user.role.name} "
#         f"{user.created_at} "
#     )
#     print("")

users = UserRepository(session).users_list()
for u in users:
    print(
        f"{u.id} "
        f"{u.first_name} {u.last_name} "
        f"{u.email} "
        f"{u.password_hash} "
        f"{u.role.name} "
        f"{u.created_at} "
    )
    print("")

user = UserRepository(session).get_by_id("c5c668fa-655b-4fc8-b6ae-911ad1b12fe5")
print(user.id)
print(user.email)
print(user.first_name)
