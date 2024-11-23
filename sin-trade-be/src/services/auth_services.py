# services/auth_service.py
from models.user_model import User
from flask import jsonify
from config import BackendConfig
class AuthService:
    @staticmethod
    def signup(data):
        email = data['email']
        password = data['password']

        if BackendConfig.supabase != None:
            response = BackendConfig.supabase.auth.sign_up({
                'email': email,
                'password': password
            })
            return response
    
        return {"message": "Database connection unsuccessful"}, 500

    @staticmethod
    def login(data):
        # user = User.query.filter_by(username=data['username']).first()
        # if user and user.check_password(data['password']):
            # Implement JWT token creation here
        return {"message": "Login successful"}, 200
        # return {"message": "Invalid credentials"}, 401

    @staticmethod
    def logout(): 
        return {"status": "success"}, 200
        # Handle token revocation if using JWTs or sessions
        