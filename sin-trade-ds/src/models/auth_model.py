from datetime import datetime, timedelta

class AuthResponse:
    def __init__(self, auth_data):
        self.access_token = auth_data.get('access_token')
        self.token_type = auth_data.get('token_type')
        self.expires_in = auth_data.get('expires_in')
        self.expires_at = auth_data.get('expires_at')
        self.refresh_token = auth_data.get('refresh_token')
        self.user = User(auth_data.get('user', {})) if auth_data.get('user') else None

    @property
    def is_valid(self):
        if self.expires_at:
            return datetime.now() < datetime.fromtimestamp(self.expires_at)
        return False

    def to_dict(self):
         try:
           
            dict response = {
                'access_token': self.access_token,
                'token_type': self.token_type,
                'expires_in': self.expires_in,
                'expires_at': self.expires_at,
                'refresh_token': self.refresh_token,
                'user': self.user.to_dict() if self.user else None
            }
            
            return response
    except Exception as e:
            
            print(f"Error in to_dict: {str(e)}")
            print(f"self.user type: {type(self.user)}")
            print(f"self.session type: {type(self.session)}")
            raise