## what do we need to do?
## we need a function we call that fetches history from alphavantage for a single asset
from urllib import response
import requests
from src.config import DSConfig

async def fetch_history_for_asset(ticker_code: str, is_crypto: bool):
    
    url = ""
    
    if is_crypto:
        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={ticker_code}&market=USD&apikey={DSConfig.ALPHAVANTAGE_KEY}'
    else:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker_code}&outputsize=full&apikey={DSConfig.ALPHAVANTAGE_KEY}'
    r = requests.get(url)
    
    try :
        data = r.json()
    except requests.exceptions.HTTPError as e:
        
        ## need to maybe process an error here to retry? 
        print(f"HTTP error occurred: {e}")
        return {"message": f"HTTP error occurred: {e}"}, 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": f"An error occurred: {e}"}, 500
    
    write_history_response = await write_history_to_db(ticker_code, data, is_crypto)
    return write_history_response
    
     

async def write_history_to_db(ticker_code: str, history_data: dict, is_crypto: bool):
    
    history = None
    name = None
    market = "USD"
    
    if is_crypto:
        name = history_data.get('Meta Data', {}).get('3. Digital Currency Name', None)
        market = history_data.get('Meta Data', {}).get('4. Market Code', 'USD')
        market_name = history_data.get('Meta Data', {}).get('4. Market Name', 'Dollar')
        history = history_data.get('Time Series (Digital Currency Daily)', {})
        
        
        
        record_list = []
        
        for key in history.keys():
            record = history[key]
            record_list.append({
                "to_asset_code": market,
                "from_asset_code": ticker_code,
                "from_asset_name": name,
                "to_asset_name": market_name,
                "date": key,
                "daily_open": record['1. open'],
                "daily_high": record['2. high'],
                "daily_low": record['3. low'],
                "current_price": record['4. close'],
                "daily_close": record['4. close'],
                "daily_volume": record['5. volume'],
                # "market_cap": record['6. market cap (USD)'],
                # "open": record['1a. open (USD)'],
                # "high": record['2a. high (USD)'],
                # "low": record['3a. low (USD)'],
                # "close": record['4a. close (USD)'],
                # "volume": record['5. volume'],
                # "market_cap": record['6. market cap (USD)'],
            })
            
            

        batch_size = 1000
        for i in range(0, len(record_list), batch_size):
            batch = record_list[i:i + batch_size]
            try:
                response = DSConfig.supabase.table("asset_prices").upsert(batch).execute()
                print(f"Successfully inserted batch: {len(batch)} records")
            except Exception as e:
                print(f"Error inserting batch: {e}")
                return {"message": f"Error inserting history data: {e}"}, 500
        
        try:
            active_asset_response = DSConfig.supabase.table("active_assets").select('*').eq('ticker_code', ticker_code).execute()
        
            if len(active_asset_response.data) > 0:
                asset_id = active_asset_response.data[0]['id']
                DSConfig.supabase.table("active_assets").update(
                    {
                        "initial_fetch_complete": True,
                    }
                ).eq('id', asset_id).execute()
               
               
            ## need to set the initial fetch complete to true here
             
            return {"message": "History data inserted successfully"}, 200
        except Exception as e:
            print("error", e)
            return {"message": f"Error: {e}"}, 500
        
        
        
        
    else:
        time_series = history_data.get('Time Series (Daily)', {})
        
        
        active_asset_response = DSConfig.supabase.table("active_assets").select('*').eq('ticker_code', ticker_code).execute()
                

        
    print("test")
    