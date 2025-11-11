import os
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from src.services.amqp_ds_publisher import publish_message

def check_history():
    print(f"Checking history for {datetime.now()}")
    print('fech active assets')
    print('iterate through assets and check history')


def check_targets():
    print(f"Checking targets at {datetime.now()}")
    print('fetch active assets with targets')
    print('perform calculations on targets')
    print('send email notifications if targets are met')