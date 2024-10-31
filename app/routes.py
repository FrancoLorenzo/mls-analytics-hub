from flask import current_app as app
from .db_connection import get_db_connection

@app.route('/test-db-connection')
def test_db_connection():
    connection = get_db_connection()
    if connection:
        return "Database connection successful!"
    else:
        return "Failed to connect to the database."

