import pika, os

# importing the config with easy access to env variables.
from src.config import BackendConfig


def declare_queues():
    connection = BackendConfig.get_connection()
    if not connection:
        return None

    try:
        channel = connection.channel()
        channel.queue_declare(queue="crypto_queue")
        channel.queue_declare(queue="stock_queue")
        return channel
    finally:
        if connection and not connection.is_closed:
            connection.close()


def publish_message(channel_name, message, exchange=""):
    connection = BackendConfig.get_connection()
    if not connection:
        return
    try:
        channel = connection.channel()
        channel.basic_publish(exchange=exchange, routing_key=channel_name, body=message)
    finally:
        if connection and not connection.is_closed:
            connection.close()
