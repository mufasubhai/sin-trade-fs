import pytest
import os
import sys
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    
    with app.app_context():
        yield app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def mock_supabase():
    with patch('src.config.BackendConfig.supabase') as mock:
        mock.table.return_value.select.return_value.execute.return_value = MagicMock(data=[])
        yield mock


@pytest.fixture
def mock_pika_connection():
    with patch('src.config.BackendConfig.get_connection') as mock_conn:
        mock_connection = MagicMock()
        mock_connection.is_closed = False
        mock_channel = MagicMock()
        mock_connection.channel.return_value = mock_channel
        mock_conn.return_value = mock_connection
        yield mock_connection, mock_channel
