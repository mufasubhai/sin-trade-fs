# Ping prometheus to keep alive
from src.config import DSConfig
import urllib.request
from datetime import date, datetime

async def ping_prometheus(): 
    print(f"Pinging Prometheus at {DSConfig.SINE_TRADE_PROMETHEUS_URL} - {datetime.now()}")
    try:
        urllib.request.urlopen(
            DSConfig.SINE_TRADE_PROMETHEUS_URL
        )

    
    except Exception as e:
        print(f"Error pinging Prometheus: {e}")
    
    print(f"Successfully pinged Prometheus at {DSConfig.SINE_TRADE_PROMETHEUS_URL}")
   
   