from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from models.user import User
from collections.abc import Sequence


class UserView:

    VALID_ROLES = ("gestion", "commercial", "support")

    def __init__(self, console: Console | None = None):
        self.console = console or Console()

    # Demande un role au user
    def _prompt_role(self, prompt="role (gestion, commercial, support)") -> str:
        return Prompt.ask(prompt, choices=list(self.VALID_ROLES))

    # Demande les attributs d'un user au user
    def create_user(self) -> tuple[str, str, str, str, str]:
        email = Prompt.ask("email")
        password = Prompt.ask("mot de passe")
        first_name = Prompt.ask("prenom")
        last_name = Prompt.ask("nom")
        role = self._prompt_role()
        return email, password, first_name, last_name, role

    # Demande les logs d'un user (email, password)
    def login(self) -> tuple[str, str]:
        email = Prompt.ask("email")
        password = Prompt.ask("mot de passe")
        return email, password

    # Affiche un user
    def display_user(self, user: User):
        self.console.print(
            Panel(
                f"Email : {user.email}",
                title=f"{user.role.name}: {user.first_name} {user.last_name}",
            )
        )

    # Affiche sous forme d'un tableau tous les users
    def display_users_list(self, users: Sequence[User]):
        table = Table(title="Collaborateurs")
        table.add_column("Prenom")
        table.add_column("Nom")
        table.add_column("Email")
        table.add_column("Role")

        for user in users:
            table.add_row(user.first_name, user.last_name, user.email, user.role.name)

        self.console.print(table)

    # Demande le nouvel attribut au user pour une modification user
    def update_email(self) -> str:
        return Prompt.ask("nouvel email")

    def update_password(self) -> str:
        return Prompt.ask("nouveau mot de passe")

    def update_first_name(self) -> str:
        return Prompt.ask("nouveau prenom")

    def update_last_name(self) -> str:
        return Prompt.ask("nouveau nom")

    def update_role(self) -> str:
        return self._prompt_role("nouveau role (gestion, commercial, support)")
