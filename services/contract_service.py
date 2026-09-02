import sentry_sdk

from models.contract import Contract
from models.user import User
from repositories.contract_repository import ContractRepository
from repositories.client_repository import ClientRepository
from permissions.permission import gestion_required, owner_required

from decimal import Decimal
from collections.abc import Sequence


def get_contract_owner_id(contract, *a, **kw):
    return contract.client.commercial_id


class ContractService:

    def __init__(
        self, repository: ContractRepository, client_repository: ClientRepository
    ):
        self.repository = repository
        self.client_repository = client_repository

    # Créer et retourne une instance de Contract
    @gestion_required
    def create_contract(
        self,
        current_user: User,
        total_amount: Decimal,
        remaining_amount: Decimal,
        client_email: str,
    ) -> Contract:
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

    # Rtourne tous les contrats
    def list_contracts(self) -> Sequence[Contract]:
        return self.repository.contract_list()

    # Retourne tous les contrats non signés
    def list_unsigned_contracts(self) -> Sequence[Contract]:
        return self.repository.unsigned()

    # Retourne tous les contrats avec un reste à payer
    def list_contracts_with_remaining_amount(self) -> Sequence[Contract]:
        return self.repository.remaining_amount()

    # Retourne un Contract avec les modifications effectuées
    @owner_required(get_contract_owner_id, "gestion")
    def update_total_amount(
        self, current_user: User, contract: Contract, total_amount: Decimal
    ) -> Contract:
        self.repository.update_total_amount(contract, total_amount)
        return contract

    @owner_required(get_contract_owner_id, "gestion")
    def update_remaining_amount(
        self, current_user: User, contract: Contract, remaining_amount: Decimal
    ) -> Contract:
        self.repository.update_remaining_amount(contract, remaining_amount)
        return contract

    @owner_required(get_contract_owner_id, "gestion")
    def update_signed(
        self, current_user: User, contract: Contract, signed: bool
    ) -> Contract:
        self.repository.update_signed(contract, signed)
        if signed:
            sentry_sdk.capture_message(f"Contrat signe : {contract.id}", level="info")
        return contract
