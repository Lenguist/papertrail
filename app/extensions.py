# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from supabase import create_client
import os

db = SQLAlchemy()
supabase = None  # Global reference for compatibility


def init_supabase(app=None):
    """
    Initialize the Supabase client using environment variables.
    Attaches client to the Flask app instance.
    """
    global supabase
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError("❌ Missing SUPABASE_URL or SUPABASE_KEY in environment variables.")

    try:
        supabase = create_client(url, key)
        if app:
            app.supabase = supabase  # make available via app.supabase
            app.logger.info(f"✅ Supabase client initialized for project {url.split('//')[-1]}")
        else:
            print(f"✅ Supabase client initialized for project {url.split('//')[-1]}")
    except Exception as e:
        if app:
            app.logger.error(f"❌ Failed to initialize Supabase: {e}")
        raise
