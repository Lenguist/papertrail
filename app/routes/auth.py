# app/routes/auth.py

from flask import Blueprint, redirect, request, session, current_app
import urllib.parse
from app.extensions import supabase

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login")
def login():
    # ✅ Ensure Supabase client is initialized
    from app.extensions import supabase as sb
    if sb is None:
        current_app.logger.error("Supabase client not initialized")
        return "Internal configuration error: Supabase not initialized", 500

    # Build Google OAuth URL
    redirect_uri = request.url_root.rstrip("/") + "/auth/callback"
    params = {
        "provider": "google",
        "redirect_to": redirect_uri,
    }
    query = urllib.parse.urlencode(params)

    auth_url = f"{sb.supabase_url}/auth/v1/authorize?{query}"
    current_app.logger.info(f"Redirecting to: {auth_url}")
    return redirect(auth_url)


@auth_bp.route("/callback")
def callback():
    """Handle Supabase OAuth redirect after Google sign-in."""
    code = request.args.get("code")
    if not code:
        return "Missing OAuth code", 400

    from app.extensions import supabase as sb
    if sb is None:
        current_app.logger.error("Supabase client not initialized")
        return "Internal configuration error: Supabase not initialized", 500

    # Exchange code for session
    res = sb.auth.exchange_code_for_session({"code": code})
    session["user"] = res.user.__dict__
    current_app.logger.info(f"✅ User logged in: {res.user.email}")

    return redirect("/library")
