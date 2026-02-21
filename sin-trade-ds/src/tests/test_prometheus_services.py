import pytest
from unittest.mock import patch, MagicMock
import asyncio


class TestPrometheusServices:
    @patch('src.services.prometheus_services.urllib.request.urlopen')
    @patch('src.services.prometheus_services.DSConfig')
    def test_ping_prometheus_success(self, mock_config, mock_urlopen):
        from src.services.prometheus_services import ping_prometheus
        
        mock_config.SINE_TRADE_PROMETHEUS_URL = "http://prometheus:9090/-/healthy"
        
        asyncio.run(ping_prometheus())
        
        mock_urlopen.assert_called_once()

    @patch('src.services.prometheus_services.urllib.request.urlopen')
    @patch('src.services.prometheus_services.DSConfig')
    def test_ping_prometheus_error(self, mock_config, mock_urlopen):
        from src.services.prometheus_services import ping_prometheus
        
        mock_config.SINE_TRADE_PROMETHEUS_URL = "http://prometheus:9090/-/healthy"
        mock_urlopen.side_effect = Exception("Connection failed")
        
        asyncio.run(ping_prometheus())
        
        mock_urlopen.assert_called_once()

    @patch('src.services.prometheus_services.urllib.request.urlopen')
    @patch('src.services.prometheus_services.DSConfig')
    def test_ping_prometheus_empty_url(self, mock_config, mock_urlopen):
        from src.services.prometheus_services import ping_prometheus
        
        mock_config.SINE_TRADE_PROMETHEUS_URL = ""
        
        asyncio.run(ping_prometheus())
        
        mock_urlopen.assert_called_once_with("")
