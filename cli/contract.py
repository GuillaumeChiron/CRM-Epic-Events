import click
from rich.prompt import Confirm, Prompt

from cli.context import AppContext, deny_if_false, require_login, resolve_or_exit
from views.contract_view import ContractView

view = ContractView()

FIELD_HANDLERS = {
    "montant-total": ("update_total_amount", "update_total_amount"),
    "montant-restant": ("update_remaining_amount", "update_remaining_amount"),
    "signe": ("update_signed", "update_signed"),
}


@click.group()
def contract():
    """Gestion des contrats."""


@contract.command("create")
@click.pass_context
def create(ctx: click.Context):
    """Creer un contrat pour un client existant (equipe de gestion)."""
    app_ctx = require_login(ctx)
    total_amount, remaining_amount, client_email = view.create_contract()

    created = app_ctx.contract_service.create_contract(
        app_ctx.current_user, total_amount, remaining_amount, client_email
    )

    if created is False:
        app_ctx.console.print("[bold red]Acces refuse.[/bold red]")
        raise click.exceptions.Exit(1)
    if created is None:
        app_ctx.console.print(f"[bold red]Client introuvable : {client_email}[/bold red]")
        raise click.exceptions.Exit(1)

    app_ctx.console.print("[bold green]Contrat cree.[/bold green]")
    view.display_contract(created)


@contract.command("list")
@click.option("--unsigned", is_flag=True, help="N'afficher que les contrats non signes.")
@click.option("--unpaid", is_flag=True, help="N'afficher que les contrats non entierement payes.")
@click.pass_context
def list_(ctx: click.Context, unsigned: bool, unpaid: bool):
    """Lister les contrats, avec filtres optionnels."""
    app_ctx = require_login(ctx)

    if unsigned:
        contracts = app_ctx.contract_service.list_unsigned_contracts()
    elif unpaid:
        contracts = app_ctx.contract_service.list_contracts_with_remaining_amount()
    else:
        contracts = app_ctx.contract_service.list_contracts()

    view.display_contracts_list(contracts)


@contract.command("update")
@click.argument("contract_id")
@click.pass_context
def update(ctx: click.Context, contract_id: str):
    """Mettre a jour un contrat (gestion, ou commercial responsable du client)."""
    app_ctx = require_login(ctx)
    target = resolve_or_exit(app_ctx, app_ctx.contract_repository, contract_id, "Contrat")

    while True:
        field = Prompt.ask("Champ a modifier", choices=list(FIELD_HANDLERS.keys()))
        view_method_name, service_method_name = FIELD_HANDLERS[field]
        new_value = getattr(view, view_method_name)()

        updated = deny_if_false(
            app_ctx,
            getattr(app_ctx.contract_service, service_method_name)(
                app_ctx.current_user, target, new_value
            ),
        )
        view.display_contract(updated)

        if not Confirm.ask("Modifier un autre champ ?", choices=["o", "n"], default=False):
            break
