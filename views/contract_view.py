from models.contract import Contract


class ContractView:

    def create_contract(self):

        total_amount = input("montant total à payer: ")
        remaining_amount = input("montant restant à payer: ")
        client_email = input("email du client associé: ")
        return total_amount, remaining_amount, client_email

    def display_contract(self, contract: Contract):
        print(
            f"{contract.client.company}: {contract.client.first_name} {contract.client.last_name}\n"
            f"siganture: {contract.signed}\n"
            f"Reste à payer: {contract.remaining_amount}/{contract.total_amount}"
        )
