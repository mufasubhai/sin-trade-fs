import os
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from src.services.alphavantage_services import fetch_history_for_asset
from src.services.amqp_ds_publisher import publish_message


## here are the functions for scheduled jobs
async def check_history():
    history_response = None
    
    try:    
        history_response = await fetch_history_for_asset()
       
        if history_response[1] != 200:
            print(f"Error in history response: {history_response[0]}")
    except Exception as e:
        print(f"Error fetching history: {e}")
    


def check_targets():
    
    print(f"Checking targets at {datetime.now()}")
    print('fetch active assets with targets')
    print('perform calculations on targets')
    print('send email notifications if targets are met')