import pyodbc
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config

def get_db_connection():
    conn_str = (
        f"DRIVER={Config.DB_DRIVER};"
        f"SERVER={Config.DB_SERVER};"
        f"PORT={Config.DB_PORT};"  # Add port for MySQL
        f"DATABASE={Config.DB_NAME};"
        f"UID={Config.DB_USERNAME};"
        f"PWD={Config.DB_PASSWORD};"
    )

    try:
        connection = pyodbc.connect(conn_str)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


def delete_club(club_id):
    connection = get_db_connection()
    if not connection:
        print("Database connection failed.")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Club WHERE club_id = ?", (club_id,))
            connection.commit()
            print(f"Club with ID {club_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting club: {e}")
    finally:
        connection.close()






