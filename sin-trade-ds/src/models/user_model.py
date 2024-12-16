
from datetime import datetime

class User:
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.email = user_data.get('email')
        self.role = user_data.get('role')
        self.email_confirmed_at = self._parse_datetime(user_data.get('email_confirmed_at'))
        self.last_sign_in_at = self._parse_datetime(user_data.get('last_sign_in_at'))
        self.created_at = self._parse_datetime(user_data.get('created_at'))
        self.updated_at = self._parse_datetime(user_data.get('updated_at'))
        
        # User metadata
        metadata = user_data.get('user_metadata', {})
        self.username = metadata.get('username')
        self.first_name = metadatag.et('first_name')
        self.last_name = metadata.get('last_name')
        self.avatar_url = metadata.get('avatar_url')
        self.website = metadata.get('website')
        
        # App metadata
        # app_metadata = user_data.get('app_metadata', {})
        # self.provider = app_metadata.get('provider')
        # self.providers = app_metadata.get('providers', [])



    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'website': self.website,
            'role': self.role,
            'email_confirmed_at': self.email_confirmed_at.isoformat() if self.email_confirmed_at else None,
            'last_sign_in_at': self.last_sign_in_at.isoformat() if self.last_sign_in_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'provider': self.provider,
            'providers': self.providers
        }