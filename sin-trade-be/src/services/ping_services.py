# Ping prometheus to keep alive
from src.config import BackendConfig
import urllib.request
from datetime import date, datetime


   
async def ping_ds(): 
    print(f"Pinging DS at {BackendConfig.SIN_TRADE_DS_HOST} - {datetime.now()}")
    try:
        urllib.request.urlopen(
            
            f'{BackendConfig.SIN_TRADE_DS_HOST}/health'
        )

    
    except Exception as e:
        print(f"Error pinging DS: {e}")
    
    print(f"Successfully pinged DS at {BackendConfig.SIN_TRADE_DS_HOST}")
   
   