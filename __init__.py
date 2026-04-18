import os

from flask import Flask, redirect, render_template, url_for

from .config import Config
from .extensions import db, login_manager
from .models import User


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        instance_relative_config=True,
    )
    app.config.from_object(config_class)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.admin import admin_bp
    from .routes.auth import auth_bp
    from .routes.chat import chat_bp
    from .routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(admin_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        return redirect(url_for("main.dashboard"))

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    with app.app_context():
        db.create_all()
        _bootstrap_admin_from_env()

    return app


def _bootstrap_admin_from_env():
    from werkzeug.security import generate_password_hash

    admin_username = os.environ.get("ADMIN_USERNAME")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        return

    existing_user = User.query.filter_by(username=admin_username).first()
    if existing_user:
        if existing_user.role != "admin":
            existing_user.role = "admin"
        existing_user.password = generate_password_hash(admin_password)
        db.session.commit()
        return

    admin_user = User(
        username=admin_username,
        password=generate_password_hash(admin_password),
        role="admin",
    )
    db.session.add(admin_user)
    db.session.commit()
