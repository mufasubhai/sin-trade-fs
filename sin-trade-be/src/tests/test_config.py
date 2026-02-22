import pytest
from unittest.mock import MagicMock, patch


class TestBackendConfig:
    def test_config_port_default(self):
        from src.config import BackendConfig
        assert BackendConfig.PORT == "5002"

    def test_get_connection_success(self, mock_pika_connection):
        from src.config import BackendConfig
        mock_conn, mock_channel = mock_pika_connection
        result = BackendConfig.get_connection()
        assert result is not None

    def test_get_connection_failure(self):
        from src.config import BackendConfig
        with patch.object(BackendConfig, 'params', side_effect=Exception("Connection failed")):
            result = BackendConfig.get_connection()
            assert result is None
