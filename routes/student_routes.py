from flask import Blueprint
from controllers.student_controller import register_student, update_student_embedding

student_bp = Blueprint("student", __name__)

@student_bp.route("/register", methods=["POST"])
def register():
    return register_student()

@student_bp.route("/update", methods=["POST"])
def update():
    return update_student_embedding()