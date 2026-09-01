import sys

import sentry_sdk
from rich.console import Console

from cli.main import cli
from cli.sentry import init_sentry

console = Console()

if __name__ == "__main__":
    init_sentry()
    try:
        cli()
    except Exception:
        sentry_sdk.capture_exception()
        sentry_sdk.flush(timeout=2)
        console.print(
            "[bold red]Une erreur inattendue est survenue. Elle a ete journalisee.[/bold red]"
        )
        sys.exit(1)
