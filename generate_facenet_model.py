from keras_facenet import FaceNet
from tensorflow.keras.models import save_model

print("Loading FaceNet model...")
embedder = FaceNet()

model = embedder.model  # underlying Keras model

print("Saving model as facenet_keras.h5...")
model.save("facenet_keras.h5")

print("Model saved successfully!")