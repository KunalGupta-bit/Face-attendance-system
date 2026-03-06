from flask import Blueprint
from controllers.student_controller import register_student, update_student_embedding, bulk_register_students, get_all_students

student_bp = Blueprint("student", __name__)

@student_bp.route("/register", methods=["POST"])
def register():
    return register_student()

@student_bp.route("/update", methods=["POST"])
def update():
    return update_student_embedding()

@student_bp.route("/bulk-register", methods=["POST"])
def bulk_register():
    return bulk_register_students()

# Added this route for the Student List view
@student_bp.route("/all", methods=["GET"])
def get_students():
    return get_all_students()