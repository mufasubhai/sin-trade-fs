import pika, os

# importing the config with easy access to env variables.
from src.config import DSConfig


def declare_queues():
    connection = DSConfig.get_connection()
    if not connection:
        return None

    try:
        channel = connection.channel()
        channel.queue_declare(queue="email_queue")
        return channel
    finally:
        if connection and not connection.is_closed:
            connection.close()


def publish_message(channel_name, message, exchange=""):
    connection = DSConfig.get_connection()
    if not connection:
        return

    try:
        channel = connection.channel()
        channel.basic_publish(exchange=exchange, routing_key=channel_name, body=message)
    finally:
        if connection and not connection.is_closed:
            connection.close()
            


