from datetime import datetime, timedelta, timezone

import jwt
import pytest

from cli import session
from models.user import UserRole
from tests.factories import build_user


@pytest.fixture()
def session_file(tmp_path):
    return tmp_path / "session.json"


def test_create_then_read_session_returns_same_user_id(session_file):
    user = build_user(role=UserRole.gestion)

    session.create_session(user, session_file=session_file)
    user_id = session.read_current_user_id(session_file=session_file)

    assert user_id == user.id


def test_read_current_user_id_returns_none_when_file_missing(session_file):
    assert session.read_current_user_id(session_file=session_file) is None


def test_read_current_user_id_returns_none_for_tampered_token(session_file):
    user = build_user()
    session.create_session(user, session_file=session_file)

    session_file.write_text(session_file.read_text() + "tampered")

    assert session.read_current_user_id(session_file=session_file) is None


def test_read_current_user_id_returns_none_for_expired_token(session_file):
    user = build_user()
    now = datetime.now(timezone.utc)
    expired_token = jwt.encode(
        {
            "sub": str(user.id),
            "role": user.role.name,
            "iat": now - timedelta(hours=9),
            "exp": now - timedelta(hours=1),
        },
        session.SECRET_KEY,
        algorithm=session.ALGORITHM,
    )
    session_file.parent.mkdir(parents=True, exist_ok=True)
    session_file.write_text(expired_token)

    assert session.read_current_user_id(session_file=session_file) is None


def test_clear_session_removes_file(session_file):
    user = build_user()
    session.create_session(user, session_file=session_file)

    session.clear_session(session_file=session_file)

    assert not session_file.exists()


def test_clear_session_does_not_fail_when_file_missing(session_file):
    session.clear_session(session_file=session_file)
