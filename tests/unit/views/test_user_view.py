from models.user import User, UserRole
from views.user_view import UserView


def test_login_reads_email_and_password(monkeypatch):
    view = UserView()
    inputs = iter(["a@b.com", "secret"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    email, password = view.login()

    assert email == "a@b.com"
    assert password == "secret"


def test_create_user_retries_until_valid_role(monkeypatch):
    view = UserView()
    inputs = iter(["a@b.com", "secret", "Jean", "Dupont", "invalide", "commercial"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    result = view.create_user()

    assert result == ("a@b.com", "secret", "Jean", "Dupont", "commercial")


def test_display_user_prints_expected_format(capsys):
    view = UserView()
    user = User(
        email="a@b.com",
        password_hash="hash",
        first_name="Jean",
        last_name="Dupont",
        role=UserRole.commercial,
    )

    view.display_user(user)

    captured = capsys.readouterr()
    assert "commercial: Jean Dupont" in captured.out
    assert "a@b.com" in captured.out


def test_display_users_list_prints_separator_between_entries(capsys):
    view = UserView()
    users = [
        User(email="a@b.com", password_hash="h", first_name="A", last_name="B", role=UserRole.commercial),
        User(email="c@d.com", password_hash="h", first_name="C", last_name="D", role=UserRole.gestion),
    ]

    view.display_users_list(users)

    captured = capsys.readouterr()
    assert captured.out.count("---") == 2
