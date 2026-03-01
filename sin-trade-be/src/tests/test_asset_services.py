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

    @patch('src.services.asset_services.BackendConfig.supabase_service')
    def test_get_asset_history_kraken_data(self, mock_supabase):
        from src.services.asset_services import AssetService

        kraken_row = {
            "from_asset_code": "BTC",
            "date": "2026-02-14",
            "price_time": "2026-02-14T10:00:00",
            "current_price": 50000.0,
        }
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.gte.return_value.order.return_value.execute.return_value = MagicMock(data=[kraken_row])

        result, status = AssetService.getAssetHistory("BTC")

        assert status == 200
        assert len(result["data"]) == 1
        assert result["data"][0]["interval"] == "5min"
        assert result["data"][0]["price_time"] == "2026-02-14T10:00:00"

    @patch('src.services.asset_services.BackendConfig.supabase_service')
    def test_get_asset_history_alphavantage_data(self, mock_supabase):
        from src.services.asset_services import AssetService

        av_row = {
            "from_asset_code": "BTC",
            "date": "2026-02-14",
            "price_time": None,
            "current_price": 50000.0,
        }
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.gte.return_value.order.return_value.execute.return_value = MagicMock(data=[av_row])

        result, status = AssetService.getAssetHistory("BTC")

        assert status == 200
        assert len(result["data"]) == 288
        assert all(r["interval"] == "daily_expanded" for r in result["data"])
        assert result["data"][0]["price_time"] == "2026-02-14T00:00:00"
        assert result["data"][1]["price_time"] == "2026-02-14T00:05:00"
        assert result["data"][287]["price_time"] == "2026-02-14T23:55:00"

    @patch('src.services.asset_services.BackendConfig.supabase_service')
    def test_get_asset_history_mixed_data(self, mock_supabase):
        from src.services.asset_services import AssetService

        av_row = {
            "from_asset_code": "BTC",
            "date": "2026-02-14",
            "price_time": None,
            "current_price": 50000.0,
        }
        kraken_row = {
            "from_asset_code": "BTC",
            "date": "2026-02-15",
            "price_time": "2026-02-15T00:00:00",
            "current_price": 51000.0,
        }
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.gte.return_value.order.return_value.execute.return_value = MagicMock(data=[av_row, kraken_row])

        result, status = AssetService.getAssetHistory("BTC")

        assert status == 200
        assert len(result["data"]) == 289  # 288 expanded + 1 kraken
        # Verify sorted by price_time
        times = [r["price_time"] for r in result["data"]]
        assert times == sorted(times)
        # Kraken row should be last
        assert result["data"][-1]["interval"] == "5min"
        assert result["data"][-1]["current_price"] == 51000.0

    def test_get_asset_history_no_db(self):
        from src.services.asset_services import AssetService

        with patch('src.services.asset_services.BackendConfig') as mock_config:
            mock_config.supabase_service = None

            result, status = AssetService.getAssetHistory("BTC")

            assert status == 500
            assert "Database connection unsuccessful" in result["message"]

    @patch('src.services.asset_services.BackendConfig.supabase_service')
    def test_get_asset_history_db_error(self, mock_supabase):
        from src.services.asset_services import AssetService

        mock_supabase.table.side_effect = Exception("DB connection failed")

        result, status = AssetService.getAssetHistory("BTC")

        assert status == 500
        assert "DB connection failed" in result["message"]
