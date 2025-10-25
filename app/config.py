import os

class Config:
    # Flask basics
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")

    # Supabase Postgres connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # External APIs
    OPENALEX_BASE_URL = "https://api.openalex.org/works"

    # Supabase optional auth / storage
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
