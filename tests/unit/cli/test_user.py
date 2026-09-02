from cli import session
from cli.main import cli
from models.user import UserRole
from tests.factories import build_user


def login_as(user):
    session.create_session(user)


def test_create_user_as_gestion_succeeds(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    login_as(gestion)

    result = cli_runner.invoke(
        cli,
        ["user", "create"],
        input="jean@example.com\ns3cret!\nJean\nDupont\ncommercial\n",
    )

    assert result.exit_code == 0
    assert "Collaborateur cree" in result.output
    assert "jean@example.com" in result.output


def test_create_user_as_commercial_is_denied(cli_runner, cli_persist):
    commercial = cli_persist(build_user(role=UserRole.commercial, email="c@example.com"))
    login_as(commercial)

    result = cli_runner.invoke(
        cli,
        ["user", "create"],
        input="jean@example.com\ns3cret!\nJean\nDupont\ncommercial\n",
    )

    assert result.exit_code == 1
    assert "Acces refuse" in result.output


def test_list_users_shows_existing_users(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    login_as(gestion)

    result = cli_runner.invoke(cli, ["user", "list"])

    assert result.exit_code == 0
    assert "g@example.com" in result.output


def test_show_user_displays_details(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    target = cli_persist(build_user(role=UserRole.support, email="s@example.com"))
    login_as(gestion)

    result = cli_runner.invoke(cli, ["user", "show", target.email])

    assert result.exit_code == 0
    assert "s@example.com" in result.output


def test_show_user_with_unknown_email_shows_not_found(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    login_as(gestion)

    result = cli_runner.invoke(cli, ["user", "show", "missing@example.com"])

    assert result.exit_code == 1
    assert "introuvable" in result.output


def test_update_user_role_as_gestion_succeeds(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    target = cli_persist(build_user(role=UserRole.support, email="s@example.com"))
    login_as(gestion)

    result = cli_runner.invoke(
        cli, ["user", "update", target.email], input="role\ncommercial\nn\n"
    )

    assert result.exit_code == 0
    assert "commercial:" in result.output


def test_delete_user_with_confirmation_succeeds(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    target = cli_persist(build_user(role=UserRole.support, email="s@example.com"))
    login_as(gestion)

    result = cli_runner.invoke(cli, ["user", "delete", target.email], input="o\n")

    assert result.exit_code == 0
    assert "Collaborateur supprime" in result.output


def test_delete_user_without_confirmation_is_cancelled(cli_runner, cli_persist):
    gestion = cli_persist(build_user(role=UserRole.gestion, email="g@example.com"))
    target = cli_persist(build_user(role=UserRole.support, email="s@example.com"))
    login_as(gestion)

    result = cli_runner.invoke(cli, ["user", "delete", target.email], input="n\n")

    assert result.exit_code == 0
    assert "Annule" in result.output
