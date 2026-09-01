import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
SESSION_LIFETIME = timedelta(hours=8)
SESSION_FILE = Path.home() / ".epicevents" / "session.json"


def create_session(user, session_file: Path | None = None) -> None:
    session_file = session_file or SESSION_FILE
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "role": user.role.name,
        "iat": now,
        "exp": now + SESSION_LIFETIME,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    session_file.parent.mkdir(parents=True, exist_ok=True)
    session_file.write_text(token)
    try:
        os.chmod(session_file, 0o600)
    except OSError:
        pass


def read_current_user_id(session_file: Path | None = None) -> UUID | None:
    session_file = session_file or SESSION_FILE
    if not session_file.exists():
        return None

    token = session_file.read_text().strip()
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return None

    return UUID(payload["sub"])


def clear_session(session_file: Path | None = None) -> None:
    session_file = session_file or SESSION_FILE
    session_file.unlink(missing_ok=True)
