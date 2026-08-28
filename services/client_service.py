from models.client import Client
from repositories.client_repository import ClientRepository


class ClientService:

    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def create_client(self, current_user, first_name, last_name, email, phone, company):
        client = Client(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            company=company,
            commercial_id=current_user.id,
        )
        self.repository.create(client)
        return client
