# Ping prometheus to keep alive
from src.config import BackendConfig
import urllib.request
from datetime import date, datetime


   
async def ping_ds(): 
    print(f"Pinging DS at {BackendConfig.SINE_TRADE_DS_URL} - {datetime.now()}")
    try:
        urllib.request.urlopen(
            
            f'{BackendConfig.SINE_TRADE_DS_URL}/health'
        )

    
    except Exception as e:
        print(f"Error pinging DS: {e}")
    
    print(f"Successfully pinged DS at {BackendConfig.SINE_TRADE_DS_URL}")
   
   