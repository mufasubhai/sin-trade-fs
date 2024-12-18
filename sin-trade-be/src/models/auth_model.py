class AuthResponse:
    def __init__(self, supabase_response):
        # Handle both session-based (login) and direct user (registration) responses
        if hasattr(supabase_response, 'user') and hasattr(supabase_response, 'session'):
            # Login response
            
            self.user = supabase_response.user
            self.aud = self.user.aud if hasattr(self.user, 'aud') else None
            self.session = supabase_response.session
            self.access_token = self.session.access_token if hasattr(self.session, 'access_token') else None
            self.refresh_token = self.session.refresh_token if hasattr(self.session, 'refresh_token') else None
   

    def to_dict(self):
        try:
            response = {
                'access_token': self.access_token,
                'aud': self.aud,
                'refresh_token': self.refresh_token,
                'user': {
                    'id': self.user.id,
                    'email': self.user.email,
                    'first_name': self.user.user_metadata.get('first_name') if hasattr(self.user, 'user_metadata') else None,
                    'last_name': self.user.user_metadata.get('last_name') if hasattr(self.user, 'user_metadata') else None,
                    'username': self.user.user_metadata.get('username') if hasattr(self.user, 'user_metadata') else None,
                    'website': self.user.user_metadata.get('website') if hasattr(self.user, 'user_metadata') else None,
                    'avatar_url': self.user.user_metadata.get('avatar_url') if hasattr(self.user, 'user_metadata') else None,
                    'email_verified': self.user.user_metadata.get('email_verified') if hasattr(self.user, 'user_metadata') else None,
                    'phone_verified': self.user.user_metadata.get('phone_verified') if hasattr(self.user, 'user_metadata') else None,
                    'created_at': self.user.created_at if hasattr(self.user, 'created_at') else None,
                    'updated_at': self.user.updated_at if hasattr(self.user, 'updated_at') else None
                }
            }
            
            return response
        except Exception as e:
            print(f"Error in to_dict: {str(e)}")
            print(f"self.user type: {type(self.user)}")
            raise