import click

from cli.context import build_context
from cli.auth import auth
from cli.client import client
from cli.contract import contract
from cli.event import event
from cli.user import user


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    """Epic Events CRM - gestion des clients, contrats et evenements."""
    ctx.obj = build_context()


@cli.result_callback()
@click.pass_context
def _close_session(ctx, result, **kwargs):
    ctx.obj.db_session.close()


cli.add_command(auth)
cli.add_command(client)
cli.add_command(contract)
cli.add_command(event)
cli.add_command(user)
