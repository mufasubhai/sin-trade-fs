# import pika, os
import asyncio
import threading
from src.services.alphavantage_services import fetch_history_for_asset

# importing the config with easy access to env variables.
from src.config import DSConfig

def stock_callback(ch, method, properties, body):
    print(f"Received stock message: {body}")

def crypto_callback(ch, method, properties, body):
    ## need to addd logic to process the crypto message
    print(f"Received crypto message: {body}")
    
    async def process_message():
        try:
            await fetch_history_for_asset(body.decode(), True)
        except Exception as e:
            print(f"Error processing crypto message {body}: {e}")
            ## schedule for retry here. 
             # Run the async code in the event loop
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, use run_coroutine_threadsafe
            asyncio.run_coroutine_threadsafe(process_message(), loop)
        else:
            loop.run_until_complete(process_message())
    except RuntimeError:
        # No event loop, create a new one
        asyncio.run(process_message())


def _consume_queue(queue_name, callback):
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
        target=_consume_queue, args=("crypto_queue", crypto_callback), daemon=True
    )
    
    stock_thread = threading.Thread(
        target=_consume_queue, args=("stock_queue", stock_callback), daemon=True
    )

    crypto_thread.start()
    stock_thread.start()

    print("Started AMQP DS subscriber threads")