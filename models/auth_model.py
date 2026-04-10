import bcrypt
from datetime import datetime
from database.db import db

users_collection = db["users"]

class User:
    """
    User model for authentication.
    Supports role-based access: 'admin', 'teacher', 'student'
    """
    
    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed_password):
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def create_user(email, password, full_name, role='student'):
        """
        Create a new user in the database.
        
        Args:
            email: User email (unique identifier)
            password: Plain text password (will be hashed)
            full_name: User's full name
            role: User role - 'admin', 'teacher', or 'student'
        
        Returns:
            dict with user info or error message
        """
        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return {"error": "User with this email already exists"}
        
        user_data = {
            "email": email,
            "password_hash": User.hash_password(password),
            "full_name": full_name,
            "role": role,
            "created_at": datetime.utcnow(),
            "last_login": None,
            "is_active": True
        }
        
        result = users_collection.insert_one(user_data)
        return {"id": str(result.inserted_id), "email": email, "full_name": full_name, "role": role}
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return users_collection.find_one({"email": email})
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by MongoDB ObjectId"""
        from bson import ObjectId
        return users_collection.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def authenticate(email, password):
        """
        Authenticate a user.
        
        Returns:
            dict with user info if successful, error message otherwise
        """
        user = User.get_user_by_email(email)
        
        if not user:
            return {"error": "Invalid email or password"}
        
        if not user.get("is_active"):
            return {"error": "User account is inactive"}
        
        if not User.verify_password(password, user["password_hash"]):
            return {"error": "Invalid email or password"}
        
        # Update last login
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        return {
            "id": str(user["_id"]),
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        }
    
    @staticmethod
    def update_user(user_id, updates):
        """Update user information"""
        from bson import ObjectId
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updates}
        )
        return User.get_user_by_id(user_id)
