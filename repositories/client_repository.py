from sqlalchemy import select
from uuid import UUID

from models.client import Client


class ClientRepository:

    def __init__(self, session):
        self.session = session

    def create(self, client: Client):
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)

    def get_by_id(self, client_id):
        client = self.session.get(Client, UUID(client_id))
        return client

    def get_by_last_name(self, last_name):
        client = self.session.scalars(
            select(Client).where(Client.last_name == last_name)
        ).first()
        return client

    def get_by_email(self, email):
        client = self.session.scalars(
            select(Client).where(Client.email == email)
        ).first()
        return client

    def client_list(self):
        clients = self.session.scalars(select(Client)).all()
        return clients

    def update_first_name(self, client, first_name):
        client.first_name = first_name
        self.session.commit()
        self.session.refresh(client)

    def update_last_name(self, client, last_name):
        client.last_name = last_name
        self.session.commit()
        self.session.refresh(client)

    def update_email(self, client, email):
        client.email = email
        self.session.commit()
        self.session.refresh(client)

    def update_phone(self, client, phone):
        client.phone = phone
        self.session.commit()
        self.session.refresh(client)

    def update_company(self, client, company):
        client.company = company
        self.session.commit()
        self.session.refresh(client)

    def update_last_contact_at(self, client, last_contact_at):
        client.last_contact_at = last_contact_at
        self.session.commit()
        self.session.refresh(client)

    def update_commercial_id(self, client, commercial_id):
        client.commercial_id = commercial_id
        self.session.commit()
        self.session.refresh(client)

    def delete(self, client):
        self.session.delete(client)
        self.session.commit()
