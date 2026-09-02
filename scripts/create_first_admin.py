import sys

from argon2 import PasswordHasher

from database.database import SessionLocal
from models.user import User, UserRole

ph = PasswordHasher()


# Créer le premier utilisateur avec le role gestion
# Ne s'execute pas si des users existent deja en base de données
def create_first_admin(
    email, password, first_name, last_name, session_factory=SessionLocal
):
    session = session_factory()
    try:
        if session.query(User).count() > 0:
            return None

        user = User(
            email=email,
            password_hash=ph.hash(password),
            first_name=first_name,
            last_name=last_name,
            role=UserRole.gestion,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    finally:
        session.close()


def main():
    email = input("email: ")
    password = input("mot de passe: ")
    first_name = input("prenom: ")
    last_name = input("nom: ")

    user = create_first_admin(email, password, first_name, last_name)

    if user is None:
        print(
            "Des collaborateurs existent deja. "
            "Utilisez `python main.py user create` une fois connecte."
        )
        sys.exit(1)

    print(f"Premier administrateur cree : {user.email}")


if __name__ == "__main__":
    main()
