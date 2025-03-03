
from datetime import datetime
from src.utils.date_utils import parse_datetime


class ProfileResponse:
    def __init__(self, profile_data):
        self.id = profile_data.get('id')
        self.user_id = profile_data.get('user_id')
        self.email = profile_data.get('email')
        self.username = profile_data.get('username')
        self.first_name = profile_data.get('first_name')
        self.last_name = profile_data.get('last_name')
        self.avatar_url = profile_data.get('avatar_url')
        self.updated_at = profile_data.get('updated_at')
        self.active_assets = profile_data.get('active_assets')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id if self.user_id else None,
            'email': self.email if self.email else None,
            'username': self.username if self.username else None,
            'first_name': self.first_name if self.first_name else None,
            'last_name': self.last_name if self.last_name else None,
            'avatar_url': self.avatar_url if self.avatar_url else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'active_assets': self.active_assets if self.active_assets else {},
        }
       
       
        

class User:
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.user_id = user_data.get('user_id')
        self.email = user_data.get('email')
        self.username = user_data.get('username')
        self.first_name = user_data.get("first_name")
        self.last_name = user_data.get("last_name")
        self.avatar_url = user_data.get("avatar_url")
        self.website = user_data.get("website")
        self.email_confirmed_at =user_data.get('email_confirmed_at')
        self.created_at =user_data.get('created_at')
        self.updated_at =user_data.get('updated_at')
        self.active_assets = user_data.get("active_assets")
        # self.phone = user_data.get("phone")
        self.refresh_token = user_data.get("refresh_token")
        
        
        

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'avatar_url': self.avatar_url,
            'website': self.website,
            'email_confirmed_at': self.email_confirmed_at.isoformat() if self.email_confirmed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'active_assets': self.active_assets,
            # 'phone': self.phone,
            'refresh_token': self.refresh_token,
            'access_token': self.access_token
        }
        
