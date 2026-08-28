from datetime import datetime

from models.event import Event


class EventView:

    def _prompt_datetime(self, prompt):
        raw = input(prompt)
        while True:
            try:
                return datetime.strptime(raw, "%d/%m/%Y %H:%M")
            except ValueError:
                raw = input("Date invalide, format attendu JJ/MM/AAAA HH:MM: ")

    def _prompt_int(self, prompt):
        raw = input(prompt)
        while True:
            try:
                return int(raw)
            except ValueError:
                raw = input("Nombre invalide, saisissez un entier: ")

    def create_event(self):
        event_name = input("nom de l'evenement: ")
        date_start = self._prompt_datetime("date de debut (JJ/MM/AAAA HH:MM): ")
        date_end = self._prompt_datetime("date de fin (JJ/MM/AAAA HH:MM): ")
        location = input("lieu: ")
        attendees = self._prompt_int("nombre de participants: ")
        notes = input("notes: ")
        contract_id = input("identifiant du contract: ")

        return (
            event_name,
            contract_id,
            date_start,
            date_end,
            location,
            attendees,
            notes,
        )

    def prompt_support_email(self):
        return input("email du support à assigner: ")

    def display_event(self, event: Event):
        print(
            f"{event.event_name}\n"
            f"début: {event.date_start} / fin: {event.date_end}\n"
            f"lieu: {event.location}\n"
            f"nombre de participant: {event.attendees}\n"
            f"notes: {event.notes}"
        )

    def display_events_list(self, events):
        for event in events:
            self.display_event(event)
            print("---")

    def update_event_name(self):
        return input("nouveau nom de l'evenement: ")

    def update_date_start(self):
        return self._prompt_datetime("nouvelle date de debut (JJ/MM/AAAA HH:MM): ")

    def update_date_end(self):
        return self._prompt_datetime("nouvelle date de fin (JJ/MM/AAAA HH:MM): ")

    def update_location(self):
        return input("nouveau lieu: ")

    def update_attendees(self):
        return self._prompt_int("nouveau nombre de participants: ")

    def update_notes(self):
        return input("nouvelles notes: ")
