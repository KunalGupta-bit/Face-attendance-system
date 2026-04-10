from flask import Flask, jsonify, render_template, redirect, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from config import Config
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp
from routes.lecture_routes import lecture_bp
from routes.auth_routes import auth_bp

app = Flask(__name__, template_folder="templates")

# JWT Configuration
app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY or "your-secret-key-change-this"
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

@app.route("/")
def index():
    """Home page - redirects to app"""
    return redirect("/app")

@app.route("/login", methods=["GET"])
def login():
    """Login/Register page"""
    return render_template("login.html", api_base="http://localhost:5000/api")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Dashboard page (frontend checks authentication)"""
    return render_template("dashboard.html", api_base="http://localhost:5000/api")

@app.route("/app", methods=["GET"])
def attendance_app():
    """Attendance system app"""
    return render_template("index.html")

@app.route("/api")
def api_info():
    """API information endpoint"""
    return {
        "message": "Face Recognition Attendance API",
        "version": "1.0.0",
        "web_pages": {
            "login": "/login",
            "dashboard": "/dashboard",
            "home": "/"
        },
        "api_endpoints": {
            "authentication": "/api/auth/",
            "student": "/api/student/",
            "attendance": "/api/attendance/",
            "lecture": "/api/lecture/"
        }
    }

if __name__ == "__main__":
    # debug=True automatically restarts the server when you save code changes
    app.run(debug=True, port=5000)