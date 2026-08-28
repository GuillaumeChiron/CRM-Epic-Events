from datetime import datetime
from decimal import Decimal

from models.user import UserRole
from repositories.client_repository import ClientRepository
from repositories.contract_repository import ContractRepository
from repositories.event_repository import EventRepository
from repositories.user_repository import UserRepository
from services.client_service import ClientService
from services.contract_service import ContractService
from services.event_service import EventService
from services.user_service import UserService
from tests.factories import build_user


def test_create_user_then_authenticate_end_to_end(db_session):
    user_repository = UserRepository(db_session)
    service = UserService(user_repository)
    admin = build_user(role=UserRole.gestion)
    db_session.add(admin)
    db_session.commit()

    service.create_user(
        admin, "new@example.com", "s3cret", "Jean", "Dupont", UserRole.commercial
    )

    authenticated = service.authenticate("new@example.com", "s3cret")

    assert authenticated is not None
    assert authenticated.email == "new@example.com"


def test_create_contract_looks_up_client_across_repositories(db_session):
    client_repository = ClientRepository(db_session)
    contract_repository = ContractRepository(db_session)
    client_service = ClientService(client_repository)
    contract_service = ContractService(contract_repository, client_repository)

    commercial = build_user(role=UserRole.commercial)
    gestion = build_user(role=UserRole.gestion)
    db_session.add_all([commercial, gestion])
    db_session.commit()

    client = client_service.create_client(
        commercial, "Marie", "Curie", "marie@example.com", "0600000000", "ACME"
    )

    contract = contract_service.create_contract(
        gestion, Decimal("1000.00"), Decimal("1000.00"), client.email
    )

    assert contract.client_id == client.id
    assert contract_repository.get_by_id(str(contract.id)) is not None


def test_create_event_requires_signed_contract_owned_by_commercial(db_session):
    client_repository = ClientRepository(db_session)
    contract_repository = ContractRepository(db_session)
    event_repository = EventRepository(db_session)
    user_repository = UserRepository(db_session)

    client_service = ClientService(client_repository)
    contract_service = ContractService(contract_repository, client_repository)
    event_service = EventService(event_repository, contract_repository, user_repository)

    commercial = build_user(role=UserRole.commercial)
    gestion = build_user(role=UserRole.gestion)
    db_session.add_all([commercial, gestion])
    db_session.commit()

    client = client_service.create_client(
        commercial, "Marie", "Curie", "marie@example.com", "0600000000", "ACME"
    )
    contract = contract_service.create_contract(
        gestion, Decimal("1000.00"), Decimal("1000.00"), client.email
    )
    contract_service.update_signed(gestion, contract, True)

    event = event_service.create_event(
        commercial,
        event_name="Soiree",
        date_start=datetime(2026, 1, 1, 20, 0),
        date_end=datetime(2026, 1, 1, 23, 0),
        location="Paris",
        attendees=50,
        notes=None,
        contract_id=str(contract.id),
    )

    assert event is not None
    assert event_repository.get_by_id(str(event.id)) is not None


def test_create_event_rejected_when_contract_not_signed(db_session):
    client_repository = ClientRepository(db_session)
    contract_repository = ContractRepository(db_session)
    event_repository = EventRepository(db_session)
    user_repository = UserRepository(db_session)

    client_service = ClientService(client_repository)
    contract_service = ContractService(contract_repository, client_repository)
    event_service = EventService(event_repository, contract_repository, user_repository)

    commercial = build_user(role=UserRole.commercial)
    gestion = build_user(role=UserRole.gestion)
    db_session.add_all([commercial, gestion])
    db_session.commit()

    client = client_service.create_client(
        commercial, "Marie", "Curie", "marie@example.com", "0600000000", "ACME"
    )
    contract = contract_service.create_contract(
        gestion, Decimal("1000.00"), Decimal("1000.00"), client.email
    )

    event = event_service.create_event(
        commercial,
        event_name="Soiree",
        date_start=datetime(2026, 1, 1, 20, 0),
        date_end=datetime(2026, 1, 1, 23, 0),
        location="Paris",
        attendees=50,
        notes=None,
        contract_id=str(contract.id),
    )

    assert event is None
    assert event_repository.event_list() == []
