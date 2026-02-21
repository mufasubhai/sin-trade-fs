import pytest
from unittest.mock import MagicMock, patch
import asyncio


class TestAlphavantageServices:
    @patch('src.services.alphavantage_services.requests.get')
    @patch('src.services.alphavantage_services.write_history_to_db')
    def test_fetch_history_for_asset_crypto(self, mock_write, mock_get):
        from src.services.alphavantage_services import fetch_history_for_asset
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Meta Data": {
                "3. Digital Currency Name": "Bitcoin",
                "4. Market Code": "USD"
            },
            "Time Series (Daily)": {}
        }
        mock_get.return_value = mock_response
        mock_write.return_value = ({"message": "success"}, 200)
        
        result = asyncio.run(fetch_history_for_asset("BTC", True))
        
        assert result is not None

    @patch('src.services.alphavantage_services.requests.get')
    @patch('src.services.alphavantage_services.write_history_to_db')
    def test_fetch_history_for_asset_stock(self, mock_write, mock_get):
        from src.services.alphavantage_services import fetch_history_for_asset
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Meta Data": {},
            "Time Series (Daily)": {}
        }
        mock_get.return_value = mock_response
        mock_write.return_value = ({"message": "success"}, 200)
        
        result = asyncio.run(fetch_history_for_asset("AAPL", False))
        
        assert result is not None

    @patch('src.services.alphavantage_services.requests.get')
    def test_fetch_history_http_error(self, mock_get):
        from src.services.alphavantage_services import fetch_history_for_asset
        import requests
        
        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.HTTPError("404")
        mock_get.return_value = mock_response
        
        result = asyncio.run(fetch_history_for_asset("BTC", True))
        
        assert result[1] == 500

    @patch('src.services.alphavantage_services.requests.get')
    def test_fetch_history_general_error(self, mock_get):
        from src.services.alphavantage_services import fetch_history_for_asset
        
        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("Network error")
        mock_get.return_value = mock_response
        
        result = asyncio.run(fetch_history_for_asset("BTC", True))
        
        assert result[1] == 500

    @patch('src.services.alphavantage_services.DSConfig.supabase')
    def test_write_history_to_db_crypto(self, mock_supabase):
        from src.services.alphavantage_services import write_history_to_db
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value.execute.return_value = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        mock_table.update.return_value.eq.return_value.execute.return_value = MagicMock()
        
        history_data = {
            "Meta Data": {
                "3. Digital Currency Name": "Bitcoin",
                "4. Market Code": "USD",
                "4. Market Name": "Dollar"
            },
            "Time Series (Daily)": {
                "2024-01-01": {
                    "1. open": "100.0",
                    "2. high": "110.0",
                    "3. low": "90.0",
                    "4. close": "105.0",
                    "5. volume": "1000"
                }
            }
        }
        
        result = asyncio.run(write_history_to_db("BTC", history_data, True))
        
        assert result[1] == 200

    @patch('src.services.alphavantage_services.DSConfig.supabase')
    def test_write_history_to_db_stock(self, mock_supabase):
        from src.services.alphavantage_services import write_history_to_db
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        
        history_data = {
            "Meta Data": {},
            "Time Series (Daily)": {
                "2024-01-01": {
                    "1. open": "100.0",
                    "2. high": "110.0",
                    "3. low": "90.0",
                    "4. close": "105.0",
                    "5. volume": "1000"
                }
            }
        }
        
        result = asyncio.run(write_history_to_db("AAPL", history_data, False))
        
        assert result is None
