from datetime import datetime
from src.services.amqp_be_publisher import publish_message


def tick():
    print(f"Tick! The time is: {datetime.now()} Publishing message to all queues")
