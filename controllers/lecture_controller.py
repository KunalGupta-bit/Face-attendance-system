from flask import request, jsonify
from database.db import lectures_collection
from datetime import datetime

def create_lecture():
    data = request.json

    course_id = data["course_id"]
    teacher_id = data["teacher_id"]

    lecture = {
        "course_id": course_id,
        "teacher_id": teacher_id,
        "date": datetime.now().date().isoformat(),
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "status": "active"
    }

    result = lectures_collection.insert_one(lecture)

    return jsonify({
        "message": "Lecture created",
        "lecture_id": str(result.inserted_id)
    })