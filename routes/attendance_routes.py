from flask import Blueprint
from controllers.attendace_controller import mark_attendance

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/mark", methods=["POST"])
def mark():
    return mark_attendance()