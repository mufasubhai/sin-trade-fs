import pytest
from unittest.mock import MagicMock, patch


class TestAuthServices:
    @patch('src.services.auth_services.BackendConfig.supabase')
    def test_login_no_db(self, mock_supabase):
        from src.services.auth_services import AuthService
        
        with patch('src.services.auth_services.BackendConfig') as mock_config:
            mock_config.supabase = None
            
            data = {"email": "test@example.com", "password": "password123"}
            result = AuthService.login(data)
            
            assert result[1] == 500

    @patch('src.services.auth_services.BackendConfig.supabase')
    def test_login_exception(self, mock_supabase):
        from src.services.auth_services import AuthService
        
        mock_supabase.auth.sign_in_with_password.side_effect = Exception("Auth failed")
        
        data = {"email": "test@example.com", "password": "wrong_password"}
        result = AuthService.login(data)
        
        assert result[1] == 401

    @patch('src.services.auth_services.BackendConfig.supabase')
    def test_signup_success(self, mock_supabase):
        from src.services.auth_services import AuthService
        
        mock_user = MagicMock()
        mock_user.id = "user123"
        
        mock_response = MagicMock()
        mock_response.user = mock_user
        
        mock_supabase.auth.sign_up.return_value = mock_response
        
        data = {"email": "test@example.com", "password": "password123", "first_name": "John", "last_name": "Doe", "username": "johndoe"}
        result = AuthService.signup(data)
        
        assert result[1] == 200

    @patch('src.services.auth_services.BackendConfig.supabase')
    def test_signup_no_db(self, mock_supabase):
        from src.services.auth_services import AuthService
        
        with patch('src.services.auth_services.BackendConfig') as mock_config:
            mock_config.supabase = None
            
            data = {"email": "test@example.com", "password": "password123"}
            result = AuthService.signup(data)
            
            assert result[1] == 500

    @patch('src.services.auth_services.BackendConfig.supabase')
    def test_signup_exception(self, mock_supabase):
        from src.services.auth_services import AuthService
        
        mock_supabase.auth.sign_up.side_effect = Exception("Signup failed")
        
        data = {"email": "test@example.com", "password": "password123"}
        result = AuthService.signup(data)
        
        assert result[1] == 400
