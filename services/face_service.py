# import cv2
# import numpy as np
# from mtcnn import MTCNN
# from tensorflow.keras.models import load_model
# from keras_facenet import FaceNet
# import os

# detector = MTCNN()

# MODEL_PATH = os.path.join(
#     os.path.dirname(__file__),
#     "..",
#     "models",
#     "facenet_keras.h5"
# )

# model = None

# def load_face_model():
#     global model
#     if model is None:
#         try:
#             model = load_model(MODEL_PATH)
#         except Exception as e:
#             print(f"Warning: load_model failed: {e}")
#             try:
#                 model = load_model(MODEL_PATH, custom_objects={"scaling": lambda x: x})
#             except Exception as e2:
#                 print(f"Warning: load_model with custom_objects failed: {e2}")
#                 try:
#                     embedder = FaceNet()
#                     model = embedder.model
#                 except Exception as e3:
#                     print(f"Warning: keras_facenet fallback failed: {e3}")
#                     return False
#     return True

# def get_embedding(face_pixels):

#     if face_pixels is None or face_pixels.size == 0:
#         return None

#     face_pixels = face_pixels.astype("float32")

#     mean, std = face_pixels.mean(), face_pixels.std()
#     face_pixels = (face_pixels - mean) / (std + 1e-6)

#     samples = np.expand_dims(face_pixels, axis=0)

#     yhat = model.predict(samples)

#     return yhat[0]

# def extract_faces(image):
#     results = detector.detect_faces(image)
#     faces = []

#     for result in results:
#         x1, y1, width, height = result['box']

#         x1, y1 = abs(x1), abs(y1)

#         x2 = x1 + width
#         y2 = y1 + height

#         face = image[y1:y2, x1:x2]

#         if face.size == 0:
#             continue

#         try:
#             face = cv2.resize(face, (160,160))
#             faces.append(face)
#         except:
#             continue

#     return faces

import cv2
import numpy as np
from mtcnn import MTCNN
from keras_facenet import FaceNet
import os

# Initialize detector and embedder globally
detector = MTCNN()
embedder = FaceNet() # This loads the pre-trained model automatically

def get_embedding(face_pixels):
    if face_pixels is None or face_pixels.size == 0:
        return None

    # FaceNet expects (160, 160) which you already resize to in extract_faces
    # the 'embeddings' method handles normalization and expand_dims internally
    detections = [{'box': [0, 0, 160, 160], 'confidence': 1.0}] 
    # Use the helper directly for a single cropped face
    embeddings = embedder.embeddings(np.expand_dims(face_pixels, axis=0))
    
    return embeddings[0]

def extract_faces(image):
    results = detector.detect_faces(image)
    faces = []
    for result in results:
        # Filter by confidence to avoid ghost detections
        if result['confidence'] < 0.90:
            continue
            
        x1, y1, width, height = result['box']

        if width < 50 or height < 50:
            continue
        x1, y1 = max(0, x1), max(0, y1) # Use max to prevent negative slicing
        x2, y2 = x1 + width, y1 + height

        face = image[y1:y2, x1:x2]
        if face.size == 0: continue

        face = cv2.resize(face, (160, 160))
        faces.append(face)
    return faces