import face_recognition
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import os

# Define path to models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

PREDICTOR_PATH = os.path.join(MODEL_DIR, "shape_predictor_68_face_landmarks.dat")
RECOGNITION_MODEL_PATH = os.path.join(MODEL_DIR, "dlib_face_recognition_resnet_model_v1.dat")

# Patch the model paths into face_recognition
face_recognition.api.pose_predictor_68_point_model_location = lambda: PREDICTOR_PATH
face_recognition.api.face_recognition_model_location = lambda: RECOGNITION_MODEL_PATH

def encode_face(image_bytes) -> list:
    try:
        image = Image.open(BytesIO(image_bytes))
        image = np.array(image.convert('RGB'))

        # Detect faces
        face_locations = face_recognition.face_locations(image, model="hog")

        if not face_locations:
            return None

        # Encode faces using manually loaded models
        face_encoding = face_recognition.face_encodings(image, known_face_locations=face_locations)[0]
        return face_encoding.tolist()  # JSON serializable

    except Exception as e:
        print(f"⚠️ Face encoding failed: {e}")
        return None

