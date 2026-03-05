from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client["face_attendance"]

teachers_collection = db["teachers"]
courses_collection = db["courses"]
students_collection = db["students"]
lectures_collection = db["lectures"]
attendance_collection = db["attendance"]