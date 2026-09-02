from decimal import Decimal, InvalidOperation

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from models.contract import Contract
from collections.abc import Sequence


class ContractView:

    def __init__(self, console: Console | None = None):
        self.console = console or Console()

    # Demande un montant au user
    def _prompt_decimal(self, prompt: Decimal) -> Decimal:
        raw = Prompt.ask(prompt)
        while True:
            try:
                return Decimal(raw)
            except InvalidOperation:
                self.console.print(
                    "[red]Montant invalide, saisissez un nombre (ex: 1500.00)[/red]"
                )
                raw = Prompt.ask(prompt)

    # Demande d'une validation au user
    def _prompt_bool(self, prompt: str):
        return Confirm.ask(prompt, choices=["o", "n"])

    # Demande les attributs du contrat au user
    def create_contract(self) -> tuple[Decimal, Decimal, str]:
        total_amount = self._prompt_decimal("montant total a payer")
        remaining_amount = self._prompt_decimal("montant restant a payer")
        client_email = Prompt.ask("email du client associe")
        return total_amount, remaining_amount, client_email

    # Affiche un contrat
    def display_contract(self, contract: Contract):
        body = (
            f"Client : {contract.client.first_name} {contract.client.last_name} "
            f"({contract.client.company})\n"
            f"Signe : {contract.signed}\n"
            f"Reste a payer : {contract.remaining_amount}/{contract.total_amount}"
        )
        self.console.print(Panel(body, title=f"Contrat {contract.id}"))

    # Affiche dans un tableau tous les contrats
    def display_contracts_list(self, contracts: Sequence[Contract]):
        table = Table(title="Contrats")
        table.add_column("#", no_wrap=True)
        table.add_column("Client", no_wrap=True)
        table.add_column("Entreprise")
        table.add_column("Signe")
        table.add_column("Reste a payer")
        table.add_column("Montant total")

        for index, contract in enumerate(contracts, start=1):
            table.add_row(
                str(index),
                f"{contract.client.first_name} {contract.client.last_name}",
                contract.client.company,
                "oui" if contract.signed else "non",
                str(contract.remaining_amount),
                str(contract.total_amount),
            )

        self.console.print(table)

    # Demande le nouvel attribut au user pour une modification contrat
    def update_total_amount(self) -> str:
        return self._prompt_decimal("nouveau montant total")

    def update_remaining_amount(self) -> str:
        return self._prompt_decimal("nouveau montant restant")

    def update_signed(self) -> str:
        return self._prompt_bool("contrat signe ?")
