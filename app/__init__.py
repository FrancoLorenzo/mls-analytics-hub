from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)

    # Register the main blueprint
    app.register_blueprint(main)

    return app