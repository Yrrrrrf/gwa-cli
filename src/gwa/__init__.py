from gwa._core import hello_from_bin
from gwa._core import init

from gwa.cli import app
from gwa.tui import run_tui


def main() -> None:
    """Main entry point for the GWA CLI."""
    init()

    # Register all commands and options before running the app
    from gwa.cli import register_commands

    register_commands()

    app()  # run cli app


if __name__ == "__main__":
    main()


# * Export fn's
def export_version():
    def rust_version():
        global __version_crates__
        __version_crates__ = "todo: get from rust"
        return __version_crates__

    def python_version():
        from importlib.metadata import version

        global __version_pypi__
        __version_pypi__ = version("gwa")
        return __version_pypi__

    rust_version()
    python_version()


# * Export callouts
export_version()
# export_some_other_callout()
