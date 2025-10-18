import os
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from src.services.amqp_ds_publisher import publish_message


def tick():
    print(f"Tick! The time is: {datetime.now()} Publishing message to email queue")
    publish_message("email_queue", f"Email queue message {datetime.now()}")
