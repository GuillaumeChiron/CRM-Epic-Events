from sqlalchemy import select
from uuid import UUID
from collections.abc import Sequence
from datetime import datetime

from models.client import Client


class ClientRepository:

    def __init__(self, session):
        self.session = session

    # Creation du client dans la base de données
    def create(self, client: Client):
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)

    # Retourne un client dans la base de données par son uuid
    def get_by_id(self, client_id: str) -> Client:
        client = self.session.get(Client, UUID(client_id))
        return client

    # Retourne un client dans la base de données par son Nom
    def get_by_last_name(self, last_name: str) -> Client:
        client = self.session.scalars(
            select(Client).where(Client.last_name == last_name)
        ).first()
        return client

    # Retourne un client dans la base de données par son email
    def get_by_email(self, email: str) -> Client:
        client = self.session.scalars(
            select(Client).where(Client.email == email)
        ).first()
        return client

    # Retourne la liste de tous les client de la base de données
    def client_list(self) -> Sequence[Client]:
        clients = self.session.scalars(select(Client)).all()
        return clients

    # Modification des attributs d'un client dans la base de données
    def update_first_name(self, client: Client, first_name: str):
        client.first_name = first_name
        self.session.commit()
        self.session.refresh(client)

    def update_last_name(self, client: Client, last_name: str):
        client.last_name = last_name
        self.session.commit()
        self.session.refresh(client)

    def update_email(self, client: Client, email: str):
        client.email = email
        self.session.commit()
        self.session.refresh(client)

    def update_phone(self, client: Client, phone: str):
        client.phone = phone
        self.session.commit()
        self.session.refresh(client)

    def update_company(self, client: Client, company: str):
        client.company = company
        self.session.commit()
        self.session.refresh(client)

    def update_last_contact_at(self, client: Client, last_contact_at: datetime):
        client.last_contact_at = last_contact_at
        self.session.commit()
        self.session.refresh(client)

    def update_commercial_id(self, client: Client, commercial_id: UUID):
        client.commercial_id = commercial_id
        self.session.commit()
        self.session.refresh(client)

    # Suppression d'un client de la base de données
    def delete(self, client: Client):
        self.session.delete(client)
        self.session.commit()
