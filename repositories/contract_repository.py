from sqlalchemy import select
from uuid import UUID

from models.contract import Contract


class ContractRepository:

    def __init__(self, session):
        self.session = session

    def create(self, contract):
        self.session.add(contract)
        self.session.commit()
        self.session.refresh(contract)

    def get_by_id(self, contract_id):
        contract = self.session.get(Contract, UUID(contract_id))
        return contract

    def contract_list(self):
        contracts = self.session.scalars(select(Contract)).all()
        return contracts

    def update(self, contract):
        pass

    def delete(self, contract):
        self.session.delete(contract)
        self.session.commit()

    def unsigned(self):
        contracts = self.session.scalars(
            select(Contract).where(Contract.signed == False)
        ).all()
        return contracts

    def remaining_amount(self):
        contracts = self.session.scalars(
            select(Contract).where(Contract.remaining_amount > 0)
        ).all()
        return contracts

    def get_contracts_for_commercial_clients(self):
        pass
