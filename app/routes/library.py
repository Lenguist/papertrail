# app/routes/library.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.paper import Paper
from app.models.user import User
from app.models.user_paper import UserPaper
from app.services.openalex import search_papers

library_bp = Blueprint("library_bp", __name__)


@library_bp.route("/", methods=["GET", "POST"])
def library_home():
    # ✅ Require user login
    if "user" not in session:
        return redirect(url_for("auth_bp.login"))

    user_info = session["user"]
    email = user_info.get("email")

    # Find or create local user record
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=email.split("@")[0], email=email)
        db.session.add(user)
        db.session.commit()

    if request.method == "POST":
        title = request.form.get("title")
        authors = request.form.get("authors")
        doi = request.form.get("doi")
        url = request.form.get("url")

        # Check if paper already exists
        paper = Paper.query.filter_by(doi=doi).first()
        if not paper:
            paper = Paper(title=title, authors=authors, doi=doi, url=url, source="openalex")
            db.session.add(paper)
            db.session.commit()

        # Link user to paper
        link = UserPaper.query.filter_by(user_id=user.id, paper_id=paper.id).first()
        if not link:
            user_paper = UserPaper(user_id=user.id, paper_id=paper.id)
            db.session.add(user_paper)
            db.session.commit()
            flash("Added to your library!", "success")
        else:
            flash("Already in your library.", "info")

        return redirect(url_for("library_bp.library_home"))

    # Show saved papers
    papers = (
        db.session.query(Paper)
        .join(UserPaper)
        .filter(UserPaper.user_id == user.id)
        .order_by(UserPaper.added_at.desc())
        .all()
    )

    return render_template("library.html", papers=papers)


@library_bp.route("/search")
def search():
    query = request.args.get("q")
    results = []
    if query:
        results = search_papers(query)
    return render_template("search.html", query=query, results=results)
