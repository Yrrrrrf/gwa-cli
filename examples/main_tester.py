from gwa import init
from gwa import __version_crates__, __version_pypi__


def main():
    init()
    print(f"gwa crate version: {__version_crates__}")
    print(f"gwa pypi version: {__version_pypi__}")


if __name__ == "__main__":
    main()
