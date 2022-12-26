import pathlib

THIS_DIR = pathlib.Path(__file__).parent.resolve().absolute()
ROOT_DIR = THIS_DIR.parent


def get_sqlite_connection_str():
    """
    Returns path to sqlite database.
    :return: str
    """
    db_path = THIS_DIR / 'assets' / 'databases' / 'sqlite_Source.db'
    return str(db_path)


def get_csv_tables_names():
    """
    Returns paths of csv files.
    :return: Dict[str, str]
    """
    db_path = THIS_DIR / 'assets' / 'databases' / 'csv'
    names = ['cats.csv']
    return {name[:name.find('.')]: str(db_path / name) for name in names}


def get_csv_headers():
    return {'cats': ('item_id', 'nick')}


def get_tcp_ip_credits():
    return "localhost", 6678
