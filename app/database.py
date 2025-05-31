import oracledb

def get_conexion():
    conexion = oracledb.connect(
        user="db",
        password="db",
        dsn="localhost:1521/orcl"
    )
    return conexion