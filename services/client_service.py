from models.client import Client
from repositories.client_repository import ClientRepository
from repositories.user_repository import UserRepository


class ClientService:

    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def create_client(
        self, first_name, last_name, email, phone, company, commercial_email
    ):
        commercial = UserRepository.get_by_email(commercial_email)

        client = Client(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            company=company,
            commercial_id=commercial.id,
        )
        return self.repository.create(client)
