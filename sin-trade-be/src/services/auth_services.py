# services/auth_services.py
from src.models.auth_model import AuthResponse
from src.models.user_model import User, ProfileResponse
from src.models.active_assets_model import ActiveAssets
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
                
                #  We need  to add some tests for this. 
                
                
                # initial response from supabase
                auth_response = AuthResponse(response)
                auth_dict = auth_response.to_dict()
                
                # set session for supabase
                BackendConfig.supabase.auth.set_session(auth_dict['access_token'], auth_dict['refresh_token'])
                
                # get profile from supabase
                profile_response = BackendConfig.supabase.table("profiles").select('*').eq('id', auth_dict['user']['id']).execute()
                
                # convert profile to object
                profile_object = ProfileResponse(profile_response.data[0]).to_dict()
                
                # get active assets from supabase
                active_assets_response = BackendConfig.supabase.table("user_assets").select('*').eq('user_id', profile_object['user_id']).execute()
                
                # convert active assets to object
                active_assets_object = ActiveAssets(active_assets_response.data)
                
                # convert active assets to dict
                active_assets_dict = active_assets_object.to_dict()
                
                # add active assets to profile object
                profile_object['active_assets'] = active_assets_dict['active_assets']
                
                # convert profile object to user object
                user = User(profile_object)
                
                # set access token and refresh token
                user.access_token = auth_dict['access_token']
                user.refresh_token = auth_dict['refresh_token']
                user.website = auth_dict['user']['website']
                user.created_at = auth_dict['user']['created_at']
                user.updated_at = auth_dict['user']['updated_at']
                
                return jsonify(user.to_dict()), 200
            
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