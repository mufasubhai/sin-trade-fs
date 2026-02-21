import pytest
from unittest.mock import MagicMock, patch


class TestAssetServices:
    @patch('src.services.asset_services.DSConfig.supabase')
    def test_add_asset_new(self, mock_supabase):
        from src.services.asset_services import AssetRefreshService
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
        mock_table.insert.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        
        data = {
            "ticker_code": "BTC",
            "is_crypto": True,
            "user_id": "user123"
        }
        
        result = AssetRefreshService.addAsset(data)
        
        assert result[1] == 200

    @patch('src.services.asset_services.DSConfig.supabase')
    def test_add_asset_already_exists(self, mock_supabase):
        from src.services.asset_services import AssetRefreshService
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        
        data = {
            "ticker_code": "BTC",
            "is_crypto": True,
            "user_id": "user123"
        }
        
        result = AssetRefreshService.addAsset(data)
        
        assert result[1] == 500

    @patch('src.services.asset_services.DSConfig.supabase')
    def test_add_asset_user_already_has(self, mock_supabase):
        from src.services.asset_services import AssetRefreshService
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        
        data = {
            "ticker_code": "BTC",
            "is_crypto": True,
            "user_id": "user123"
        }
        
        result = AssetRefreshService.addAsset(data)
        
        assert result[1] == 500

    @patch('src.services.asset_services.DSConfig.supabase')
    def test_add_asset_db_error(self, mock_supabase):
        from src.services.asset_services import AssetRefreshService
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.side_effect = Exception("DB Error")
        
        data = {
            "ticker_code": "BTC",
            "is_crypto": True,
            "user_id": "user123"
        }
        
        result = AssetRefreshService.addAsset(data)
        
        assert result[1] == 401

    @patch('src.services.asset_services.DSConfig.supabase')
    def test_get_active_assets_by_user_id_success(self, mock_supabase):
        from src.services.asset_services import AssetRefreshService
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        
        result = AssetRefreshService.getActiveAssetsByUserId("user123")
        
        assert result[1] == 200
        assert "data" in result[0]

    @patch('src.services.asset_services.DSConfig.supabase')
    def test_get_active_assets_by_user_id_error(self, mock_supabase):
        from src.services.asset_services import AssetRefreshService
        
        mock_supabase.table.side_effect = Exception("DB Error")
        
        result = AssetRefreshService.getActiveAssetsByUserId("user123")
        
        assert result[1] == 401

    def test_add_asset_no_db(self):
        from src.services.asset_services import AssetRefreshService
        
        with patch('src.services.asset_services.DSConfig') as mock_config:
            mock_config.supabase = None
            
            data = {
                "ticker_code": "BTC",
                "is_crypto": True,
                "user_id": "user123"
            }
            
            result = AssetRefreshService.addAsset(data)
            
            assert result[1] == 500

    def test_get_active_assets_no_db(self):
        from src.services.asset_services import AssetRefreshService
        
        with patch('src.services.asset_services.DSConfig') as mock_config:
            mock_config.supabase = None
            
            result = AssetRefreshService.getActiveAssetsByUserId("user123")
            
            assert result[1] == 500
