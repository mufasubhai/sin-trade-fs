import pytest
from unittest.mock import MagicMock, patch
import pika


class TestDSConfig:
    def test_config_port_default(self):
        from src.config import DSConfig
        assert DSConfig.PORT == "5004"

    def test_get_connection_success(self, mock_pika_connection):
        from src.config import DSConfig
        mock_conn, mock_channel = mock_pika_connection
        result = DSConfig.get_connection()
        assert result is not None

    def test_get_connection_failure(self):
        from src.config import DSConfig
        with patch.object(DSConfig, 'params', side_effect=Exception("Connection failed")):
            result = DSConfig.get_connection()
            assert result is None
