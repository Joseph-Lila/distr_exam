import pathlib

THIS_DIR = pathlib.Path(__file__).parent.resolve().absolute()
ROOT_DIR = THIS_DIR.parent


def get_sqlite_connection_str():
    """
    Returns path to sqlite database.
    :return: str
    """
    db_path = THIS_DIR / 'assets' / 'databases' / 'sqlite.db'
    return str(db_path)
