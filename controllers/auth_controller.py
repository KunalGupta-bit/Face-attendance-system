from flask import request, jsonify
from flask_jwt_extended import create_access_token
from models.auth_model import User
from datetime import timedelta

def register():
    """
    Register a new user.
    
    Expected JSON:
    {
        "email": "user@example.com",
        "password": "password123",
        "full_name": "John Doe",
        "role": "student"  # optional, defaults to 'student'
    }
    """
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        full_name = data.get("full_name", "").strip()
        role = data.get("role", "student").strip().lower()
        
        # Validate required fields
        if not email or not password or not full_name:
            return jsonify({"error": "Email, password, and full name are required"}), 400
        
        # Validate email format
        if "@" not in email or "." not in email:
            return jsonify({"error": "Invalid email format"}), 400
        
        # Validate password strength
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        
        # Validate role
        if role not in ["admin", "teacher", "student"]:
            role = "student"
        
        # Create user
        result = User.create_user(email, password, full_name, role)
        
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify({
            "message": "User registered successfully",
            "user": result
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def login():
    """
    Login user and return JWT token.
    
    Expected JSON:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Authenticate user
        user_info = User.authenticate(email, password)
        
        if "error" in user_info:
            return jsonify(user_info), 401
        
        # Create JWT token (expires in 24 hours)
        access_token = create_access_token(
            identity=user_info["id"],
            expires_delta=timedelta(hours=24),
            additional_claims={
                "email": user_info["email"],
                "role": user_info["role"],
                "full_name": user_info["full_name"]
            }
        )
        
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": user_info
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_current_user():
    """
    Get current logged-in user info (requires valid JWT token).
    This is called automatically by the @jwt_required decorator.
    """
    try:
        from flask_jwt_extended import get_jwt_identity, get_jwt
        
        user_id = get_jwt_identity()
        claims = get_jwt()
        
        return jsonify({
            "id": user_id,
            "email": claims.get("email"),
            "full_name": claims.get("full_name"),
            "role": claims.get("role")
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def logout():
    """
    Logout user (JWT tokens are stateless, so this is mainly for frontend).
    In production, you could implement token blacklisting here.
    """
    return jsonify({"message": "Logout successful"}), 200
