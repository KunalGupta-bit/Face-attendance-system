from flask import Flask
from flask_cors import CORS
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp
from routes.lecture_routes import lecture_bp

app = Flask(__name__)

# CORS allows your browser (index.html) to communicate with this Flask server
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Registering Blueprints
app.register_blueprint(student_bp, url_prefix="/api/student")
app.register_blueprint(attendance_bp, url_prefix="/api/attendance")
app.register_blueprint(lecture_bp, url_prefix="/api/lecture")

@app.route("/")
def home():
    return {"message": "Face Recognition Attendance API Running"}

if __name__ == "__main__":
    # debug=True automatically restarts the server when you save code changes
    app.run(debug=True, port=5000)