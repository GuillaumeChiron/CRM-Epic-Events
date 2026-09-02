import click
from rich.prompt import Confirm, Prompt

from cli.context import deny_if_false, require_login, resolve_or_exit
from views.client_view import ClientView

view = ClientView()

FIELD_HANDLERS = {
    "prenom": ("update_first_name", "update_first_name"),
    "nom": ("update_last_name", "update_last_name"),
    "email": ("update_email", "update_email"),
    "telephone": ("update_phone", "update_phone"),
    "entreprise": ("update_company", "update_company"),
    "dernier-contact": ("update_last_contact_at", "update_last_contact_at"),
}


@click.group()
def client():
    """Gestion des clients."""


@client.command("create")
@click.pass_context
def create(ctx: click.Context):
    """Creer un client (associe automatiquement au commercial connecte)."""
    app_ctx = require_login(ctx)
    first_name, last_name, email, phone, company = view.create_client()

    created = deny_if_false(
        app_ctx,
        app_ctx.client_service.create_client(
            app_ctx.current_user, first_name, last_name, email, phone, company
        ),
    )
    app_ctx.console.print("[bold green]Client cree.[/bold green]")
    view.display_client(created)


@client.command("list")
@click.pass_context
def list_(ctx: click.Context):
    """Lister tous les clients."""
    app_ctx = require_login(ctx)
    view.display_clients_list(app_ctx.client_service.list_clients())


@client.command("update")
@click.argument("email")
@click.pass_context
def update(ctx: click.Context, email: str):
    """Mettre a jour un client (uniquement le commercial qui en est responsable)."""
    app_ctx = require_login(ctx)
    target = resolve_or_exit(
        app_ctx, app_ctx.client_repository, email, "Client", lookup="email"
    )

    while True:
        field = Prompt.ask("Champ a modifier", choices=list(FIELD_HANDLERS.keys()))
        view_method_name, service_method_name = FIELD_HANDLERS[field]
        new_value = getattr(view, view_method_name)()

        updated = deny_if_false(
            app_ctx,
            getattr(app_ctx.client_service, service_method_name)(
                app_ctx.current_user, target, new_value
            ),
        )
        view.display_client(updated)

        if not Confirm.ask("Modifier un autre champ ?", choices=["o", "n"], default=False):
            break
