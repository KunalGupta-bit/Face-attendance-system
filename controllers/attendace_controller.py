# from flask import request, jsonify
# from database.db import students_collection, attendance_collection
# from services.face_service import extract_faces, get_embedding
# import numpy as np
# import cv2
# import base64
# from datetime import datetime
# from numpy.linalg import norm
# from bson import ObjectId


# def cosine_similarity(a, b):
#     denom = norm(a) * norm(b)
#     if denom == 0 or np.isnan(denom):
#         return -1.0
#     return float(np.dot(a, b) / denom)


# def mark_attendance():
#     try:
#         data = request.json

#         if not data or "image" not in data or "lecture_id" not in data:
#             return jsonify({"error": "image and lecture_id are required"}), 400

#         lecture_id = data["lecture_id"]
#         image_data = data["image"]

#         img_bytes = base64.b64decode(image_data.split(",")[1])
#         np_arr = np.frombuffer(img_bytes, np.uint8)
#         image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#         if image is None:
#             return jsonify({"error": "Invalid image data"}), 400

#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#         faces = extract_faces(image)

#         if not faces:
#             return jsonify({"error": "No faces detected"}), 400

#         students = list(students_collection.find())

#         marked_students = []

#         for face in faces:

#             embedding = get_embedding(face)

#             for student in students:

#                 stored_embedding = np.array(student["embedding"])
#                 similarity = cosine_similarity(embedding, stored_embedding)

#                 print("Similarity with", student["name"], ":", similarity)

#                 if similarity > 0.55:

#                     existing = attendance_collection.find_one({
#                         "lecture_id": ObjectId(lecture_id),
#                         "student_id": student["_id"]
#                     })

#                     if not existing:

#                         attendance_collection.insert_one({
#                             "lecture_id": ObjectId(lecture_id),
#                             "student_id": student["_id"],
#                             "name": student["name"],
#                             "timestamp": datetime.now(),
#                             "status": "Present"
#                         })

#                         marked_students.append(student["name"])

#                     break

#         if not marked_students:
#             return jsonify({"message": "No students recognized"}), 404

#         return jsonify({
#             "message": "Attendance processed",
#             "students_marked": marked_students
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

from flask import request, jsonify
from database.db import students_collection, attendance_collection
from services.face_service import extract_faces, get_embedding
import numpy as np
import cv2
import base64
from datetime import datetime
from numpy.linalg import norm
from bson import ObjectId

def cosine_similarity(a, b):
    denom = norm(a) * norm(b)
    if denom == 0 or np.isnan(denom):
        return -1.0
    return float(np.dot(a, b) / denom)

def mark_attendance():
    try:
        data = request.json
        if not data or "image" not in data or "lecture_id" not in data:
            return jsonify({"error": "image and lecture_id are required"}), 400

        lecture_id = data["lecture_id"]
        image_data = data["image"]

        # Handle Base64 conversion safely
        if "," in image_data:
            image_data = image_data.split(",")[1]
        
        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Invalid image data"}), 400

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Optimization: Fetch all students once
        students = list(students_collection.find())
        if not students:
            return jsonify({"error": "No registered students found"}), 404

        marked_students = []
        faces = extract_faces(image)

        if not faces:
            return jsonify({"error": "No faces detected in the image"}), 400

        for face in faces:
            embedding = get_embedding(face)
            best_match = None
            max_sim = -1

            for student in students:
                stored_emb = np.array(student["embedding"])
                sim = cosine_similarity(embedding, stored_emb)
                
                if sim > max_sim:
                    max_sim = sim
                    best_match = student

            # Threshold check (0.70 is the sweet spot for FaceNet cosine similarity)
            if best_match and max_sim > 0.70:
                # Check for duplicate attendance in this specific lecture
                existing = attendance_collection.find_one({
                    "lecture_id": ObjectId(lecture_id),
                    "student_id": best_match["_id"]
                })

                if not existing:
                    attendance_collection.insert_one({
                        "lecture_id": ObjectId(lecture_id),
                        "student_id": best_match["_id"],
                        "name": best_match["name"],
                        "timestamp": datetime.now(),
                        "status": "Present"
                    })
                    marked_students.append(best_match["name"])

        if not marked_students:
            return jsonify({"message": "Faces detected but no students recognized"}), 404

        return jsonify({
            "message": "Attendance processed",
            "students_marked": marked_students
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_lecture_attendance(lecture_id):
    try:
        # Find all attendance records for this specific lecture
        records = list(attendance_collection.find({"lecture_id": ObjectId(lecture_id)}))
        
        # Format for frontend
        output = []
        for rec in records:
            output.append({
                "name": rec["name"],
                "time": rec["timestamp"].strftime("%H:%M:%S"),
                "status": rec["status"]
            })
            
        return jsonify({"attendance": output}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_attendance_report():
    try:
        # Get all records, sorted by most recent first
        report = list(attendance_collection.find().sort("timestamp", -1))
        
        for r in report:
            r["_id"] = str(r["_id"])
            r["lecture_id"] = str(r["lecture_id"])
            r["student_id"] = str(r["student_id"])
            # Format date for the UI
            r["timestamp"] = r["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500