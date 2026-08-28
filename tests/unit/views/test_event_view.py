from datetime import datetime

from models.event import Event
from views.event_view import EventView


def test_prompt_datetime_retries_on_invalid_format(monkeypatch):
    view = EventView()
    inputs = iter(["31/12/2024", "31/12/2024 20:00"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    result = view._prompt_datetime("date: ")

    assert result == datetime(2024, 12, 31, 20, 0)


def test_prompt_int_retries_on_invalid_input(monkeypatch):
    view = EventView()
    inputs = iter(["abc", "50"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    result = view._prompt_int("participants: ")

    assert result == 50


def test_create_event_reads_all_fields(monkeypatch):
    view = EventView()
    inputs = iter(
        ["Soiree", "31/12/2024 20:00", "31/12/2024 23:00", "Paris", "50", "notes", "contract-id"]
    )
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    result = view.create_event()

    assert result == (
        "Soiree",
        "contract-id",
        datetime(2024, 12, 31, 20, 0),
        datetime(2024, 12, 31, 23, 0),
        "Paris",
        50,
        "notes",
    )


def test_display_event_prints_expected_fields(capsys):
    view = EventView()
    event = Event(
        event_name="Soiree",
        date_start=datetime(2024, 12, 31, 20, 0),
        date_end=datetime(2024, 12, 31, 23, 0),
        location="Paris",
        attendees=50,
        notes="RAS",
    )

    view.display_event(event)

    captured = capsys.readouterr()
    assert "Soiree" in captured.out
    assert "Paris" in captured.out
