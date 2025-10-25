from flask import Blueprint, request, redirect, url_for, flash
from ..extensions import db
from ..models.user import User
from ..models.paper import Paper
from ..models.user_paper import UserPaper

library_bp = Blueprint("library", __name__)

# For MVP, assume a single logged-in user (mock)
CURRENT_USER_ID = "00000000-0000-0000-0000-000000000001"


@library_bp.route("/add", methods=["POST"])
def add_to_library():
    title = request.form.get("title")
    authors = request.form.get("authors")
    doi = request.form.get("doi")
    url = request.form.get("url")

    # 1. Ensure paper exists in DB
    paper = Paper.query.filter_by(doi=doi).first()
    if not paper:
        paper = Paper(title=title, authors=authors, doi=doi, url=url, source="openalex")
        db.session.add(paper)
        db.session.commit()

    # 2. Link paper to user library
    existing = UserPaper.query.filter_by(user_id=CURRENT_USER_ID, paper_id=paper.id).first()
    if not existing:
        user_paper = UserPaper(user_id=CURRENT_USER_ID, paper_id=paper.id)
        db.session.add(user_paper)
        db.session.commit()
        flash("Added to library!", "success")
    else:
        flash("Already in your library.", "info")

    return redirect(url_for("main.index"))
