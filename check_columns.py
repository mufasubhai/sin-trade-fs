import asyncio
import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def check():
    try:
        # Fetching one row to inspect keys
        res = supabase.table("ml_signal_history").select("*").limit(1).execute()
        if res.data:
            print("Columns in ml_signal_history:", res.data[0].keys())
        else:
            print("Table ml_signal_history is empty.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
