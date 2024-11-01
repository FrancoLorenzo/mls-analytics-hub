from flask import Flask
from .routes import main
import os

def create_app():
    app = Flask(__name__)

    # Set a secret key for session management
    app.secret_key = os.urandom(24)  # Generates a random 24-byte key

    # Register the main blueprint
    app.register_blueprint(main)

    return app
