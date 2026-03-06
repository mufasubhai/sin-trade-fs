# Ping prometheus to keep alive
from src.config import DSConfig
import urllib.request
from datetime import date, datetime

async def ping_prometheus(): 
    print(f"Pinging Prometheus at {DSConfig.SINE_TRADE_PROMETHEUS_URL} - {datetime.now()}")
    try:
        urllib.request.urlopen(
            f'{DSConfig.SINE_TRADE_PROMETHEUS_URL}/health'
        )

    
    except Exception as e:
        print(f"Error pinging Prometheus: {e}")
    
    print(f"Successfully pinged Prometheus at {DSConfig.SINE_TRADE_PROMETHEUS_URL}")
   
   
async def ping_backend(): 
    print(f"Pinging Backend at {DSConfig.SIN_TRADE_BA} - {datetime.now()}")
    try:
        urllib.request.urlopen(
            DSConfig.SIN_TRADE_BA
        )

    
    except Exception as e:
        print(f"Error pinging Backend: {e}")
    
    print(f"Successfully pinged Backend at {DSConfig.SIN_TRADE_BA}")
   
   