from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

from models.event import Event
from uuid import UUID
from collections.abc import Sequence


class EventView:

    def __init__(self, console: Console | None = None):
        self.console = console or Console()

    # Demande une date au user
    def _prompt_datetime(self, prompt: str) -> datetime:
        raw = Prompt.ask(prompt)
        while True:
            try:
                return datetime.strptime(raw, "%d/%m/%Y %H:%M")
            except ValueError:
                self.console.print(
                    "[red]Date invalide, format attendu JJ/MM/AAAA HH:MM[/red]"
                )
                raw = Prompt.ask(prompt)

    # Demande un nombre au user
    def _prompt_int(self, prompt: str) -> int:
        return IntPrompt.ask(prompt)

    # Demande les attributs de l'evenement au user
    def create_event(self) -> tuple[str, UUID, datetime, datetime, str, int, str]:
        event_name = Prompt.ask("nom de l'evenement")
        date_start = self._prompt_datetime("date de debut (JJ/MM/AAAA HH:MM)")
        date_end = self._prompt_datetime("date de fin (JJ/MM/AAAA HH:MM)")
        location = Prompt.ask("lieu")
        attendees = self._prompt_int("nombre de participants")
        notes = Prompt.ask("notes")
        contract_id = Prompt.ask("identifiant du contract")

        return (
            event_name,
            contract_id,
            date_start,
            date_end,
            location,
            attendees,
            notes,
        )

    # Demande l'email du support associé au user
    def prompt_support_email(self) -> str:
        return Prompt.ask("email du support a assigner")

    # Affiche un evenement
    def display_event(self, event: Event):
        body = (
            f"Debut : {event.date_start} / Fin : {event.date_end}\n"
            f"Lieu : {event.location}\n"
            f"Participants : {event.attendees}\n"
            f"Notes : {event.notes}"
        )
        self.console.print(Panel(body, title=event.event_name))

    # Affiche sous forme d'un tableau tous les evenements
    def display_events_list(self, events: Sequence[Event]):
        table = Table(title="Evenements")
        table.add_column("#", no_wrap=True)
        table.add_column("Nom", no_wrap=True)
        table.add_column("Debut")
        table.add_column("Fin")
        table.add_column("Lieu")
        table.add_column("Participants")
        table.add_column("Support")

        for index, event in enumerate(events, start=1):
            table.add_row(
                str(index),
                event.event_name,
                str(event.date_start),
                str(event.date_end),
                event.location,
                str(event.attendees),
                (
                    f"{event.support.first_name} {event.support.last_name}"
                    if event.support
                    else "-"
                ),
            )

        self.console.print(table)

    # Demande le nouvel attribut au user pour une modification evenement
    def update_event_name(self) -> str:
        return Prompt.ask("nouveau nom de l'evenement")

    def update_date_start(self) -> str:
        return self._prompt_datetime("nouvelle date de debut (JJ/MM/AAAA HH:MM)")

    def update_date_end(self) -> str:
        return self._prompt_datetime("nouvelle date de fin (JJ/MM/AAAA HH:MM)")

    def update_location(self) -> str:
        return Prompt.ask("nouveau lieu")

    def update_attendees(self) -> str:
        return self._prompt_int("nouveau nombre de participants")

    def update_notes(self) -> str:
        return Prompt.ask("nouvelles notes")
