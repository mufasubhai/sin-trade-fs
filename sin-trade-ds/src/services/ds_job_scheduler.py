
from datetime import datetime
import asyncio
import json



from src.services.alphavantage_services import fetch_history_for_asset
from src.services.kraken_services import run_history_flow
from src.services.prometheus_services import ping_prometheus
from src.services.ml_trading_service import run_ml_trading_analysis
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


def run_ml_trading_cron():
    print(f"Running ML trading cron at {datetime.now()}")
    
    async def process_ml_trading():
        print(f"Processing ML trading signals at {datetime.now()}")
        
        try:
            users_with_signals = await run_ml_trading_analysis()
            
            if users_with_signals:
                for user_data in users_with_signals:
                    message = {
                        "user_id": user_data["user_id"],
                        "email": user_data["email"],
                        "signals": user_data["signals"],
                    }
                    publish_message("email_queue", json.dumps(message))
                    print(f"Queued email notification for user {user_data['user_id']}")
            else:
                print("No users with active signals to notify")
                
        except Exception as e:
            print(f"Error in ML trading cron: {e}")
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(process_ml_trading(), loop)
        else:
            loop.run_until_complete(process_ml_trading())
    except RuntimeError:
        asyncio.run(process_ml_trading())


def compute_ticker_stats():
    print(f"Computing ticker stats at {datetime.now()}")
    try:
        from src.config import DSConfig
        DSConfig.supabase.rpc("compute_ticker_stats").execute()
        print("Ticker stats computed successfully")
    except Exception as e:
        print(f"Error computing ticker stats: {e}")