from flask import request, jsonify
from database.db import student_collection, attendance_collection
from services.face_service import extract_face, get_embedding
import numpy as np
import cv2
import base64
from datetime import datetime
from numpy.linalg import norm

def cosine_similarity(a, b):
    denom = norm(a) * norm(b)
    if denom == 0 or np.isnan(denom):
        return -1.0
    return float(np.dot(a, b) / denom)

def mark_attendance():
    try:
        data = request.json

        if not data or "image" not in data:
            return jsonify({"error": "Image is required"}), 400

        image_data = data["image"]

        img_bytes = base64.b64decode(image_data.split(",")[1])
        np_arr = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Invalid image data"}), 400
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        face = extract_face(image)
        if face is None:
            return jsonify({"error": "No face detected"}), 400
        

        embedding = get_embedding(face)

        students = list(student_collection.find())

        for student in students:
            stored_embedding = np.array(student["embedding"])
            similarity = cosine_similarity(embedding, stored_embedding)
            print("Similarity with", student["name"], ":", similarity)

            if similarity > 0.55:

                today = datetime.now().date().isoformat()

                existing = attendance_collection.find_one({
                    "student_id": student["_id"],
                    "date": today
                })

                if existing:
                    return jsonify({
                        "message": "Attendance already marked today",
                        "name": student["name"]
                    }), 200

                attendance_collection.insert_one({
                    "student_id": student["_id"],
                    "name": student["name"],
                    "date": today,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "status": "Present"
                })

                return jsonify({
                    "message": "Attendance Marked",
                    "name": student["name"]
                }), 200

        return jsonify({"message": "Student Not Recognized"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500