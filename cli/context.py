from dataclasses import dataclass

import click
from rich.console import Console

from cli import session
from database.database import SessionLocal
from models.user import User
from repositories.client_repository import ClientRepository
from repositories.contract_repository import ContractRepository
from repositories.event_repository import EventRepository
from repositories.user_repository import UserRepository
from services.client_service import ClientService
from services.contract_service import ContractService
from services.event_service import EventService
from services.user_service import UserService


@dataclass
class AppContext:
    db_session: object
    console: Console
    user_repository: UserRepository
    client_repository: ClientRepository
    contract_repository: ContractRepository
    event_repository: EventRepository
    user_service: UserService
    client_service: ClientService
    contract_service: ContractService
    event_service: EventService
    current_user: User | None


def build_context() -> AppContext:
    db_session = SessionLocal()
    console = Console()

    user_repository = UserRepository(db_session)
    client_repository = ClientRepository(db_session)
    contract_repository = ContractRepository(db_session)
    event_repository = EventRepository(db_session)

    user_id = session.read_current_user_id()
    current_user = user_repository.get_by_id(str(user_id)) if user_id else None

    return AppContext(
        db_session=db_session,
        console=console,
        user_repository=user_repository,
        client_repository=client_repository,
        contract_repository=contract_repository,
        event_repository=event_repository,
        user_service=UserService(user_repository),
        client_service=ClientService(client_repository),
        contract_service=ContractService(contract_repository, client_repository),
        event_service=EventService(event_repository, contract_repository, user_repository),
        current_user=current_user,
    )


def require_login(ctx: click.Context) -> AppContext:
    app_ctx: AppContext = ctx.obj
    if app_ctx.current_user is None:
        app_ctx.console.print(
            "[bold red]Veuillez vous connecter :[/bold red] python main.py auth login"
        )
        raise click.exceptions.Exit(1)
    return app_ctx


def resolve_or_exit(app_ctx: AppContext, repository, entity_id: str, label: str):
    try:
        entity = repository.get_by_id(entity_id)
    except ValueError:
        entity = None

    if entity is None:
        app_ctx.console.print(f"[bold red]{label} introuvable.[/bold red]")
        raise click.exceptions.Exit(1)
    return entity


def deny_if_false(app_ctx: AppContext, result):
    if result is False:
        app_ctx.console.print("[bold red]Acces refuse.[/bold red]")
        raise click.exceptions.Exit(1)
    return result
