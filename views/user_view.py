from models.user import User


class UserView:

    VALID_ROLES = ("gestion", "commercial", "support")

    def _prompt_role(self, prompt="role (gestion, commercial, support): "):
        role = input(prompt)
        while role not in self.VALID_ROLES:
            print("Rôle invalide, choix possibles : gestion, commercial, support.")
            role = input(prompt)
        return role

    def create_user(self):
        email = input("email: ")
        password = input("mot de passe: ")
        first_name = input("prenom: ")
        last_name = input("nom: ")
        role = self._prompt_role()
        return email, password, first_name, last_name, role

    def login(self):
        email = input("email: ")
        password = input("mot de passe: ")
        return email, password

    def display_user(self, user: User):
        print(f"{user.role.name}: {user.first_name} {user.last_name}\n" f"{user.email}")

    def display_users_list(self, users):
        for user in users:
            self.display_user(user)
            print("---")

    def update_email(self):
        return input("nouvel email: ")

    def update_password(self):
        return input("nouveau mot de passe: ")

    def update_first_name(self):
        return input("nouveau prenom: ")

    def update_last_name(self):
        return input("nouveau nom: ")

    def update_role(self):
        return self._prompt_role("nouveau role (gestion, commercial, support): ")
