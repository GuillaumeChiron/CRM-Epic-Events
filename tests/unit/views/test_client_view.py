from datetime import datetime

from models.client import Client
from views.client_view import ClientView


def test_create_client_reads_all_fields(monkeypatch):
    view = ClientView()
    inputs = iter(["Marie", "Curie", "marie@example.com", "0600000000", "ACME"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    result = view.create_client()

    assert result == ("Marie", "Curie", "marie@example.com", "0600000000", "ACME")


def test_prompt_date_retries_on_invalid_format(monkeypatch):
    view = ClientView()
    inputs = iter(["31-12-2024", "31/12/2024"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    result = view.update_last_contact_at()

    assert result == datetime(2024, 12, 31)


def test_display_client_prints_expected_fields(capsys):
    view = ClientView()
    client = Client(
        first_name="Marie",
        last_name="Curie",
        email="marie@example.com",
        phone="0600000000",
        company="ACME",
    )

    view.display_client(client)

    captured = capsys.readouterr()
    assert "Marie Curie" in captured.out
    assert "ACME" in captured.out


def test_display_clients_list_prints_a_row_per_client(capsys):
    view = ClientView()
    clients = [
        Client(first_name="A", last_name="B", email="a@b.com", phone="1", company="C1"),
        Client(first_name="C", last_name="D", email="c@d.com", phone="2", company="C2"),
    ]

    view.display_clients_list(clients)

    captured = capsys.readouterr()
    assert "a@b.com" in captured.out
    assert "c@d.com" in captured.out
