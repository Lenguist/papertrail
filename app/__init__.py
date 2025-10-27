# app/__init__.py

import os
from flask import Flask
from dotenv import load_dotenv

print("[DEBUG] Importing app.__init__")

# Load environment variables
load_dotenv()

from .extensions import db, init_supabase
from .config import Config

# Blueprints (importing these may cause early supabase references)
print("[DEBUG] Importing Blueprints...")
from .routes.main import main_bp
from .routes.library import library_bp
from .routes.auth import auth_bp
print("[DEBUG] Blueprints imported successfully.")


def create_app():
    """Flask application factory."""
    print("[DEBUG] create_app() starting...")
    app = Flask(__name__)
    app.config.from_object(Config)

    db_url = os.getenv("DATABASE_URL")
    print(f"[DEBUG] DATABASE_URL present? {'yes' if db_url else 'no'}")

    # Initialize extensions
    db.init_app(app)
    print("[DEBUG] DB initialized.")

    init_supabase(app)
    print("[DEBUG] Supabase init called inside create_app()")

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(library_bp, url_prefix="/library")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    print("[DEBUG] Blueprints registered.")

    @app.route("/ping")
    def ping():
        return {"status": "ok"}

    print("[DEBUG] create_app() done.")
    return app
