class AuthResponse:
    def __init__(self, supabase_response):
        self.user = supabase_response.user
        self.session = supabase_response.session
        self.access_token = self.session.access_token
        self.refresh_token = self.session.refresh_token

    def to_dict(self):
        try:
            response = {
                'access_token': self.access_token if hasattr(self, 'access_token') else None,
                'refresh_token': self.refresh_token if hasattr(self, 'refresh_token') else None,
                'user': {
                    'id': self.user.id,
                    'email': self.user.email,
                    'first_name': self.user.user_metadata.get('first_name') if hasattr(self.user, 'user_metadata') else None,
                    'last_name': self.user.user_metadata.get('last_name') if hasattr(self.user, 'user_metadata') else None,
                    'username': self.user.user_metadata.get('username') if hasattr(self.user, 'user_metadata') else None,
                    'website': self.user.user_metadata.get('website') if hasattr(self.user, 'user_metadata') else None,
                    'avatar_url': self.user.user_metadata.get('avatar_url') if hasattr(self.user, 'user_metadata') else None
                }
            }
            
            return response
        except Exception as e:
            
            print(f"Error in to_dict: {str(e)}")
            print(f"self.user type: {type(self.user)}")
            print(f"self.session type: {type(self.session)}")
            raise