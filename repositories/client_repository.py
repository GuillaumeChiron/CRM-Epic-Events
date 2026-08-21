from sqlalchemy import select
from uuid import UUID

from models.client import Client


class ClientRepository:

    def __init__(self, session):
        self.session = session

    def create(self, client):
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)

    def get_by_id(self, client_id):
        client = self.session.get(Client, UUID(client_id))
        return client

    def get_by_last_name(self, last_name):
        client = self.session.scalars(
            select(Client).where(Client.last_name == last_name).first()
        )
        return client

    def get_by_email(self, email):
        client = self.session.scarlars(
            select(Client).where(Client.email == email).first()
        )
        return client

    def client_list(self):
        clients = self.session.scalars(select(Client)).all()
        return clients

    def update(self, client, data):
        pass

    def delete(self, client):
        self.session.delete(client)
        self.session.commit()
