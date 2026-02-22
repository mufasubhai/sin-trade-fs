import pytest
from src.models.auth_model import AuthResponse
from src.models.user_model import User, ProfileResponse
from src.models.active_assets_model import ActiveAssets
from unittest.mock import MagicMock


class TestModels:
    def test_auth_response_login(self):
        mock_user = MagicMock()
        mock_user.id = "user123"
        mock_user.email = "test@example.com"
        mock_user.user_metadata = {"first_name": "John", "last_name": "Doe"}
        mock_user.aud = "authenticated"
        
        mock_session = MagicMock()
        mock_session.access_token = "access_token_123"
        mock_session.refresh_token = "refresh_token_123"
        
        mock_response = MagicMock()
        mock_response.user = mock_user
        mock_response.session = mock_session
        
        auth = AuthResponse(mock_response)
        result = auth.to_dict()
        
        assert result["access_token"] == "access_token_123"
        assert result["refresh_token"] == "refresh_token_123"
        assert result["user"]["id"] == "user123"

    def test_profile_response_init(self):
        from datetime import datetime
        profile_data = {
            "id": 1,
            "user_id": "user123",
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "avatar_url": "http://example.com/avatar.png",
            "updated_at": datetime.now()
        }
        
        profile = ProfileResponse(profile_data)
        result = profile.to_dict()
        
        assert result["user_id"] == "user123"
        assert result["email"] == "test@example.com"
        assert result["username"] == "testuser"

    def test_profile_response_missing_fields(self):
        profile_data = {"id": 1}
        
        profile = ProfileResponse(profile_data)
        result = profile.to_dict()
        
        assert result["user_id"] is None
        assert result["email"] is None

    def test_user_init(self):
        user_data = {
            "id": 1,
            "user_id": "user123",
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "active_assets": {}
        }
        
        user = User(user_data)
        
        assert user.user_id == "user123"
        assert user.email == "test@example.com"
        assert user.first_name == "John"

    def test_user_full_name(self):
        user_data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        
        user = User(user_data)
        
        assert user.full_name == "John Doe"

    def test_user_full_name_no_last_name(self):
        user_data = {
            "first_name": "John"
        }
        
        user = User(user_data)
        
        assert "John" in user.full_name

    def test_user_to_dict(self):
        user_data = {
            "user_id": "user123",
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "active_assets": {"BTC": {}},
        }
        
        user = User(user_data)
        
        assert user.user_id == "user123"
        assert user.email == "test@example.com"

    def test_active_assets_init(self):
        assets_list = [
            {"ticker_name": "BTC", "id": 1},
            {"ticker_name": "ETH", "id": 2}
        ]
        
        active_assets = ActiveAssets(assets_list)
        
        assert "BTC" in active_assets.active_assets
        assert "ETH" in active_assets.active_assets

    def test_active_assets_empty(self):
        assets_list = []
        
        active_assets = ActiveAssets(assets_list)
        
        assert active_assets.active_assets == {}

    def test_active_assets_to_dict(self):
        assets_list = [
            {"ticker_name": "BTC", "id": 1}
        ]
        
        active_assets = ActiveAssets(assets_list)
        result = active_assets.to_dict()
        
        assert "active_assets" in result
        assert "BTC" in result["active_assets"]
