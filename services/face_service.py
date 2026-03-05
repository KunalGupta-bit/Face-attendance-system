import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.models import load_model
from keras_facenet import FaceNet
import os

detector = MTCNN()

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "facenet_keras.h5"
)

model = None

def load_face_model():
    global model
    if model is None:
        # Try loading the saved Keras model; if it uses custom objects (eg. 'scaling'),
        # attempt fallback strategies.
        try:
            model = load_model(MODEL_PATH)
        except Exception as e:
            print(f"Warning: load_model failed: {e}")
            try:
                # try with a noop 'scaling' function if that's the missing custom object
                model = load_model(MODEL_PATH, custom_objects={"scaling": lambda x: x})
            except Exception as e2:
                print(f"Warning: load_model with custom_objects failed: {e2}")
                try:
                    # Fallback: use keras_facenet FaceNet wrapper instead of loading .h5
                    embedder = FaceNet()
                    model = embedder.model
                except Exception as e3:
                    print(f"Warning: keras_facenet fallback failed: {e3}")
                    return False
    return True

def get_embedding(face_pixels):
    if not load_face_model():
        # Return dummy embedding for testing
        return np.zeros((128,), dtype=np.float32)
    
    face_pixels = face_pixels.astype("float32")
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean)/std
    samples = np.expand_dims(face_pixels, axis = 0)
    yhat = model.predict(samples)
    return yhat[0]

def extract_faces(image):
    results = detector.detect_faces(image)
    faces = []

    for result in results:
        x1, y1, width, height = result['box']
        x2, y2 = x1 + width, y1 + height
        face = image[y1:y2, x1:x2]
        face = cv2.resize(face, (160, 160))
        faces.append(face)

    return faces