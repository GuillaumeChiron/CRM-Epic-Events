from models.client import Client


class ClientView:

    def create_client(self):
        first_name = input()
        last_name = input()
        email = input()
        phone = input()
        company = input()
        return first_name, last_name, email, phone, company

    def display_client(self, client: Client):
        print(
            f"{client.first_name} {client.last_name}\n"
            f"{client.email}\n"
            f"{client.phone}\n"
            f"{client.company}"
        )
