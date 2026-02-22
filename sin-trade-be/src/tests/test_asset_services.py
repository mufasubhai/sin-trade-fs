import pytest
from unittest.mock import MagicMock, patch


class TestAssetServices:
    @patch('src.services.asset_services.publish_message')
    @patch('src.services.asset_services.BackendConfig.supabase')
    def test_add_asset_crypto_new(self, mock_supabase, mock_publish):
        from src.services.asset_services import AssetService
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
        mock_table.insert.return_value.execute.return_value = MagicMock(data=[{"id": 1, "initial_fetch_complete": False}])
        
        data = {
            "ticker_code": "BTC",
            "is_crypto": True,
            "user_id": "user123"
        }
        
        result = AssetService.addAsset(data)
        
        assert result[1] == 200

    @patch('src.services.asset_services.publish_message')
    @patch('src.services.asset_services.BackendConfig.supabase')
    def test_add_asset_non_crypto(self, mock_supabase, mock_publish):
        from src.services.asset_services import AssetService
        
        data = {
            "ticker_code": "AAPL",
            "is_crypto": False,
            "user_id": "user123"
        }
        
        result = AssetService.addAsset(data)
        
        assert result[1] == 400
        assert "Only crypto" in result[0]["message"]

    @patch('src.services.asset_services.publish_message')
    @patch('src.services.asset_services.BackendConfig.supabase')
    def test_add_asset_unsupported(self, mock_supabase, mock_publish):
        from src.services.asset_services import AssetService
        
        data = {
            "ticker_code": "UNSUPPORTED",
            "is_crypto": True,
            "user_id": "user123"
        }
        
        result = AssetService.addAsset(data)
        
        assert result[1] == 400
        assert "not supported" in result[0]["message"]

    @patch('src.services.asset_services.publish_message')
    @patch('src.services.asset_services.BackendConfig.supabase')
    def test_add_asset_user_already_has(self, mock_supabase, mock_publish):
        from src.services.asset_services import AssetService
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        
        data = {
            "ticker_code": "BTC",
            "is_crypto": True,
            "user_id": "user123"
        }
        
        result = AssetService.addAsset(data)
        
        assert result[1] == 500

    @patch('src.services.asset_services.BackendConfig.supabase')
    def test_get_active_assets_by_user_id_success(self, mock_supabase):
        from src.services.asset_services import AssetService
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        
        result = AssetService.getActiveAssetsByUserId("user123")
        
        assert result[1] == 200

    @patch('src.services.asset_services.BackendConfig.supabase')
    def test_get_active_assets_by_user_id_error(self, mock_supabase):
        from src.services.asset_services import AssetService
        
        mock_supabase.table.side_effect = Exception("DB Error")
        
        result = AssetService.getActiveAssetsByUserId("user123")
        
        assert result[1] == 401

    @patch('src.services.asset_services.BackendConfig.supabase')
    def test_delete_user_asset_success(self, mock_supabase):
        from src.services.asset_services import AssetService
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.delete.return_value.eq.return_value.execute.return_value = MagicMock()
        
        result = AssetService.deleteUserAsset(1, "user123")
        
        assert result[1] == 200

    def test_add_asset_no_db(self):
        from src.services.asset_services import AssetService
        
        with patch('src.services.asset_services.BackendConfig') as mock_config:
            mock_config.supabase = None
            
            data = {
                "ticker_code": "BTC",
                "is_crypto": True,
                "user_id": "user123"
            }
            
            result = AssetService.addAsset(data)
            
            assert result[1] == 500
