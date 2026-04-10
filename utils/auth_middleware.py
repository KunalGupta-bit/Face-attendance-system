from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify

def require_role(*allowed_roles):
    """
    Decorator to check if user has required role(s).
    
    Usage:
    @require_role('admin', 'teacher')
    def some_function():
        ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")
            
            if user_role not in allowed_roles:
                return jsonify({"error": "Insufficient permissions"}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_only(fn):
    """Decorator to restrict access to admin users only"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        
        if claims.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def teacher_or_admin(fn):
    """Decorator to allow teacher and admin users"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        
        if claims.get("role") not in ["admin", "teacher"]:
            return jsonify({"error": "Teacher or admin access required"}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def authenticated_required(fn):
    """Decorator to require any authenticated user"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper
