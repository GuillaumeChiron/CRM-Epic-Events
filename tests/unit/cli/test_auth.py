from argon2 import PasswordHasher

from cli.main import cli
from cli import session
from models.user import UserRole
from tests.factories import build_user

ph = PasswordHasher()


def make_user(cli_persist, password, **kwargs):
    user = build_user(password_hash=ph.hash(password), **kwargs)
    return cli_persist(user)


def test_login_with_valid_credentials_creates_session(cli_runner, cli_persist):
    user = make_user(cli_persist, "s3cret!", email="gestion@example.com", role=UserRole.gestion)

    result = cli_runner.invoke(cli, ["auth", "login"], input="gestion@example.com\ns3cret!\n")

    assert result.exit_code == 0
    assert "Connecte en tant que" in result.output
    assert session.read_current_user_id() == user.id


def test_login_with_invalid_password_is_rejected(cli_runner, cli_persist):
    make_user(cli_persist, "s3cret!", email="gestion@example.com", role=UserRole.gestion)

    result = cli_runner.invoke(cli, ["auth", "login"], input="gestion@example.com\nwrong\n")

    assert result.exit_code == 1
    assert "Authentification echouee" in result.output
    assert session.read_current_user_id() is None


def test_whoami_without_login_asks_to_login(cli_runner):
    result = cli_runner.invoke(cli, ["auth", "whoami"])

    assert result.exit_code == 1
    assert "Veuillez vous connecter" in result.output


def test_whoami_after_login_shows_current_user(cli_runner, cli_persist):
    make_user(cli_persist, "s3cret!", email="commercial@example.com", role=UserRole.commercial)
    cli_runner.invoke(cli, ["auth", "login"], input="commercial@example.com\ns3cret!\n")

    result = cli_runner.invoke(cli, ["auth", "whoami"])

    assert result.exit_code == 0
    assert "commercial@example.com" in result.output


def test_logout_clears_session(cli_runner, cli_persist):
    make_user(cli_persist, "s3cret!", email="support@example.com", role=UserRole.support)
    cli_runner.invoke(cli, ["auth", "login"], input="support@example.com\ns3cret!\n")

    result = cli_runner.invoke(cli, ["auth", "logout"])

    assert result.exit_code == 0
    assert session.read_current_user_id() is None

    whoami_result = cli_runner.invoke(cli, ["auth", "whoami"])
    assert "Veuillez vous connecter" in whoami_result.output
