from models.event import Event


class EventView:

    def create_event(self):

        event_name = input("nom de l'evenement: ")
        date_start = input("date de debut: ")
        date_end = input("date de fin: ")
        location = input("lieu: ")
        attendees = input("nombre de participants: ")
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

    def display_event(self, event: Event):
        print(
            f"{event.event_name}\n"
            f"début: {event.date_start} / fin: {event.date_end}\n"
            f"lieu: {event.location}\n"
            f"nombre de participant: {event.attendees}\n"
            f"notes: {event.notes}"
        )
