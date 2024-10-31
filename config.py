import os

class Config:
    DB_DRIVER = 'MySQL ODBC 9.1 Unicode Driver'  # Exact driver name as shown in ODBC Data Sources
    DB_SERVER = '127.0.0.1'  # Or your MySQL server address
    DB_PORT = '3306'  # Ensure this matches your MySQL port
    DB_NAME = 'mls_analytics_hub_db'  # Replace with your database name
    DB_USERNAME = 'root'  # Replace with your MySQL username
    DB_PASSWORD = 'Flo13051991!'  # Replace with your MySQL password