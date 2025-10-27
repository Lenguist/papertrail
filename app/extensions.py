# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from supabase import create_client
import os

db = SQLAlchemy()
supabase = None  # Global reference


def init_supabase(app=None):
    """
    Initialize the Supabase client using environment variables.
    Attaches client to the Flask app instance.
    """
    global supabase
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    print("[DEBUG] init_supabase() called")
    print(f"[DEBUG] Existing supabase global: {supabase}")
    print(f"[DEBUG] SUPABASE_URL={url}")
    print(f"[DEBUG] SUPABASE_KEY set? {'yes' if key else 'no'}")

    if not url or not key:
        raise RuntimeError("❌ Missing SUPABASE_URL or SUPABASE_KEY in environment variables.")

    try:
        supabase = create_client(url, key)
        print(f"[DEBUG] Supabase client created: {supabase}")

        if app:
            app.supabase = supabase
            app.logger.info(f"✅ Supabase client attached to app: {url.split('//')[-1]}")
            print("[DEBUG] Supabase attached to app instance.")
        else:
            print("[DEBUG] init_supabase() called without app context")

    except Exception as e:
        if app:
            app.logger.error(f"❌ Failed to initialize Supabase: {e}")
        print(f"[DEBUG] ERROR in init_supabase: {e}")
        raise
