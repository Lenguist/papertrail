from flask import Flask
from .extensions import db
from .config import Config

# Blueprints
from .routes.main import main_bp
from .routes.library import library_bp
from .routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(library_bp, url_prefix="/library")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/ping")
    def ping():
        return {"status": "ok"}

    return app
