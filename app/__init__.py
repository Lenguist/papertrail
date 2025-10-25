import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env at project root
load_dotenv()

from .extensions import db
from .config import Config

# Blueprints
from .routes.main import main_bp
from .routes.library import library_bp
from .routes.auth import auth_bp


def create_app():
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Verify environment variable loaded correctly (optional)
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL not found. Make sure .env is loaded correctly.")
    else:
        print(f"Connected using DATABASE_URL: {db_url.split('@')[-1]}")

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(library_bp, url_prefix="/library")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/ping")
    def ping():
        return {"status": "ok"}

    return app
