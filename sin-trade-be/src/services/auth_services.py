# services/auth_services.py
from src.models.auth_model import AuthResponse
from src.models.user_model import User
from src.config import BackendConfig
from flask import jsonify


class AuthService:
    @staticmethod
    def login(data):
        try:
            if BackendConfig.supabase:
                response = BackendConfig.supabase.auth.sign_in_with_password({
                    'email': data['email'],
                    'password': data['password']
                })
                auth_response = AuthResponse(response)
                auth_dict = auth_response.to_dict()
                return jsonify(auth_dict), 200
            return {"message": "Database connection unsuccessful"}, 500
        except Exception as e:
            return {"message": str(e)}, 401

    @staticmethod
    def signup(data):
        try:
            if BackendConfig.supabase:
                response = BackendConfig.supabase.auth.sign_up({
                    'email': data['email'],
                    'password': data['password'],
                    'options': {
                        'data': {
                            'first_name': data.get('first_name'),
                            'last_name': data.get('last_name'),
                            'username': data.get('username'),
                            'website': data.get('website'),
                            'avatar_url': data.get('avatar_url'),
                            'email': data.get('email')
                        }
                    }
                })
                auth_response = AuthResponse(response)
                return auth_response.to_dict(), 200
            return {"message": "Database connection unsuccessful"}, 500
        except Exception as e:
            return {"message": str(e)}, 400