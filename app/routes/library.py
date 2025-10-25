from flask import Blueprint, render_template

library_bp = Blueprint("library_bp", __name__)

@library_bp.route("/")
def library_home():
    return render_template("library.html")
