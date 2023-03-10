import pathlib

THIS_DIR = pathlib.Path(__file__).parent.resolve().absolute()
ROOT_DIR = THIS_DIR.parent


def get_sqlite_connection_str():
    """
    Returns path to sqlite database.
    :return: str
    """
    db_path = ROOT_DIR / 'assets' / 'databases' / 'sqlite_Source.db'
    return str(db_path)


def get_additional_sqlite_connection_str():
    db_path = ROOT_DIR / 'assets' / 'databases' / 'sqlite_additional_Source.db'
    return str(db_path)


def get_tcp_ip_credits():
    return '192.168.56.101', 5000


def get_encoding():
    return 'utf8'
