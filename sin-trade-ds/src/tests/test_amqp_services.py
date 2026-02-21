import pytest
from unittest.mock import MagicMock, patch


class TestAMQPDSPublisher:
    @patch('src.services.amqp_ds_publisher.DSConfig.get_connection')
    def test_declare_queues_success(self, mock_get_conn):
        from src.services.amqp_ds_publisher import declare_queues
        
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_connection.channel.return_value = mock_channel
        mock_get_conn.return_value = mock_connection
        
        result = declare_queues()
        
        assert result is not None
        mock_channel.queue_declare.assert_called_once_with(queue="email_queue")

    @patch('src.services.amqp_ds_publisher.DSConfig.get_connection')
    def test_declare_queues_no_connection(self, mock_get_conn):
        from src.services.amqp_ds_publisher import declare_queues
        
        mock_get_conn.return_value = None
        
        result = declare_queues()
        
        assert result is None

    @patch('src.services.amqp_ds_publisher.DSConfig.get_connection')
    def test_publish_message_success(self, mock_get_conn):
        from src.services.amqp_ds_publisher import publish_message
        
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_connection.channel.return_value = mock_channel
        mock_get_conn.return_value = mock_connection
        
        publish_message("test_queue", "test_message")
        
        mock_channel.basic_publish.assert_called_once()

    @patch('src.services.amqp_ds_publisher.DSConfig.get_connection')
    def test_publish_message_no_connection(self, mock_get_conn):
        from src.services.amqp_ds_publisher import publish_message
        
        mock_get_conn.return_value = None
        
        publish_message("test_queue", "test_message")


class TestAMQPDSSubscriber:
    @patch('src.services.amqp_ds_subscriber.DSConfig.get_connection')
    def test_stock_callback(self, mock_get_conn):
        from src.services.amqp_ds_subscriber import stock_callback
        
        mock_ch = MagicMock()
        mock_method = MagicMock()
        mock_properties = MagicMock()
        
        stock_callback(mock_ch, mock_method, mock_properties, b"BTC")

    @patch('src.services.amqp_ds_subscriber.DSConfig.get_connection')
    @patch('src.services.amqp_ds_subscriber.fetch_history_for_asset')
    def test_crypto_callback(self, mock_fetch, mock_get_conn):
        from src.services.amqp_ds_subscriber import crypto_callback
        
        mock_ch = MagicMock()
        mock_method = MagicMock()
        mock_properties = MagicMock()
        mock_fetch.return_value = ({"message": "success"}, 200)
        
        crypto_callback(mock_ch, mock_method, mock_properties, b"BTC")

    @patch('src.services.amqp_ds_subscriber.DSConfig.get_connection')
    @patch('src.services.amqp_ds_subscriber.fetch_history_for_asset')
    def test_crypto_callback_error(self, mock_fetch, mock_get_conn):
        from src.services.amqp_ds_subscriber import crypto_callback
        
        mock_ch = MagicMock()
        mock_method = MagicMock()
        mock_properties = MagicMock()
        mock_fetch.side_effect = Exception("Error")
        
        crypto_callback(mock_ch, mock_method, mock_properties, b"BTC")

    @patch('src.services.amqp_ds_subscriber._consume_queue')
    @patch('src.services.amqp_ds_subscriber.threading.Thread')
    def test_subscribe_to_queues(self, mock_thread, mock_consume):
        from src.services.amqp_ds_subscriber import subscribe_to_queues
        
        subscribe_to_queues()
        
        assert mock_thread.call_count == 2
