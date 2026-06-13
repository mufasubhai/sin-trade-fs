
import asyncio
import os
from datetime import datetime, timedelta
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
# Mocking the structure as per the project's config
# In a real scenario, these would come from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-key")
print(f"Using Supabase URL: {SUPABASE_URL}")
print(f"Using Supabase Key: {'****' + SUPABASE_KEY[-4:]}")  # Masking the key for security

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def analyze_data():
    print("Starting Data Analysis...")
    
    # 1. Examine ml_signal_history (last month)
    one_month_ago = (datetime.now() - timedelta(days=30)).isoformat()
    print(f"Fetching ml_signal_history since {one_month_ago}")
    try:
        signals = supabase.table("ml_signal_history").select("*").gte("created_at", one_month_ago).execute()
        print(f"Found {len(signals.data)} signals in history.")
        if signals.data:
            # Sample a few to see structure
            for s in signals.data[:5]:
                print(f"Signal: {s}")
    except Exception as e:
        print(f"Error fetching signals: {e}")

    # 2. Examine ml_model_metrics
    print("\nFetching ml_model_metrics...")
    try:
        metrics = supabase.table("ml_model_metrics").select("*").order("created_at", desc=True).limit(10).execute()
        print(f"Latest metrics: {metrics.data}")
    except Exception as e:
        print(f"Error fetching metrics: {e}")

    # 3. Examine asset_prices (sample recent data for a specific ticker if available)
    # We'll try to find a ticker from signals first
    ticker_to_check = None
    if 'signals' in locals() and signals.data:
        ticker_to_check = signals.data[0].get('ticker_code') or signals.data[0].get('from_asset_code')
    
    if ticker_to_check:
        print(f"\nFetching recent asset_prices for {ticker_to_check}...")
        try:
            prices = supabase.table("asset_prices").select("*").eq("from_asset_code", ticker_to_check).order("price_time", desc=True).limit(100).execute()
            print(f"Found {len(prices.data)} price points for {ticker_to_check}.")
            if prices.data:
                print(f"Latest price point: {prices.data[0]}")
        except Exception as e:
            print(f"Error fetching prices: {e}")
    else:
        print("\nNo ticker found in signals to check prices.")

    # 4. Examine ml_model_performance (if it exists as a table)
    print("\nFetching ml_model_performance...")
    try:
        perf = supabase.table("ml_model_performance").select("*").limit(5).execute()
        print(f"Performance data: {perf.data}")
    except Exception as e:
        print(f"Error fetching performance (table might not exist): {e}")

if __name__ == "__main__":
    asyncio.run(analyze_data())
