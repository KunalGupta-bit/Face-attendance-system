from flask import Blueprint
from controllers.attendace_controller import get_attendance_report, mark_attendance, get_lecture_attendance, get_my_attendance
from flask_jwt_extended import jwt_required

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/mark", methods=["POST"])
def mark():
    return mark_attendance()

@attendance_bp.route("/report", methods=["GET"])
def get_report():
    return get_attendance_report()

@attendance_bp.route("/lecture/<lecture_id>", methods=["GET"])
def lecture_attendance(lecture_id):
    return get_lecture_attendance(lecture_id)

@attendance_bp.route("/my", methods=["GET"])
@jwt_required()
def my_attendance():
    return get_my_attendance()