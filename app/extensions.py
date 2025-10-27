from flask_sqlalchemy import SQLAlchemy
from supabase import create_client
import os

db = SQLAlchemy()  # ← restore this line
supabase = None

def init_supabase(app=None):
    global supabase
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY.")

    supabase = create_client(url, key)
    if app:
        app.supabase = supabase
