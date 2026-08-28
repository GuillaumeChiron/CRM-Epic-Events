from types import SimpleNamespace
from uuid import uuid4

from models.user import UserRole
from permissions.permission import gestion_required, owner_required
from tests.factories import build_user


class DummyRoleGuard:
    def __init__(self):
        self.called_with = None

    @gestion_required
    def gestion_only(self, current_user, value):
        self.called_with = value
        return value


class DummyOwnerGuard:
    def __init__(self):
        self.called = False

    @owner_required(lambda item, *a, **kw: item.owner_id, "gestion")
    def act(self, current_user, item):
        self.called = True
        return "done"


def test_roles_required_allows_matching_role():
    dummy = DummyRoleGuard()
    user = build_user(role=UserRole.gestion)

    result = dummy.gestion_only(user, "ok")

    assert result == "ok"
    assert dummy.called_with == "ok"


def test_roles_required_blocks_non_matching_role():
    dummy = DummyRoleGuard()
    user = build_user(role=UserRole.commercial)

    result = dummy.gestion_only(user, "ok")

    assert result is False
    assert dummy.called_with is None


def test_owner_required_allows_owner():
    dummy = DummyOwnerGuard()
    user = build_user(role=UserRole.commercial)
    item = SimpleNamespace(owner_id=user.id)

    result = dummy.act(user, item)

    assert result == "done"
    assert dummy.called is True


def test_owner_required_blocks_non_owner():
    dummy = DummyOwnerGuard()
    user = build_user(role=UserRole.commercial)
    item = SimpleNamespace(owner_id=uuid4())

    result = dummy.act(user, item)

    assert result is False
    assert dummy.called is False


def test_owner_required_bypass_role_ignores_ownership():
    dummy = DummyOwnerGuard()
    user = build_user(role=UserRole.gestion)
    item = SimpleNamespace(owner_id=uuid4())

    result = dummy.act(user, item)

    assert result == "done"
    assert dummy.called is True
