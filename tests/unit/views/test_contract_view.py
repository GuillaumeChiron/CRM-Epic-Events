from decimal import Decimal

from models.client import Client
from models.contract import Contract
from views.contract_view import ContractView


def test_prompt_decimal_retries_on_invalid_input(monkeypatch):
    view = ContractView()
    inputs = iter(["abc", "1500.00"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    result = view._prompt_decimal("montant: ")

    assert result == Decimal("1500.00")


def test_prompt_bool_retries_until_valid_choice(monkeypatch):
    view = ContractView()
    inputs = iter(["maybe", "o"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    result = view._prompt_bool("signe ? ")

    assert result is True


def test_create_contract_reads_amounts_and_email(monkeypatch):
    view = ContractView()
    inputs = iter(["1000.00", "500.00", "client@example.com"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    total, remaining, email = view.create_contract()

    assert total == Decimal("1000.00")
    assert remaining == Decimal("500.00")
    assert email == "client@example.com"


def test_display_contract_prints_expected_fields(capsys):
    view = ContractView()
    client = Client(
        first_name="Marie", last_name="Curie", email="m@c.com", phone="0600000000", company="ACME"
    )
    contract = Contract(
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        signed=True,
        client=client,
    )

    view.display_contract(contract)

    captured = capsys.readouterr()
    assert "ACME" in captured.out
    assert "500.00/1000.00" in captured.out
