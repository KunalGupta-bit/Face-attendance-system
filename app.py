from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp
from routes.lecture_routes import lecture_bp
from routes.auth_routes import auth_bp

app = Flask(__name__, template_folder="templates")

# JWT Configuration
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
app.config["JWT_ALGORITHM"] = "HS256"
jwt = JWTManager(app)

# CORS allows your browser to communicate with this Flask server
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Registering Blueprints for API
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(student_bp, url_prefix="/api/student")
app.register_blueprint(attendance_bp, url_prefix="/api/attendance")
app.register_blueprint(lecture_bp, url_prefix="/api/lecture")

# JWT Error Handlers
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized - Invalid or missing token"}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Forbidden - Insufficient permissions"}), 403

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Authorization required - Token missing"}), 401

# ==================== WEB PAGES ====================

# API_BASE = "http://localhost:5000/api"
API_BASE = "/api"

@app.route("/")
def index():
    """Landing page — role selector"""
    return render_template("landing.html")

# ---- Auth portals ----
@app.route("/auth/student", methods=["GET"])
def auth_student():
    return render_template("auth_student.html", api_base=API_BASE)

@app.route("/auth/teacher", methods=["GET"])
def auth_teacher():
    return render_template("auth_teacher.html", api_base=API_BASE)

@app.route("/auth/admin", methods=["GET"])
def auth_admin():
    return render_template("auth_admin.html", api_base=API_BASE)

# ---- Role portals ----
@app.route("/portal/student", methods=["GET"])
def portal_student():
    return render_template("portal_student.html", api_base=API_BASE)

@app.route("/portal/teacher", methods=["GET"])
def portal_teacher():
    return render_template("portal_teacher.html", api_base=API_BASE)

@app.route("/portal/admin", methods=["GET"])
def portal_admin():
    return render_template("portal_admin.html", api_base=API_BASE)

@app.route("/api")
def api_info():
    """API information endpoint"""
    return {
        "message": "Face Recognition Attendance API",
        "version": "1.0.0",
        "web_pages": {
            "home": "/",
            "student_auth": "/auth/student",
            "teacher_auth": "/auth/teacher",
            "admin_auth": "/auth/admin"
        },
        "api_endpoints": {
            "authentication": "/api/auth/",
            "student": "/api/student/",
            "attendance": "/api/attendance/",
            "lecture": "/api/lecture/"
        }
    }

# if __name__ == "__main__":
#     # debug=True automatically restarts the server when you save code changes
#     app.run(debug=True, port=5000)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)