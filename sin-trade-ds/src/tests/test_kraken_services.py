import pytest
from unittest.mock import MagicMock, patch


class TestKrakenServices:
    @patch('src.services.kraken_services.urllib.request.urlopen')
    def test_request_get(self, mock_urlopen):
        from src.services.kraken_services import request
        
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"result": {"success": true}}'
        mock_urlopen.return_value = mock_response
        
        result = request(
            method="GET",
            path="/0/public/Ticker",
            environment="https://api.kraken.com"
        )
        
        assert result is not None
        mock_urlopen.assert_called_once()

    @patch('src.services.kraken_services.urllib.request.urlopen')
    def test_request_with_path_params(self, mock_urlopen):
        from src.services.kraken_services import request
        
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"result": {}}'
        mock_urlopen.return_value = mock_response
        
        result = request(
            method="GET",
            path="/0/public/Ticker?pair=BTCUSD",
            environment="https://api.kraken.com"
        )
        
        assert result is not None

    @patch('src.services.kraken_services.urllib.request.urlopen')
    @patch('src.services.kraken_services.DSConfig.supabase')
    def test_run_history_flow_no_assets(self, mock_supabase, mock_urlopen):
        from src.services.kraken_services import run_history_flow
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
        
        import asyncio
        result = asyncio.run(run_history_flow())
        
        assert result is None
