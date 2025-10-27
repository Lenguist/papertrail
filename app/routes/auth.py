# app/routes/auth.py

from flask import Blueprint, redirect, request, session, current_app, url_for
import urllib.parse
import os
from app.extensions import supabase

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login")
def login():
    """Redirects user to Supabase-hosted Google OAuth page using Authorization Code (PKCE) flow."""
    if supabase is None:
        current_app.logger.error("Supabase client not initialized")
        return "Internal configuration error: Supabase not initialized", 500

    # ✅ Flask callback endpoint that will receive ?code=...
    redirect_uri = request.url_root.rstrip("/") + url_for("auth_bp.callback")

    # ✅ Force Authorization Code + PKCE flow instead of implicit
    params = {
        "provider": "google",
        "redirect_to": redirect_uri,
        "flow_type": "pkce",           # crucial: tells Supabase to return ?code=...
        "response_type": "code",       # explicitly request code flow
    }

    query = urllib.parse.urlencode(params)
    auth_url = f"{os.getenv('SUPABASE_URL')}/auth/v1/authorize?{query}"

    current_app.logger.info(f"Redirecting to Supabase Auth: {auth_url}")
    return redirect(auth_url)


@auth_bp.route("/callback")
def callback():
    """Handles redirect from Supabase after successful OAuth login."""
    code = request.args.get("code")
    if not code:
        current_app.logger.error("❌ Missing OAuth code")
        return "Missing OAuth code", 400

    if supabase is None:
        current_app.logger.error("Supabase client not initialized")
        return "Internal configuration error: Supabase not initialized", 500

    try:
        # ✅ Exchange authorization code for a session
        res = supabase.auth.exchange_code_for_session({"code": code})
        user = res.user

        if not user:
            current_app.logger.error("❌ No user returned from Supabase")
            return "Authentication failed", 400

        # ✅ Store minimal user info in session
        session["user"] = {
            "id": user.id,
            "email": user.email,
            "name": getattr(user, "user_metadata", {}).get("full_name", ""),
            "avatar_url": getattr(user, "user_metadata", {}).get("avatar_url", ""),
        }

        current_app.logger.info(f"✅ Login successful for {user.email}")
        return redirect("/library")

    except Exception as e:
        current_app.logger.error(f"Auth callback failed: {e}")
        return f"Authentication error: {e}", 500


@auth_bp.route("/logout")
def logout():
    """Clears user session."""
    session.clear()
    current_app.logger.info("User logged out")
    return redirect("/")
