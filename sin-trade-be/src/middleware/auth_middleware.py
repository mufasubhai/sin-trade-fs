# src/middleware/auth_middleware.py
from flask import request, jsonify
from src.config import BackendConfig
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'No authorization header', "status": 401}), 401
        
        # Extract token (assuming "Bearer <token>" format)
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'message': 'Unable to authenticate', "status": 401}), 401
        
        # Verify token with Supabase
        try:
            if BackendConfig.supabase:
                # Set the session for this request
                BackendConfig.supabase.auth.set_session(token, "")
                user = BackendConfig.supabase.auth.get_user(token)
                
                if not user:
                    return jsonify({'message': 'User not found. Please login again', "status": 401}), 401
                
                # Add user info to request context
                request.current_user = user
                return f(*args, **kwargs)
            else:
                return jsonify({'message': 'Unable to connect to database', "status": 500}), 500
        except Exception as e:
            return jsonify({'message': f'Authentication failed: {str(e)}', "status": 401}), 401
    
    return decorated_function