from flask import Flask
from config import Config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Import and register blueprints
    from auth import auth_bp
    # from chat import chat_bp  # optional if you have it

    app.register_blueprint(auth_bp)

    # If chat exists:
    # app.register_blueprint(chat_bp)

    return app
