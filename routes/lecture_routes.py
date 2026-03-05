from flask import Blueprint
from controllers.lecture_controller import create_lecture

lecture_bp = Blueprint("lecture", __name__)

@lecture_bp.route("/create", methods=["POST"])
def create():
    return create_lecture()