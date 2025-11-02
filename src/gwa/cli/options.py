from typing import Optional

import typer

from gwa.cli import console


def register_callbacks(app: typer.Typer):
    """Register all global options with the Typer app."""
    app.callback()(version)


def version(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version of GWA CLI.",
        is_eager=True,
    ),
):
    """GWA CLI - A hybrid project generator."""
    if version:
        try:
            from importlib.metadata import version as get_version

            pkg_version = get_version("gwa")
        except:
            pkg_version = "0.1.0"

        console.print(f"[bold]GWA CLI v{pkg_version}[/bold]")
        console.print(
            "A hybrid project generator using Rust for performance and Python for UI"
        )
        raise typer.Exit()
