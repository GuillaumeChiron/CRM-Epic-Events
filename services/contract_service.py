from models.contract import Contract
from repositories.contract_repository import ContractRepository
from repositories.client_repository import ClientRepository


class ContractService:

    def __init__(self, repository: ContractRepository):
        self.repository = repository

    def create_contract(self, total_amount, remaining_amount, client_email):

        client = ClientRepository.get_by_email(client_email)

        contract = Contract(
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            client_id=client.id,
        )
        return self.repository.create(contract)
