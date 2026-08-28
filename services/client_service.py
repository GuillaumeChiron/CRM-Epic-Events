from models.client import Client
from repositories.client_repository import ClientRepository
from permissions.permission import commercial_required, owner_required

get_client_owner_id = lambda client, *a, **kw: client.commercial_id


class ClientService:

    def __init__(self, repository: ClientRepository):
        self.repository = repository

    @commercial_required
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

    def list_clients(self):
        return self.repository.client_list()

    @owner_required(get_client_owner_id)
    def update_first_name(self, current_user, client, first_name):
        self.repository.update_first_name(client, first_name)
        return client

    @owner_required(get_client_owner_id)
    def update_last_name(self, current_user, client, last_name):
        self.repository.update_last_name(client, last_name)
        return client

    @owner_required(get_client_owner_id)
    def update_email(self, current_user, client, email):
        self.repository.update_email(client, email)
        return client

    @owner_required(get_client_owner_id)
    def update_phone(self, current_user, client, phone):
        self.repository.update_phone(client, phone)
        return client

    @owner_required(get_client_owner_id)
    def update_company(self, current_user, client, company):
        self.repository.update_company(client, company)
        return client

    @owner_required(get_client_owner_id)
    def update_last_contact_at(self, current_user, client, last_contact_at):
        self.repository.update_last_contact_at(client, last_contact_at)
        return client
