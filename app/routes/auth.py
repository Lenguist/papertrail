# app/routes/auth.py

from flask import Blueprint, redirect, request, session, current_app, url_for
import urllib.parse
import os
from app.extensions import supabase

print(f"[DEBUG] auth.py imported. supabase object at import: {supabase}")

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login")
def login():
    """Redirects user to Supabase-hosted Google OAuth page."""
    from app.extensions import supabase as sb  # fresh lookup
    print(f"[DEBUG] /login accessed. Supabase client now: {sb}")

    if sb is None:
        current_app.logger.error("Supabase client not initialized")
        print("[DEBUG] ❌ Supabase client still None in /login")
        return "Internal configuration error: Supabase not initialized", 500

    redirect_uri = request.url_root.rstrip("/") + url_for("auth_bp.callback")
    params = {
        "provider": "google",
        "redirect_to": redirect_uri,
        "flow_type": "pkce",
        "response_type": "code",
    }

    query = urllib.parse.urlencode(params)
    auth_url = f"{os.getenv('SUPABASE_URL')}/auth/v1/authorize?{query}"

    print(f"[DEBUG] Redirecting user to: {auth_url}")
    return redirect(auth_url)


@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    print(f"[DEBUG] /callback hit. Code param: {code}")

    from app.extensions import supabase as sb
    print(f"[DEBUG] Supabase in callback: {sb}")

    if sb is None:
        print("[DEBUG] ❌ Supabase client still None in /callback")
        return "Internal configuration error: Supabase not initialized", 500

    if not code:
        current_app.logger.error("❌ Missing OAuth code")
        return "Missing OAuth code", 400

    try:
        res = sb.auth.exchange_code_for_session({"code": code})
        user = res.user
        print(f"[DEBUG] Supabase exchange_code_for_session() returned user: {user}")

        if not user:
            current_app.logger.error("❌ No user returned from Supabase")
            return "Authentication failed", 400

        session["user"] = {
            "id": user.id,
            "email": user.email,
            "name": getattr(user, "user_metadata", {}).get("full_name", ""),
            "avatar_url": getattr(user, "user_metadata", {}).get("avatar_url", ""),
        }

        current_app.logger.info(f"✅ Login successful for {user.email}")
        print(f"[DEBUG] ✅ Stored user session: {session['user']}")
        return redirect("/library")

    except Exception as e:
        current_app.logger.error(f"Auth callback failed: {e}")
        print(f"[DEBUG] ❌ Auth callback failed with error: {e}")
        return f"Authentication error: {e}", 500


@auth_bp.route("/logout")
def logout():
    session.clear()
    print("[DEBUG] Session cleared, user logged out.")
    return redirect("/")
