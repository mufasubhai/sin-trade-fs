import pika, os
import threading
import json

# importing the config with easy access to env variables.
from src.config import BackendConfig
from src.services.email_service import EmailService


def callback(ch, method, properties, body):
    print(f"Received message: {body}")
    
    try:
        message_data = json.loads(body)
        
        user_id = message_data.get("user_id")
        email = message_data.get("email")
        signals = message_data.get("signals", [])
        
        if user_id and email and signals:
            success = EmailService.send_trade_signal_alert(
                user_email=email,
                user_id=user_id,
                signals=signals
            )
            
            if success:
                print(f"Successfully processed email alert for user {user_id}")
            else:
                print(f"Failed to process email alert for user {user_id}")
        else:
            print(f"Invalid message format: {message_data}")
            
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")


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
