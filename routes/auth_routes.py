from flask import Blueprint
from controllers.auth_controller import register, login, get_current_user, logout
from flask_jwt_extended import jwt_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def auth_register():
    """Register a new user"""
    return register()

@auth_bp.route("/login", methods=["POST"])
def auth_login():
    """Login user and get JWT token"""
    return login()

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def auth_me():
    """Get current user info (requires valid JWT token)"""
    return get_current_user()

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def auth_logout():
    """Logout user"""
    return logout()
