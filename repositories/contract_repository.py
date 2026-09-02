from sqlalchemy import select
from uuid import UUID
from collections.abc import Sequence
from decimal import Decimal

from models.contract import Contract


class ContractRepository:

    def __init__(self, session):
        self.session = session

    # Création d'un contrat dans la base de données
    def create(self, contract: Contract):
        self.session.add(contract)
        self.session.commit()
        self.session.refresh(contract)

    # Retourne un contrat de la base de données par uuid
    def get_by_id(self, contract_id: str) -> Contract:
        contract = self.session.get(Contract, UUID(contract_id))
        return contract

    # Retourne tous les contrats de la base de données
    def contract_list(self) -> Sequence[Contract]:
        contracts = self.session.scalars(select(Contract)).all()
        return contracts

    # Modification des attributs d'un contrat de la base de données
    def update_total_amount(self, contract: Contract, total_amount: Decimal):
        contract.total_amount = total_amount
        self.session.commit()
        self.session.refresh(contract)

    def update_remaining_amount(self, contract: Contract, remaining_amount: Decimal):
        contract.remaining_amount = remaining_amount
        self.session.commit()
        self.session.refresh(contract)

    def update_signed(self, contract: Contract, signed: bool):
        contract.signed = signed
        self.session.commit()
        self.session.refresh(contract)

    def update_client_id(self, contract: Contract, client_id: UUID):
        contract.client_id = client_id
        self.session.commit()
        self.session.refresh(contract)

    # Suppression d'un contrat de la base de données
    def delete(self, contract: Contract):
        self.session.delete(contract)
        self.session.commit()

    # Retourne tous les contrats non signés de la base de données
    def unsigned(self) -> Sequence[Contract]:
        contracts = self.session.scalars(
            select(Contract).where(Contract.signed.is_(False))
        ).all()
        return contracts

    # Retourne tous les contrats avec un reste à payer de la base de données
    def remaining_amount(self) -> Sequence[Contract]:
        contracts = self.session.scalars(
            select(Contract).where(Contract.remaining_amount > 0)
        ).all()
        return contracts
