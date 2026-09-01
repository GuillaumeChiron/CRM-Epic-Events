import click

from cli import session
from cli.context import AppContext, require_login
from views.user_view import UserView

view = UserView()


@click.group()
def auth():
    """Connexion / deconnexion de la CLI."""


@auth.command("login")
@click.pass_context
def login(ctx: click.Context):
    """Se connecter et ouvrir une session locale."""
    app_ctx: AppContext = ctx.obj
    email, password = view.login()

    user = app_ctx.user_service.authenticate(email, password)
    if user is None:
        app_ctx.console.print("[bold red]Authentification echouee.[/bold red]")
        raise click.exceptions.Exit(1)

    session.create_session(user)
    app_ctx.console.print(
        f"[bold green]Connecte en tant que[/bold green] {user.first_name} {user.last_name} "
        f"({user.role.name})"
    )


@auth.command("logout")
@click.pass_context
def logout(ctx: click.Context):
    """Fermer la session locale."""
    app_ctx: AppContext = ctx.obj
    session.clear_session()
    app_ctx.console.print("[bold green]Deconnecte.[/bold green]")


@auth.command("whoami")
@click.pass_context
def whoami(ctx: click.Context):
    """Afficher l'utilisateur actuellement connecte."""
    app_ctx = require_login(ctx)
    view.display_user(app_ctx.current_user)
