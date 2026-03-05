import os, sys
sys.path.append(os.getcwd())
from services.face_service import load_face_model

ok = load_face_model()
print('Model loaded:', ok)
