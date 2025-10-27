# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from supabase import create_client
import os

db = SQLAlchemy()
supabase = None


def init_supabase(app):
    """
    Initialize the Supabase client using environment variables.
    Logs a warning if credentials are missing.
    """
    global supabase
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        app.logger.warning("❌ Missing SUPABASE_URL or SUPABASE_KEY in environment.")
        return

    try:
        supabase = create_client(url, key)
        app.logger.info(f"✅ Connected to Supabase at {url}")
    except Exception as e:
        app.logger.error(f"Failed to initialize Supabase: {e}")
        raise
