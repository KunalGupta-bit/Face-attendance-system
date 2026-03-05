from flask import request, jsonify
from database.db import students_collection
from services.face_service import extract_face, get_embedding
import numpy as np
import cv2
import base64

def register_student():
    try:
        data = request.json

        if not data or "name" not in data or "roll" not in data or "image" not in data:
            return jsonify({"error": "Invalid request data"}), 400
        
        name = data["name"]
        roll = data["roll"]
        image_data = data["image"]

        if student_collection.find_one({"roll": roll}):
            return jsonify({"error": "Student already exists"}), 400
        
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

        student_collection.insert_one({
            "name": name,
            "roll": roll,
            "embedding": embedding.tolist()
        })

        return jsonify({"message": "Student Registered Successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_student_embedding():
    try:
        data = request.json

        if not data or "roll" not in data or "image" not in data:
            return jsonify({"error": "Invalid request data"}), 400

        roll = data["roll"]
        image_data = data["image"]

        student = student_collection.find_one({"roll": roll})
        if not student:
            return jsonify({"error": "Student not found"}), 404

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

        student_collection.update_one({"roll": roll}, {"$set": {"embedding": embedding.tolist()}})

        return jsonify({"message": "Embedding updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500