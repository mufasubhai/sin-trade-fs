import pytest
from unittest.mock import patch, MagicMock
import asyncio


class TestPingServices:
    @patch('src.services.ping_services.urllib.request.urlopen')
    @patch('src.services.ping_services.DSConfig')
    def test_ping_backend_success(self, mock_config, mock_urlopen):
        from src.services.ping_services import ping_backend
        
        mock_config.SIN_TRADE_BE_HOST = "http://backend:5002"
        
        asyncio.run(ping_backend())
        
        mock_urlopen.assert_called_once()

    @patch('src.services.ping_services.urllib.request.urlopen')
    @patch('src.services.ping_services.DSConfig')
    def test_ping_backend_error(self, mock_config, mock_urlopen):
        from src.services.ping_services import ping_backend
        
        mock_config.SIN_TRADE_BE_HOST = "http://backend:5002"
        mock_urlopen.side_effect = Exception("Connection failed")
        
        asyncio.run(ping_backend())
        
        mock_urlopen.assert_called_once()

    @patch('src.services.ping_services.urllib.request.urlopen')
    @patch('src.services.ping_services.DSConfig')
    def test_ping_backend_empty_host(self, mock_config, mock_urlopen):
        from src.services.ping_services import ping_backend
        
        mock_config.SIN_TRADE_BE_HOST = ""
        
        asyncio.run(ping_backend())
        
        mock_urlopen.assert_called_once()
