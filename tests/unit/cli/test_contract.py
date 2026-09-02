from decimal import Decimal

from cli import session
from cli.main import cli
from models.client import Client
from models.contract import Contract
from models.user import UserRole
from tests.factories import build_user


def login_as(user):
    session.create_session(user)


def make_client(cli_persist, commercial_id, email="marie@example.com"):
    return cli_persist(
        Client(
            first_name="Marie",
            last_name="Curie",
            email=email,
            phone="0600000000",
            company="ACME",
            commercial_id=commercial_id,
        )
    )


def test_create_contract_as_gestion_succeeds(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    make_client(cli_persist, commercial.id)
    login_as(gestion)

    result = cli_runner.invoke(
        cli, ["contract", "create"], input="1000.00\n500.00\nmarie@example.com\n"
    )

    assert result.exit_code == 0
    assert "Contrat cree" in result.output
    assert "500.00/1000.00" in result.output


def test_create_contract_as_commercial_is_denied(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    make_client(cli_persist, commercial.id)
    login_as(commercial)

    result = cli_runner.invoke(
        cli, ["contract", "create"], input="1000.00\n500.00\nmarie@example.com\n"
    )

    assert result.exit_code == 1
    assert "Acces refuse" in result.output


def test_list_unsigned_contracts_filters_correctly(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    client_a = make_client(cli_persist, commercial.id, email="a@example.com")
    client_b = make_client(cli_persist, commercial.id, email="b@example.com")
    cli_persist(
        Contract(
            total_amount=Decimal("100"), remaining_amount=Decimal("0"),
            signed=True, client_id=client_a.id,
        )
    )
    cli_persist(
        Contract(
            total_amount=Decimal("200"), remaining_amount=Decimal("200"),
            signed=False, client_id=client_b.id,
        )
    )
    login_as(gestion)

    result = cli_runner.invoke(cli, ["contract", "list", "--unsigned"])

    assert result.exit_code == 0
    assert "non" in result.output
    assert "200" in result.output


def test_show_contract_displays_details(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    client_row = make_client(cli_persist, commercial.id)
    contract_row = cli_persist(
        Contract(
            total_amount=Decimal("1000"), remaining_amount=Decimal("500"),
            signed=False, client_id=client_row.id,
        )
    )
    login_as(gestion)

    result = cli_runner.invoke(cli, ["contract", "show", str(contract_row.id)])

    assert result.exit_code == 0
    assert str(contract_row.id) in result.output
    assert "Marie Curie" in result.output


def test_show_contract_with_unknown_id_shows_not_found(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    login_as(gestion)

    result = cli_runner.invoke(
        cli, ["contract", "show", "00000000-0000-0000-0000-000000000000"]
    )

    assert result.exit_code == 1
    assert "introuvable" in result.output


def test_update_contract_as_owning_commercial_succeeds(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    owned_client = make_client(cli_persist, commercial.id)
    contract_row = cli_persist(
        Contract(
            total_amount=Decimal("1000"), remaining_amount=Decimal("1000"),
            signed=False, client_id=owned_client.id,
        )
    )
    login_as(commercial)

    result = cli_runner.invoke(
        cli, ["contract", "update", str(contract_row.id)], input="signe\no\nn\n"
    )

    assert result.exit_code == 0
    assert "Signe : True" in result.output


def test_create_contract_with_unknown_client_email_shows_not_found(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    login_as(gestion)

    result = cli_runner.invoke(
        cli, ["contract", "create"], input="1000.00\n500.00\nunknown@example.com\n"
    )

    assert result.exit_code == 1
    assert "Client introuvable" in result.output


def test_update_contract_with_unknown_id_shows_not_found(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    login_as(gestion)

    result = cli_runner.invoke(
        cli, ["contract", "update", "00000000-0000-0000-0000-000000000000"]
    )

    assert result.exit_code == 1
    assert "introuvable" in result.output
