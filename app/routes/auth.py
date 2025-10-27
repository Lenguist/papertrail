# app/routes/auth.py

from flask import Blueprint, redirect, request, render_template, current_app, session
import os
import urllib.parse
import secrets

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.route("/login")
def login():
    # Important: make sure redirect_to matches exactly what you put in Supabase
    redirect_uri = "http://127.0.0.1:5000/auth/callback"

    params = {
        "provider": "google",
        "redirect_to": redirect_uri,
    }

    # Build Supabase authorize URL robustly from config or env
    supabase_url = (current_app.config.get("SUPABASE_URL") or os.getenv("SUPABASE_URL") or "").rstrip("/")
    if not supabase_url:
        return "SUPABASE_URL is not configured", 500

    auth_url = f"{supabase_url}/auth/v1/authorize?{urllib.parse.urlencode(params)}"

    # Helpful debug logging
    print(f"[AUTH] authorize_url={auth_url}")

    return redirect(auth_url)

@auth_bp.route("/callback")
def callback():
    # Client-side will parse the token and redirect to login_success
    return render_template("callback.html")

@auth_bp.route("/login_success")
def login_success():
    access_token = request.args.get("access_token")
    if not access_token:
        return "Missing access token", 400

    try:
        user = current_app.supabase.auth.get_user(access_token)
        return f"Hello, {user.user.email}"
    except Exception as e:
        return f"Failed to get user info: {e}", 500
