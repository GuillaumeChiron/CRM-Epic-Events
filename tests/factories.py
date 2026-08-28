from uuid import uuid4
from decimal import Decimal
from datetime import datetime, timedelta

from models.user import User, UserRole
from models.client import Client
from models.contract import Contract
from models.event import Event


def build_user(role=UserRole.commercial, **kwargs):
    return User(
        id=kwargs.pop("id", uuid4()),
        email=kwargs.pop("email", f"user-{uuid4()}@example.com"),
        password_hash=kwargs.pop("password_hash", "hash"),
        first_name=kwargs.pop("first_name", "Jean"),
        last_name=kwargs.pop("last_name", "Dupont"),
        role=role,
        **kwargs,
    )


def build_client(commercial_id=None, **kwargs):
    return Client(
        id=kwargs.pop("id", uuid4()),
        first_name=kwargs.pop("first_name", "Marie"),
        last_name=kwargs.pop("last_name", "Curie"),
        email=kwargs.pop("email", f"client-{uuid4()}@example.com"),
        phone=kwargs.pop("phone", "0600000000"),
        company=kwargs.pop("company", "ACME"),
        commercial_id=commercial_id,
        **kwargs,
    )


def build_contract(client=None, **kwargs):
    data = dict(
        id=kwargs.pop("id", uuid4()),
        total_amount=kwargs.pop("total_amount", Decimal("1000.00")),
        remaining_amount=kwargs.pop("remaining_amount", Decimal("500.00")),
        signed=kwargs.pop("signed", True),
    )

    if "client_id" in kwargs:
        data["client_id"] = kwargs.pop("client_id")
    elif client is not None:
        data["client_id"] = client.id
    else:
        data["client_id"] = uuid4()

    if client is not None:
        data["client"] = client

    data.update(kwargs)
    return Contract(**data)


def build_event(contract=None, **kwargs):
    now = datetime(2026, 1, 1, 20, 0)
    data = dict(
        id=kwargs.pop("id", uuid4()),
        event_name=kwargs.pop("event_name", "Soiree"),
        date_start=kwargs.pop("date_start", now),
        date_end=kwargs.pop("date_end", now + timedelta(hours=2)),
        location=kwargs.pop("location", "Paris"),
        attendees=kwargs.pop("attendees", 50),
        notes=kwargs.pop("notes", None),
        support_id=kwargs.pop("support_id", None),
    )

    if "contract_id" in kwargs:
        data["contract_id"] = kwargs.pop("contract_id")
    elif contract is not None:
        data["contract_id"] = contract.id
    else:
        data["contract_id"] = uuid4()

    if contract is not None:
        data["contract"] = contract

    data.update(kwargs)
    return Event(**data)
