from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from models.client import Client
from collections.abc import Sequence


class ClientView:

    def __init__(self, console: Console | None = None):
        self.console = console or Console()

    # Demande une date au user
    def _prompt_date(self, prompt: str) -> datetime:
        raw = Prompt.ask(prompt)
        while True:
            try:
                return datetime.strptime(raw, "%d/%m/%Y")
            except ValueError:
                self.console.print(
                    "[red]Date invalide, format attendu JJ/MM/AAAA[/red]"
                )
                raw = Prompt.ask(prompt)

    # Demande les attributs du client au user
    def create_client(self) -> tuple[str, str, str, str, str]:
        first_name = Prompt.ask("prenom")
        last_name = Prompt.ask("nom")
        email = Prompt.ask("email")
        phone = Prompt.ask("telephone")
        company = Prompt.ask("nom de l'entreprise")
        return first_name, last_name, email, phone, company

    # Affiche un client
    def display_client(self, client: Client):
        body = (
            f"Email : {client.email}\n"
            f"Telephone : {client.phone}\n"
            f"Entreprise : {client.company}"
        )
        self.console.print(Panel(body, title=f"{client.first_name} {client.last_name}"))

    # Affiche dans un tableau tous les clients
    def display_clients_list(self, clients: Sequence[Client]):
        table = Table(title="Clients")
        table.add_column("Prenom")
        table.add_column("Nom")
        table.add_column("Email")
        table.add_column("Telephone")
        table.add_column("Entreprise")

        for client in clients:
            table.add_row(
                client.first_name,
                client.last_name,
                client.email,
                client.phone,
                client.company,
            )

        self.console.print(table)

    # Demande le nouvel attribut au user pour une modification client
    def update_first_name(self) -> str:
        return Prompt.ask("nouveau prenom")

    def update_last_name(self) -> str:
        return Prompt.ask("nouveau nom")

    def update_email(self) -> str:
        return Prompt.ask("nouvel email")

    def update_phone(self) -> str:
        return Prompt.ask("nouveau telephone")

    def update_company(self) -> str:
        return Prompt.ask("nouveau nom de l'entreprise")

    def update_last_contact_at(self) -> str:
        return self._prompt_date("date du dernier contact (JJ/MM/AAAA)")
