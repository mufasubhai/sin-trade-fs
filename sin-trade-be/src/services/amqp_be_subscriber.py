import pika, os
import threading

# importing the config with easy access to env variables.
from src.config import BackendConfig


def callback(ch, method, properties, body):
    print(f"Received message: {body}")


def _consume_queue(queue_name):
    """Consume messages from a {queue_name} in a separate thread"""
    connection = BackendConfig.get_connection()
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
    # Subscribe to email queue from DS service
    email_thread = threading.Thread(
        target=_consume_queue, args=("email_queue",), daemon=True
    )
    email_thread.start()
    print("Started AMQP subscriber threads")
