from flask import request, jsonify
from database.db import lectures_collection
from datetime import datetime

def create_lecture():
    data = request.json
    teacher_id = data.get("teacher_id")
    course_id = data.get("course_id", "General")

    if not teacher_id:
        return jsonify({"error": "Teacher ID is required to start a lecture"}), 400

    lecture = {
        "course_id": course_id,
        "teacher_id": teacher_id, # Linked to the teacher
        "date": datetime.now().strftime("%Y-%m-%d"),
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "status": "active"
    }

    result = lectures_collection.insert_one(lecture)
    return jsonify({
        "message": f"Lecture created for Teacher {teacher_id}",
        "lecture_id": str(result.inserted_id)
    }), 201

def get_all_lectures():
    lectures = list(lectures_collection.find().sort("date", -1))
    for l in lectures: l["_id"] = str(l["_id"])
    return jsonify(lectures)