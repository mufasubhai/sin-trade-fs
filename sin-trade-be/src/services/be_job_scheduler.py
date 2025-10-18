import os
from datetime import datetime
from src.services.amqp_be_publisher import publish_message

from apscheduler.schedulers.blocking import BlockingScheduler


def tick():
    print(f"Tick! The time is: {datetime.now()} Publishing message to all queues")
    print("Publishing message to crypto queue")
    publish_message("crypto_queue", f"Crypto queue message {datetime.now()}")
    print("Publishing message to stock queue")
    publish_message("stock_queue", f"Stock queue message {datetime.now()}")
    print("Publishing message to refresh queue")
    publish_message("refresh_queue", f"Refresh queue message {datetime.now()}")
