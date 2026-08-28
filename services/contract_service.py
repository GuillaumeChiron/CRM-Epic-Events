from models.contract import Contract
from repositories.contract_repository import ContractRepository
from repositories.client_repository import ClientRepository


class ContractService:

    def __init__(self, repository: ContractRepository, client_repository: ClientRepository):
        self.repository = repository
        self.client_repository = client_repository

    def create_contract(self, total_amount, remaining_amount, client_email):

        client = self.client_repository.get_by_email(client_email)

        contract = Contract(
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            client_id=client.id,
        )
        self.repository.create(contract)
        return contract
