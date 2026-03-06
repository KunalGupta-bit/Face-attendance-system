# from flask import request, jsonify
# from database.db import students_collection
# from services.face_service import extract_faces, get_embedding
# import numpy as np
# import cv2
# import base64
# import os
# import zipfile
# import pandas as pd

# def register_student():
#     try:
#         data = request.json

#         if not data or "name" not in data or "roll" not in data or "image" not in data:
#             return jsonify({"error": "Invalid request data"}), 400
        
#         name = data["name"]
#         roll = data["roll"]
#         image_data = data["image"]

#         if students_collection.find_one({"roll": roll}):
#             return jsonify({"error": "Student already exists"}), 400
        
#         img_bytes = base64.b64decode(image_data.split(",")[1])
#         np_arr = np.frombuffer(img_bytes, np.uint8)
#         image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#         if image is None:
#             return jsonify({"error": "Invalid image data"}), 400
        
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#         faces = extract_faces(image)
#         if not faces:
#             return jsonify({"error": "No face detected"}), 400
        
#         embedding = get_embedding(faces[0])

#         students_collection.insert_one({
#             "name": name,
#             "roll": roll,
#             "embedding": embedding.tolist()
#         })

#         return jsonify({"message": "Student Registered Successfully"}), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# def update_student_embedding():
#     try:
#         data = request.json

#         if not data or "roll" not in data or "image" not in data:
#             return jsonify({"error": "Invalid request data"}), 400

#         roll = data["roll"]
#         image_data = data["image"]

#         student = students_collection.find_one({"roll": roll})
#         if not student:
#             return jsonify({"error": "Student not found"}), 404

#         img_bytes = base64.b64decode(image_data.split(",")[1])
#         np_arr = np.frombuffer(img_bytes, np.uint8)
#         image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#         if image is None:
#             return jsonify({"error": "Invalid image data"}), 400

#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#         faces = extract_faces(image)
#         if not faces:
#             return jsonify({"error": "No face detected"}), 400

#         embedding = get_embedding(faces[0])

#         students_collection.update_one({"roll": roll}, {"$set": {"embedding": embedding.tolist()}})

#         return jsonify({"message": "Embedding updated successfully"}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# def bulk_register_students():
#     try:
#         excel_file = request.files["excel"]
#         zip_file = request.files["images"]

#         df = pd.read_excel(excel_file)

#         zip_path = "temp_images.zip"
#         zip_file.save(zip_path)

#         with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#             zip_ref.extractall("temp_images")

#         for _, row in df.iterrows():
#             name = row["name"]
#             roll = row["roll"]
#             semester = row["semester"]

#             image_path = f"temp_images/{roll}.jpg"

#             if not os.path.exists(image_path):
#                 continue

#             image = cv2.imread(image_path)
#             if image is None:
#                 print(f"Skipping {roll} - image not found or corrupted")
#                 continue
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#             faces = extract_faces(image)
#             if not faces:
#                 print(f"Skipping {roll} - no face detected")
#                 continue

#             embedding = get_embedding(faces[0])

#             students_collection.insert_one({
#                 "name": name,
#                 "roll": roll,
#                 "semester": semester,
#                 "embedding": embedding.tolist()
#             })

#         return jsonify({"message": "Bulk Registration Completed"})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

from flask import request, jsonify
from database.db import students_collection
from services.face_service import extract_faces, get_embedding
import numpy as np
import cv2
import base64
import os
import zipfile
import pandas as pd
import shutil

def process_base64_image(image_data):
    try:
        if not image_data or not isinstance(image_data, str):
            print("Error: image_data is empty or not a string")
            return None

        # 1. Clean the Base64 string
        if "," in image_data:
            # Splits 'data:image/jpeg;base64,/9j/...' and takes the second part
            image_data = image_data.split(",")[1]
        
        # 2. Decode bytes
        img_bytes = base64.b64decode(image_data)
        if not img_bytes:
            print("Error: Decoded bytes are empty")
            return None

        # 3. Convert to numpy array
        np_arr = np.frombuffer(img_bytes, np.uint8)
        if np_arr.size == 0:
            print("Error: Numpy array from buffer is empty")
            return None

        # 4. Decode to OpenCV image
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            print("Error: OpenCV failed to decode the buffer (invalid image format)")
            return None
        
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(f"Exception during image processing: {e}")
        return None
    

def register_student():
    try:
        data = request.json

        # Added "semester" to the check
        if not data or not all(k in data for k in ["name", "roll", "image", "semester"]):
            return jsonify({"error": "Name, Roll, Semester, and Image are required"}), 400
        
        name = data["name"]
        roll = data["roll"]
        semester = data["semester"]
        image_data = data["image"]

        if students_collection.find_one({"roll": roll}):
            return jsonify({"error": "Student already exists"}), 400
        
        image = process_base64_image(image_data)
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400

        faces = extract_faces(image)
        if not faces:
            return jsonify({"error": "No face detected"}), 400
        
        embedding = get_embedding(faces[0])

        # Store semester in the database
        students_collection.insert_one({
            "name": name,
            "roll": roll,
            "semester": semester,
            "embedding": embedding.tolist()
        })

        return jsonify({"message": "Student Registered Successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_student_embedding():
    try:
        data = request.json
        roll = data.get("roll")
        
        student = students_collection.find_one({"roll": roll})
        if not student:
            return jsonify({"error": "Student not found"}), 404

        image = process_base64_image(data.get("image", ""))
        if image is None:
            return jsonify({"error": "Invalid image"}), 400

        faces = extract_faces(image)
        if not faces:
            return jsonify({"error": "No face detected"}), 400

        embedding = get_embedding(faces[0])
        students_collection.update_one({"roll": roll}, {"$set": {"embedding": embedding.tolist()}})

        return jsonify({"message": "Embedding updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def bulk_register_students():
    temp_dir = "temp_bulk_images"
    try:
        excel_file = request.files.get("excel")
        zip_file = request.files.get("images")

        if not excel_file or not zip_file:
            return jsonify({"error": "Missing files"}), 400

        df = pd.read_excel(excel_file)
        
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        zip_path = os.path.join(temp_dir, "upload.zip")
        zip_file.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        count = 0
        # Walk through all files in the extracted dir (handles subfolders)
        extracted_files = {}
        for root, dirs, files in os.walk(temp_dir):
            for f in files:
                name_part = os.path.splitext(f)[0]
                extracted_files[name_part] = os.path.join(root, f)

        for _, row in df.iterrows():
            roll = str(row["roll"]).strip()
            
            # Check if we have an image for this roll number
            if roll in extracted_files:
                image_path = extracted_files[roll]
                img = cv2.imread(image_path)
                
                if img is None:
                    print(f"Could not read image for {roll}")
                    continue
                
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                faces = extract_faces(img_rgb)
                
                if faces:
                    embedding = get_embedding(faces[0])
                    students_collection.update_one(
                        {"roll": roll},
                        {"$set": {
                            "name": row["name"],
                            "semester": row.get("semester"),
                            "embedding": embedding.tolist()
                        }},
                        upsert=True
                    )
                    count += 1
                else:
                    print(f"No face detected in {image_path}")

        return jsonify({"message": f"Bulk Registration Completed. {count} students processed."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def get_all_students():
    try:
        # Retrieve all students, but don't send the long embedding arrays
        students = list(students_collection.find({}, {"embedding": 0}))
        
        # Convert MongoDB ObjectId to string so JSON can handle it
        for s in students:
            s["_id"] = str(s["_id"])
            
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500