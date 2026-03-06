
from datetime import datetime
import asyncio
import json

from src.services.ping_services import ping_ds

def keep_ds_alive():
    print (f"Pinging Backend {datetime.now()}")
    
    async def process_ds_ping():
        print(f"processing backend at {datetime.now()}")
        
        try:
            backend_response = await ping_ds()
        except Exception as e:
            # email log this error maybe?
            print(f"Error running backend ping: {e}")  
            
        print('fetch active assets with targets')
        print('perform calculations on targets')
        print('send email notifications if targets are met')
        
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, use run_coroutine_threadsafe
            asyncio.run_coroutine_threadsafe(process_ds_ping(), loop)
        else:
            loop.run_until_complete(process_ds_ping())
    except RuntimeError:
        # No event loop, create a new one
        asyncio.run(process_ds_ping())

