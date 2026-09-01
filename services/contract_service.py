from models.contract import Contract
from repositories.contract_repository import ContractRepository
from repositories.client_repository import ClientRepository
from permissions.permission import gestion_required, owner_required

get_contract_owner_id = lambda contract, *a, **kw: contract.client.commercial_id


class ContractService:

    def __init__(self, repository: ContractRepository, client_repository: ClientRepository):
        self.repository = repository
        self.client_repository = client_repository

    @gestion_required
    def create_contract(self, current_user, total_amount, remaining_amount, client_email):
        client = self.client_repository.get_by_email(client_email)
        if client is None:
            return None

        contract = Contract(
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            client_id=client.id,
        )
        self.repository.create(contract)
        return contract

    def list_contracts(self):
        return self.repository.contract_list()

    def list_unsigned_contracts(self):
        return self.repository.unsigned()

    def list_contracts_with_remaining_amount(self):
        return self.repository.remaining_amount()

    @owner_required(get_contract_owner_id, "gestion")
    def update_total_amount(self, current_user, contract, total_amount):
        self.repository.update_total_amount(contract, total_amount)
        return contract

    @owner_required(get_contract_owner_id, "gestion")
    def update_remaining_amount(self, current_user, contract, remaining_amount):
        self.repository.update_remaining_amount(contract, remaining_amount)
        return contract

    @owner_required(get_contract_owner_id, "gestion")
    def update_signed(self, current_user, contract, signed):
        self.repository.update_signed(contract, signed)
        return contract
