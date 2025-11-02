# rust module imports
from gwa._core import hello_from_bin
from gwa._core import init
# python module imports
from gwa.cli import app
from gwa.tui import run_tui


def main() -> None:
    """Main entry point for the GWA CLI."""
    # fix this later!!!
    # todo: This fn can't be inside because it will cause an error if the Rust module is not built
    # todo: So, this script must be run... Sometime later, find a better way to handle this
    # init()

    from gwa.cli import init_cli
    init_cli()

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
