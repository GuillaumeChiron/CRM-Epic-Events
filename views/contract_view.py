from decimal import Decimal, InvalidOperation

from models.contract import Contract


class ContractView:

    def _prompt_decimal(self, prompt):
        raw = input(prompt)
        while True:
            try:
                return Decimal(raw)
            except InvalidOperation:
                raw = input("Montant invalide, saisissez un nombre (ex: 1500.00): ")

    def _prompt_bool(self, prompt):
        raw = input(prompt).strip().lower()
        while raw not in ("o", "n"):
            raw = input("Réponse invalide, entrez 'o' ou 'n': ").strip().lower()
        return raw == "o"

    def create_contract(self):
        total_amount = self._prompt_decimal("montant total à payer: ")
        remaining_amount = self._prompt_decimal("montant restant à payer: ")
        client_email = input("email du client associé: ")
        return total_amount, remaining_amount, client_email

    def display_contract(self, contract: Contract):
        print(
            f"{contract.client.company}: {contract.client.first_name} {contract.client.last_name}\n"
            f"signature: {contract.signed}\n"
            f"Reste à payer: {contract.remaining_amount}/{contract.total_amount}"
        )

    def display_contracts_list(self, contracts):
        for contract in contracts:
            self.display_contract(contract)
            print("---")

    def update_total_amount(self):
        return self._prompt_decimal("nouveau montant total: ")

    def update_remaining_amount(self):
        return self._prompt_decimal("nouveau montant restant: ")

    def update_signed(self):
        return self._prompt_bool("contrat signé ? (o/n): ")
