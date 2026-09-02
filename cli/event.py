import click
from rich.prompt import Confirm, Prompt

from cli.context import deny_if_false, require_login, resolve_or_exit
from views.event_view import EventView

view = EventView()

FIELD_HANDLERS = {
    "nom": ("update_event_name", "update_event_name"),
    "debut": ("update_date_start", "update_date_start"),
    "fin": ("update_date_end", "update_date_end"),
    "lieu": ("update_location", "update_location"),
    "participants": ("update_attendees", "update_attendees"),
    "notes": ("update_notes", "update_notes"),
}


@click.group()
def event():
    """Gestion des evenements."""


@event.command("create")
@click.pass_context
def create(ctx: click.Context):
    """Creer un evenement pour un contrat signe de son propre client (commercial)."""
    app_ctx = require_login(ctx)
    event_name, contract_id, date_start, date_end, location, attendees, notes = (
        view.create_event()
    )

    created = app_ctx.event_service.create_event(
        app_ctx.current_user,
        event_name,
        date_start,
        date_end,
        location,
        attendees,
        notes,
        contract_id,
    )

    if created is False:
        app_ctx.console.print("[bold red]Acces refuse.[/bold red]")
        raise click.exceptions.Exit(1)
    if created is None:
        app_ctx.console.print(
            "[bold red]Contrat introuvable, non signe, ou non associe a ce commercial.[/bold red]"
        )
        raise click.exceptions.Exit(1)

    app_ctx.console.print("[bold green]Evenement cree.[/bold green]")
    view.display_event(created)


@event.command("list")
@click.option("--no-support", is_flag=True, help="N'afficher que les evenements sans support.")
@click.option(
    "--mine", is_flag=True, help="N'afficher que les evenements dont je suis responsable."
)
@click.pass_context
def list_(ctx: click.Context, no_support: bool, mine: bool):
    """Lister les evenements, avec filtres optionnels."""
    app_ctx = require_login(ctx)

    if no_support:
        events = app_ctx.event_service.list_events_without_support()
    elif mine:
        events = app_ctx.event_service.list_my_events(app_ctx.current_user)
    else:
        events = app_ctx.event_service.list_events()

    view.display_events_list(events)


@event.command("show")
@click.argument("event_id")
@click.pass_context
def show(ctx: click.Context, event_id: str):
    """Afficher le detail d'un evenement."""
    app_ctx = require_login(ctx)
    target = resolve_or_exit(app_ctx, app_ctx.event_repository, event_id, "Evenement")
    view.display_event(target)


@event.command("update")
@click.argument("event_id")
@click.pass_context
def update(ctx: click.Context, event_id: str):
    """Mettre a jour un evenement (uniquement le support qui en est responsable)."""
    app_ctx = require_login(ctx)
    target = resolve_or_exit(app_ctx, app_ctx.event_repository, event_id, "Evenement")

    while True:
        field = Prompt.ask("Champ a modifier", choices=list(FIELD_HANDLERS.keys()))
        view_method_name, service_method_name = FIELD_HANDLERS[field]
        new_value = getattr(view, view_method_name)()

        updated = deny_if_false(
            app_ctx,
            getattr(app_ctx.event_service, service_method_name)(
                app_ctx.current_user, target, new_value
            ),
        )
        view.display_event(updated)

        if not Confirm.ask("Modifier un autre champ ?", choices=["o", "n"], default=False):
            break


@event.command("assign-support")
@click.argument("event_id")
@click.pass_context
def assign_support(ctx: click.Context, event_id: str):
    """Associer un collaborateur support a un evenement (equipe de gestion)."""
    app_ctx = require_login(ctx)
    target = resolve_or_exit(app_ctx, app_ctx.event_repository, event_id, "Evenement")
    support_email = view.prompt_support_email()

    updated = app_ctx.event_service.assign_support(app_ctx.current_user, target, support_email)

    if updated is False:
        app_ctx.console.print("[bold red]Acces refuse.[/bold red]")
        raise click.exceptions.Exit(1)
    if updated is None:
        app_ctx.console.print(f"[bold red]Collaborateur introuvable : {support_email}[/bold red]")
        raise click.exceptions.Exit(1)

    app_ctx.console.print("[bold green]Support assigne.[/bold green]")
    view.display_event(updated)
