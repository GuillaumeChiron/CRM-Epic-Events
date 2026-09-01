from cli import session
from cli.main import cli
from models.client import Client
from models.user import UserRole
from tests.factories import build_user


def login_as(user):
    session.create_session(user)


def test_create_client_as_commercial_succeeds(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    login_as(commercial)

    result = cli_runner.invoke(
        cli,
        ["client", "create"],
        input="Marie\nCurie\nmarie@example.com\n0600000000\nACME\n",
    )

    assert result.exit_code == 0
    assert "Client cree" in result.output
    assert "marie@example.com" in result.output


def test_create_client_as_support_is_denied(cli_runner, cli_persist):
    support = cli_persist(build_user(role=UserRole.support, email="s@example.com"))
    login_as(support)

    result = cli_runner.invoke(
        cli,
        ["client", "create"],
        input="Marie\nCurie\nmarie@example.com\n0600000000\nACME\n",
    )

    assert result.exit_code == 1
    assert "Acces refuse" in result.output


def test_list_clients_shows_existing_clients(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    cli_persist(
        Client(
            first_name="Marie",
            last_name="Curie",
            email="marie@example.com",
            phone="0600000000",
            company="ACME",
            commercial_id=commercial.id,
        )
    )
    login_as(commercial)

    result = cli_runner.invoke(cli, ["client", "list"])

    assert result.exit_code == 0
    assert "marie@example.com" in result.output


def test_update_client_by_owner_commercial_succeeds(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    owned_client = cli_persist(
        Client(
            first_name="Marie",
            last_name="Curie",
            email="marie@example.com",
            phone="0600000000",
            company="ACME",
            commercial_id=commercial.id,
        )
    )
    login_as(commercial)

    result = cli_runner.invoke(
        cli,
        ["client", "update", str(owned_client.id)],
        input="email\nmarie.curie@example.com\nn\n",
    )

    assert result.exit_code == 0
    assert "marie.curie@example.com" in result.output


def test_update_client_by_non_owner_commercial_is_denied(cli_runner, cli_persist):
    owner = cli_persist(build_user(role=UserRole.commercial, email="owner@example.com"))
    other = cli_persist(build_user(role=UserRole.commercial, email="other@example.com"))
    owned_client = cli_persist(
        Client(
            first_name="Marie",
            last_name="Curie",
            email="marie@example.com",
            phone="0600000000",
            company="ACME",
            commercial_id=owner.id,
        )
    )
    login_as(other)

    result = cli_runner.invoke(
        cli,
        ["client", "update", str(owned_client.id)],
        input="email\nmarie.curie@example.com\n",
    )

    assert result.exit_code == 1
    assert "Acces refuse" in result.output


def test_update_client_with_unknown_id_shows_not_found(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    login_as(commercial)

    result = cli_runner.invoke(cli, ["client", "update", "00000000-0000-0000-0000-000000000000"])

    assert result.exit_code == 1
    assert "introuvable" in result.output
