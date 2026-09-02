from decimal import Decimal
from datetime import datetime

from cli import session
from cli.main import cli
from models.client import Client
from models.contract import Contract
from models.event import Event
from models.user import UserRole
from tests.factories import build_user


def login_as(user):
    session.create_session(user)


def make_signed_contract(cli_persist, commercial_id):
    client = cli_persist(
        Client(
            first_name="Marie",
            last_name="Curie",
            email="marie@example.com",
            phone="0600000000",
            company="ACME",
            commercial_id=commercial_id,
        )
    )
    return cli_persist(
        Contract(
            total_amount=Decimal("1000"),
            remaining_amount=Decimal("1000"),
            signed=True,
            client_id=client.id,
        )
    )


def test_create_event_for_own_signed_contract_succeeds(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    contract = make_signed_contract(cli_persist, commercial.id)
    login_as(commercial)

    result = cli_runner.invoke(
        cli,
        ["event", "create"],
        input=(
            "Mariage\n"
            "01/06/2026 13:00\n"
            "02/06/2026 02:00\n"
            "Paris\n"
            "75\n"
            "RAS\n"
            f"{contract.id}\n"
        ),
    )

    assert result.exit_code == 0
    assert "Evenement cree" in result.output
    assert "Mariage" in result.output


def test_create_event_for_unsigned_contract_is_rejected(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    client = cli_persist(
        Client(
            first_name="Marie", last_name="Curie", email="marie@example.com",
            phone="0600000000", company="ACME", commercial_id=commercial.id,
        )
    )
    unsigned_contract = cli_persist(
        Contract(
            total_amount=Decimal("1000"), remaining_amount=Decimal("1000"),
            signed=False, client_id=client.id,
        )
    )
    login_as(commercial)

    result = cli_runner.invoke(
        cli,
        ["event", "create"],
        input=(
            "Mariage\n01/06/2026 13:00\n02/06/2026 02:00\nParis\n75\nRAS\n"
            f"{unsigned_contract.id}\n"
        ),
    )

    assert result.exit_code == 1
    assert "non signe" in result.output


def test_list_events_without_support(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    contract = make_signed_contract(cli_persist, commercial.id)
    cli_persist(
        Event(
            event_name="Sans support",
            date_start=datetime(2026, 6, 1, 13, 0),
            date_end=datetime(2026, 6, 2, 2, 0),
            location="Paris",
            attendees=75,
            contract_id=contract.id,
            support_id=None,
        )
    )
    login_as(gestion)

    result = cli_runner.invoke(cli, ["event", "list", "--no-support"])

    assert result.exit_code == 0
    assert "Sans support" in result.output


def test_assign_support_as_gestion_succeeds(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    cli_persist(build_user(role=UserRole.support, email="support@example.com"))
    contract = make_signed_contract(cli_persist, commercial.id)
    target_event = cli_persist(
        Event(
            event_name="Mariage",
            date_start=datetime(2026, 6, 1, 13, 0),
            date_end=datetime(2026, 6, 2, 2, 0),
            location="Paris",
            attendees=75,
            contract_id=contract.id,
        )
    )
    login_as(gestion)

    result = cli_runner.invoke(
        cli, ["event", "assign-support", str(target_event.id)], input="support@example.com\n"
    )

    assert result.exit_code == 0
    assert "Support assigne" in result.output


def test_assign_support_with_unknown_email_shows_not_found(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    contract = make_signed_contract(cli_persist, commercial.id)
    target_event = cli_persist(
        Event(
            event_name="Mariage",
            date_start=datetime(2026, 6, 1, 13, 0),
            date_end=datetime(2026, 6, 2, 2, 0),
            location="Paris",
            attendees=75,
            contract_id=contract.id,
        )
    )
    login_as(gestion)

    result = cli_runner.invoke(
        cli, ["event", "assign-support", str(target_event.id)], input="unknown@example.com\n"
    )

    assert result.exit_code == 1
    assert "Collaborateur introuvable" in result.output


def test_assign_support_as_commercial_is_denied(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    contract = make_signed_contract(cli_persist, commercial.id)
    target_event = cli_persist(
        Event(
            event_name="Mariage",
            date_start=datetime(2026, 6, 1, 13, 0),
            date_end=datetime(2026, 6, 2, 2, 0),
            location="Paris",
            attendees=75,
            contract_id=contract.id,
        )
    )
    login_as(commercial)

    result = cli_runner.invoke(
        cli, ["event", "assign-support", str(target_event.id)], input="anyone@example.com\n"
    )

    assert result.exit_code == 1
    assert "Acces refuse" in result.output


def test_update_event_by_assigned_support_succeeds(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    support = cli_persist(build_user(role=UserRole.support, email="support@example.com"))
    contract = make_signed_contract(cli_persist, commercial.id)
    target_event = cli_persist(
        Event(
            event_name="Mariage",
            date_start=datetime(2026, 6, 1, 13, 0),
            date_end=datetime(2026, 6, 2, 2, 0),
            location="Paris",
            attendees=75,
            contract_id=contract.id,
            support_id=support.id,
        )
    )
    login_as(support)

    result = cli_runner.invoke(
        cli, ["event", "update", str(target_event.id)], input="lieu\nLyon\nn\n"
    )

    assert result.exit_code == 0
    assert "Lieu : Lyon" in result.output
