from flask import Flask
from extensions import *   # if you use db/login manager etc

def create_app():
    app = Flask(__name__)

    # Load config
    from config import Config
    app.config.from_object(Config)

    # Initialize extensions (if any)
    # db.init_app(app)
    # login_manager.init_app(app)

    # Register routes (IMPORTANT)
    from auth import *
    from chat import *

    return app