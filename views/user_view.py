from models.user import User


class UserView:

    def create_user(self):
        email = input("email: ")
        password = input("mot de passe: ")
        first_name = input("prenom: ")
        last_name = input("nom: ")
        role = input("role (gestion, commercial, support): ")
        return email, password, first_name, last_name, role

    def login(self):
        email = input("email: ")
        password = input("mot de passe: ")
        return email, password

    def display_user(self, user: User):
        print(f"{user.role.name}: {user.first_name} {user.last_name}\n" f"{user.email}")
