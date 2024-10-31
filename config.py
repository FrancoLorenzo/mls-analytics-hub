import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    DB_DRIVER = os.getenv('DB_DRIVER')
    DB_SERVER = os.getenv('DB_SERVER')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
