"""CLI application for GWA - A hybrid project generator."""

from typer import Typer
from rich.console import Console

app: Typer = Typer(
    name="gwa",
    help="A lightning-fast scaffolder for General Web App (GWA) projects.",
    no_args_is_help=True,
    add_completion=False,
)

console = Console()


def register_commands():
    """Register all CLI commands and options with the app."""
    print("Registering commands...")
    from gwa.cli.commands import register_commands
    from gwa.cli.options import register_callbacks

    # * Register all commands and options with the app
    register_commands(app)
    register_callbacks(app)
