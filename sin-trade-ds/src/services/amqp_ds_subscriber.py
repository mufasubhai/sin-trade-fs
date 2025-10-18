import pika, os
import threading
import logging

# importing the config with easy access to env variables.
from src.config import DSConfig


def callback(ch, method, properties, body):
    print(f"Received message: {body}")


def _consume_queue(queue_name):
    f"""Consume messages from a {queue_name} in a separate thread"""
    connection = DSConfig.get_connection()
    if not connection:
        return

    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True,
        )
        print(f"Starting consumer for queue: {queue_name}")
        channel.start_consuming()
    except Exception as e:
        print(f"Error consuming from queue {queue_name}: {e}")
    finally:
        if connection and not connection.is_closed:
            connection.close()


def subscribe_to_queues():
    """Start consuming from queues in background threads"""
    # Subscribe to queues from BE service
    crypto_thread = threading.Thread(
        target=_consume_queue, args=("crypto_queue",), daemon=True
    )
    stock_thread = threading.Thread(
        target=_consume_queue, args=("stock_queue",), daemon=True
    )
    refresh_thread = threading.Thread(
        target=_consume_queue, args=("refresh_queue",), daemon=True
    )

    crypto_thread.start()
    stock_thread.start()
    refresh_thread.start()

    print("Started AMQP DS subscriber threads")
