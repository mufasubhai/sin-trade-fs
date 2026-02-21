
from datetime import datetime
import asyncio



from src.services.alphavantage_services import fetch_history_for_asset
from src.services.kraken_services import run_history_flow
from src.services.prometheus_services import ping_prometheus


## here are the functions for scheduled jobs
async def check_history():
    history_response = None
    
    try:    
        history_response = await fetch_history_for_asset()
       
        if history_response[1] != 200:
            print(f"Error in history response: {history_response[0]}")
    except Exception as e:
        print(f"Error fetching history: {e}")
    

async def run_ml_models():
    print(f"Running ML models at {datetime.now()}")
    # Placeholder for ML model execution logic
    # e.g., load models, run predictions, store results, etc.



def check_targets():
    
    print (f"Checking targets at {datetime.now()}")
    
    async def process_targets():
        print(f"processing targets at {datetime.now()}")
        
        try:
            history_flow_response = await run_history_flow()
        except Exception as e:
            # email log this error maybe?
            print(f"Error running history flow: {e}")  
            
        print('fetch active assets with targets')
        print('perform calculations on targets')
        print('send email notifications if targets are met')
        
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, use run_coroutine_threadsafe
            asyncio.run_coroutine_threadsafe(process_targets(), loop)
        else:
            loop.run_until_complete(process_targets())
    except RuntimeError:
        # No event loop, create a new one
        asyncio.run(process_targets())
        

def keep_prometheus_alive():
    print (f"Pinging Prometheus {datetime.now()}")
    
    async def process_prometheus_ping():
        print(f"processing targets at {datetime.now()}")
        
        try:
            history_flow_response = await ping_prometheus()
        except Exception as e:
            # email log this error maybe?
            print(f"Error running history flow: {e}")  
            
        print('fetch active assets with targets')
        print('perform calculations on targets')
        print('send email notifications if targets are met')
        
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, use run_coroutine_threadsafe
            asyncio.run_coroutine_threadsafe(process_prometheus_ping(), loop)
        else:
            loop.run_until_complete(process_prometheus_ping())
    except RuntimeError:
        # No event loop, create a new one
        asyncio.run(process_prometheus_ping())