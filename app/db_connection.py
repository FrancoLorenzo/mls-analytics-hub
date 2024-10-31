import pyodbc
from config import Config

def get_db_connection():
    conn_str = (
        f"DRIVER={{{Config.DB_DRIVER}}};"
        f"SERVER={Config.DB_SERVER};"
        f"PORT={Config.DB_PORT};"  # Make sure this is set to 3306 for MySQL
        f"DATABASE={Config.DB_NAME};"
        f"UID={Config.DB_USERNAME};"
        f"PWD={Config.DB_PASSWORD};"
        "OPTION=3;"  # Specific to MySQL ODBC driver to handle connections
    )
    try:
        connection = pyodbc.connect(conn_str)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
