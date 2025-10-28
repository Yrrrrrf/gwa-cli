from gwa._core import hello_from_bin




def main() -> None:
    print(hello_from_bin())

# * Export fn's
def export_version() -> str:
    from importlib.metadata import version
    global __version__
    __version__ = version("gwa")
    return __version__

# * Export callouts
export_version()
# export_some_other_callout()