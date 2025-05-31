import oracledb
from contextlib import contextmanager

@contextmanager
def oracle_connection():
    conn = None
    try:
        conn = oracledb.connect(
            user='db',
            password='db',
            dsn='localhost:1521/orcl'
        )
        yield conn
    finally:
        if conn:
            conn.close()