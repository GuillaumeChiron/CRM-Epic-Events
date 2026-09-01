import click
from rich.prompt import Confirm, Prompt

from cli.context import AppContext, deny_if_false, require_login, resolve_or_exit
from views.user_view import UserView

view = UserView()

FIELD_HANDLERS = {
    "email": ("update_email", "update_email"),
    "mot-de-passe": ("update_password", "update_password"),
    "prenom": ("update_first_name", "update_first_name"),
    "nom": ("update_last_name", "update_last_name"),
    "role": ("update_role", "update_role"),
}


@click.group()
def user():
    """Gestion des collaborateurs."""


@user.command("create")
@click.pass_context
def create(ctx: click.Context):
    """Creer un collaborateur (equipe de gestion)."""
    app_ctx = require_login(ctx)
    email, password, first_name, last_name, role = view.create_user()

    created = deny_if_false(
        app_ctx,
        app_ctx.user_service.create_user(
            app_ctx.current_user, email, password, first_name, last_name, role
        ),
    )
    app_ctx.console.print("[bold green]Collaborateur cree.[/bold green]")
    view.display_user(created)


@user.command("list")
@click.pass_context
def list_(ctx: click.Context):
    """Lister tous les collaborateurs."""
    app_ctx = require_login(ctx)
    view.display_users_list(app_ctx.user_service.list_users())


@user.command("update")
@click.argument("email")
@click.pass_context
def update(ctx: click.Context, email: str):
    """Mettre a jour un collaborateur (equipe de gestion)."""
    app_ctx = require_login(ctx)
    target = resolve_or_exit(
        app_ctx, app_ctx.user_repository, email, "Collaborateur", lookup="email"
    )

    while True:
        field = Prompt.ask("Champ a modifier", choices=list(FIELD_HANDLERS.keys()))
        view_method_name, service_method_name = FIELD_HANDLERS[field]
        new_value = getattr(view, view_method_name)()

        updated = deny_if_false(
            app_ctx,
            getattr(app_ctx.user_service, service_method_name)(
                app_ctx.current_user, target, new_value
            ),
        )
        view.display_user(updated)

        if not Confirm.ask("Modifier un autre champ ?", choices=["o", "n"], default=False):
            break


@user.command("delete")
@click.argument("email")
@click.pass_context
def delete(ctx: click.Context, email: str):
    """Supprimer un collaborateur (equipe de gestion)."""
    app_ctx = require_login(ctx)
    target = resolve_or_exit(
        app_ctx, app_ctx.user_repository, email, "Collaborateur", lookup="email"
    )

    if not Confirm.ask(
        f"Confirmer la suppression de {target.first_name} {target.last_name} ?",
        choices=["o", "n"],
        default=False,
    ):
        app_ctx.console.print("Annule.")
        return

    deny_if_false(app_ctx, app_ctx.user_service.delete_user(app_ctx.current_user, target))
    app_ctx.console.print("[bold green]Collaborateur supprime.[/bold green]")
