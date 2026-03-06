import pytest
from unittest.mock import patch, MagicMock
import asyncio


class TestPingServices:
    @patch('src.services.ping_services.urllib.request.urlopen')
    @patch('src.services.ping_services.BackendConfig')
    def test_ping_ds_success(self, mock_config, mock_urlopen):
        from src.services.ping_services import ping_ds
        
        mock_config.SIN_TRADE_DS_HOST = "http://ds:5004"
        
        asyncio.run(ping_ds())
        
        mock_urlopen.assert_called_once()

    @patch('src.services.ping_services.urllib.request.urlopen')
    @patch('src.services.ping_services.BackendConfig')
    def test_ping_ds_error(self, mock_config, mock_urlopen):
        from src.services.ping_services import ping_ds
        
        mock_config.SIN_TRADE_DS_HOST = "http://ds:5004"
        mock_urlopen.side_effect = Exception("Connection failed")
        
        asyncio.run(ping_ds())
        
        mock_urlopen.assert_called_once()

    @patch('src.services.ping_services.urllib.request.urlopen')
    @patch('src.services.ping_services.BackendConfig')
    def test_ping_ds_empty_host(self, mock_config, mock_urlopen):
        from src.services.ping_services import ping_ds
        
        mock_config.SIN_TRADE_DS_HOST = ""
        
        asyncio.run(ping_ds())
        
        mock_urlopen.assert_called_once()
