from flask import Flask
from flask_cors import CORS
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(student_bp, url_prefix="/api/student")
app.register_blueprint(attendance_bp, url_prefix="/api/attendance")

@app.route("/")
def home():
    return {"message": "Face Recognition Attendance API Running"}

if __name__ == "__main__":
    app.run(debug=True)