from flask import Blueprint
from controllers.attendace_controller import get_attendance_report, mark_attendance

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/mark", methods=["POST"])
def mark():
    return mark_attendance()

@attendance_bp.route("/report", methods=["GET"])
def get_report():
    return get_attendance_report()