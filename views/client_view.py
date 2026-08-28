from models.client import Client


class ClientView:

    def create_client(self):
        first_name = input("prenom: ")
        last_name = input("nom: ")
        email = input("email: ")
        phone = input("telephone: ")
        company = input("nom de l'entreprise: ")
        return first_name, last_name, email, phone, company

    def display_client(self, client: Client):
        print(
            f"{client.first_name} {client.last_name}\n"
            f"{client.email}\n"
            f"{client.phone}\n"
            f"{client.company}"
        )
