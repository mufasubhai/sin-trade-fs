import asyncio
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Ensure we use the environment variables that were working before
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def check():
    tables = ["ml_signal_history", "ml_model_performance_history", "asset_prices"]
    for table in tables:
        print(f"\n--- Table: {table} ---")
        try:
            # Get one row to see columns
            res = supabase.table(table).select("*").limit(1).execute()
            if res.data:
                print(f"Columns: {list(res.data[0].keys())}")
            else:
                print("Table is empty.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
