# Retrieve ticker data across all markets.
# Endpoint does not require authentication,
# but has utility functions for authentication.
from src.config import DSConfig

import http.client
import urllib.request
import urllib.parse
import hashlib
import hmac
import base64
import json
import time
from datetime import date, datetime


def request(method: str = "GET", path: str = "", query: dict | None = None, body: dict | None = None, public_key: str = "", private_key: str = "", environment: str = "") -> http.client.HTTPResponse:
   url = environment + path
   query_str = ""
   if query is not None and len(query) > 0:
      query_str = urllib.parse.urlencode(query)
      url += "?" + query_str
   nonce = ""
   if len(public_key) > 0:
      if body is None:
         body = {}
      nonce = body.get("nonce")
      if nonce is None:
         nonce = get_nonce()
         body["nonce"] = nonce
   headers = {}
   body_str = ""
   if body is not None and len(body) > 0:
      body_str = json.dumps(body)
      headers["Content-Type"] = "application/json"
   if len(public_key) > 0:
      headers["API-Key"] = public_key
      headers["API-Sign"] = get_signature(private_key, query_str+body_str, nonce, path)
   req = urllib.request.Request(
      method=method,
      url=url,
      data=body_str.encode(),
      headers=headers,
   )
   return urllib.request.urlopen(req)

def get_nonce() -> str:
   return str(int(time.time() * 1000))

def get_signature(private_key: str, data: str, nonce: str, path: str) -> str:
   return sign(
      private_key=private_key,
      message=path.encode() + hashlib.sha256(
            (nonce + data)
         .encode()
      ).digest()
   )

def sign(private_key: str, message: bytes) -> str:
   return base64.b64encode(
      hmac.new(
         key=base64.b64decode(private_key),
         msg=message,
         digestmod=hashlib.sha512,
      ).digest()
   ).decode()


async def run_history_flow(): 
   history_list = None
   try: 
      history_list =  DSConfig.supabase.table('active_assets').select('*').eq('initial_fetch_complete', True).execute()
   except Exception as e:
      return {"message": f"An error occurred: {e}"}, 500
   

      
   try: 
      asset_prices_to_update = []
      print("Processing ticker data from Kraken")
      
      for record in history_list.data:
         kraken_response = None  
         
         
         ticker_code = record['ticker_code']
         to_ticker = record['to_ticker_code']
         combined = ticker_code + to_ticker
         try:
            response = request(
               method="GET",
               path="/0/public/Ticker?pair=" + combined,
               environment="https://api.kraken.com",
            )
            kraken_response = json.loads(response.read().decode())
            
            
            ticker_data = kraken_response['result'][list(kraken_response['result'].keys())[0]]

            asset_prices_to_update.append({
               "to_asset_code": to_ticker,
               "from_asset_code": ticker_code,
               "date" : date.today().isoformat(),
               "daily_open": float(ticker_data['o']),
               "daily_high": float(ticker_data['h'][0]),
               "daily_low": float(ticker_data['l'][0]),
               "current_price":float(ticker_data['c'][0]),
               "daily_volume" : float(ticker_data['v'][0]),
               "price_time": datetime.now().isoformat(),
            })
            print(f"Prepared update for {ticker_code} with price {ticker_data['c'][0]} ")
            
         except Exception as e:
            print(f"Error fetching ticker data for {ticker_code}: {e}")
            continue

      batch_size = 500
      for i in range(0, len(asset_prices_to_update), batch_size):
         batch = asset_prices_to_update[i:i + batch_size]
         try:
            response = DSConfig.supabase.table("asset_prices").upsert(batch).execute()
            return {"message": "Asset prices updated successfully"}, 200
            print(f"Successfully updated batch: {len(batch)} records")
         except Exception as e:
            print(f"Error updating batch: {e}")
            return {"message": f"Error updating asset prices: {e}"}, 500
         
   except Exception as e:
      return {"message": f"An error occurred: {e}"}, 500

   print(f"Fetched {len(history_list)} active assets for history flow")
   
   
   
#    a
# string[]
# Ask [<price>, <whole lot volume>, <lot volume>]

# b
# string[]
# Bid [<price>, <whole lot volume>, <lot volume>]

# c
# string[]
# Last trade closed [<price>, <lot volume>]

# v
# string[]
# Volume [<today>, <last 24 hours>]

# p
# string[]
# Volume weighted average price [<today>, <last 24 hours>]

# t
# integer[]
# Number of trades [<today>, <last 24 hours>]

# l
# string[]
# Low [<today>, <last 24 hours>]

# h
# string[]
# High [<today>, <last 24 hours>]

# o
# string
# Today's opening price