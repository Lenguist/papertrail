from flask import Blueprint, render_template, request
from ..services.openalex import search_papers

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    query = None
    results = []

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            results = search_papers(query)

    return render_template("index.html", query=query, results=results)
