from datetime import datetime

from models.client import Client


class ClientView:

    def _prompt_date(self, prompt):
        raw = input(prompt)
        while True:
            try:
                return datetime.strptime(raw, "%d/%m/%Y")
            except ValueError:
                raw = input("Date invalide, format attendu JJ/MM/AAAA: ")

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

    def display_clients_list(self, clients):
        for client in clients:
            self.display_client(client)
            print("---")

    def update_first_name(self):
        return input("nouveau prenom: ")

    def update_last_name(self):
        return input("nouveau nom: ")

    def update_email(self):
        return input("nouvel email: ")

    def update_phone(self):
        return input("nouveau telephone: ")

    def update_company(self):
        return input("nouveau nom de l'entreprise: ")

    def update_last_contact_at(self):
        return self._prompt_date("date du dernier contact (JJ/MM/AAAA): ")
