from unittest.mock import MagicMock

import pytest
from argon2 import PasswordHasher

from models.user import UserRole
from services.user_service import UserService
from tests.factories import build_user


@pytest.fixture()
def repository():
    return MagicMock()


@pytest.fixture()
def service(repository):
    return UserService(repository)


class TestCreateUser:
    def test_gestion_can_create_user(self, service, repository):
        current_user = build_user(role=UserRole.gestion)

        user = service.create_user(
            current_user, "new@example.com", "s3cret", "Jean", "Dupont", UserRole.commercial
        )

        assert user.email == "new@example.com"
        assert user.password_hash != "s3cret"
        repository.create.assert_called_once_with(user)

    def test_non_gestion_cannot_create_user(self, service, repository):
        current_user = build_user(role=UserRole.commercial)

        result = service.create_user(
            current_user, "new@example.com", "s3cret", "Jean", "Dupont", UserRole.commercial
        )

        assert result is False
        repository.create.assert_not_called()

    def test_create_user_logs_to_sentry(self, service, repository, monkeypatch):
        mock_capture = MagicMock()
        monkeypatch.setattr("sentry_sdk.capture_message", mock_capture)
        current_user = build_user(role=UserRole.gestion)

        user = service.create_user(
            current_user, "new@example.com", "s3cret", "Jean", "Dupont", UserRole.commercial
        )

        mock_capture.assert_called_once_with(
            f"Collaborateur cree : {user.email}", level="info"
        )

    def test_create_user_denied_does_not_log_to_sentry(self, service, repository, monkeypatch):
        mock_capture = MagicMock()
        monkeypatch.setattr("sentry_sdk.capture_message", mock_capture)
        current_user = build_user(role=UserRole.commercial)

        service.create_user(
            current_user, "new@example.com", "s3cret", "Jean", "Dupont", UserRole.commercial
        )

        mock_capture.assert_not_called()


class TestAuthenticate:
    def test_authenticate_with_valid_credentials(self, service, repository):
        ph = PasswordHasher()
        user = build_user(password_hash=ph.hash("s3cret"))
        repository.get_by_email.return_value = user

        result = service.authenticate(user.email, "s3cret")

        assert result is user

    def test_authenticate_with_unknown_email(self, service, repository):
        repository.get_by_email.return_value = None

        result = service.authenticate("missing@example.com", "s3cret")

        assert result is None

    def test_authenticate_with_wrong_password(self, service, repository):
        ph = PasswordHasher()
        user = build_user(password_hash=ph.hash("s3cret"))
        repository.get_by_email.return_value = user

        result = service.authenticate(user.email, "wrong")

        assert result is None


def test_list_users_delegates_to_repository(service, repository):
    repository.users_list.return_value = ["u1", "u2"]

    result = service.list_users()

    assert result == ["u1", "u2"]
    repository.users_list.assert_called_once()


@pytest.mark.parametrize(
    "method, args",
    [
        ("update_email", ("new@example.com",)),
        ("update_password", ("new-pass",)),
        ("update_first_name", ("Paul",)),
        ("update_last_name", ("Martin",)),
        ("update_role", (UserRole.support,)),
        ("delete_user", ()),
    ],
)
class TestGestionOnlyActions:
    def test_gestion_can_perform_action(self, service, repository, method, args):
        current_user = build_user(role=UserRole.gestion)
        target_user = build_user(role=UserRole.support)

        getattr(service, method)(current_user, target_user, *args)

        assert getattr(repository, method).call_count == 1

    def test_non_gestion_cannot_perform_action(self, service, repository, method, args):
        current_user = build_user(role=UserRole.commercial)
        target_user = build_user(role=UserRole.support)

        result = getattr(service, method)(current_user, target_user, *args)

        assert result is False
        getattr(repository, method).assert_not_called()


@pytest.mark.parametrize(
    "method, args",
    [
        ("update_email", ("new@example.com",)),
        ("update_password", ("new-pass",)),
        ("update_first_name", ("Paul",)),
        ("update_last_name", ("Martin",)),
        ("update_role", (UserRole.support,)),
    ],
)
class TestUserUpdateSentryLogging:
    def test_update_logs_to_sentry(self, service, repository, monkeypatch, method, args):
        mock_capture = MagicMock()
        monkeypatch.setattr("sentry_sdk.capture_message", mock_capture)
        current_user = build_user(role=UserRole.gestion)
        target_user = build_user(role=UserRole.support)

        getattr(service, method)(current_user, target_user, *args)

        mock_capture.assert_called_once_with(
            f"Collaborateur modifie : {target_user.email}", level="info"
        )

    def test_denied_update_does_not_log_to_sentry(
        self, service, repository, monkeypatch, method, args
    ):
        mock_capture = MagicMock()
        monkeypatch.setattr("sentry_sdk.capture_message", mock_capture)
        current_user = build_user(role=UserRole.commercial)
        target_user = build_user(role=UserRole.support)

        getattr(service, method)(current_user, target_user, *args)

        mock_capture.assert_not_called()
