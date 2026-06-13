import asyncio
import os
from datetime import datetime, timedelta
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def analyze():
    print("--- STARTING DEEP ANALYSIS ---")
    
    one_month_ago = (datetime.now() - timedelta(days=30)).isoformat()
    print(f"Fetching signals since {one_month_ago}...")
    
    try:
        signals_res = supabase.table("ml_signal_history")            .select("ticker_code, price_at_signal, price_4h_later, was_correct, profit_loss_percent, evaluation_timestamp")            .gte("evaluation_timestamp", one_month_ago)            .order("evaluation_timestamp", desc=True)            .execute()
        
        signals = signals_res.data
        print(f"Found {len(signals)} signals.")
        
        if not signals:
            print("No signals found to analyze.")
            return

        ticker_stats = {}
        for s in signals:
            t = s['ticker_code']
            if t not in ticker_stats:
                ticker_stats[t] = {'total': 0, 'correct': 0, 'pl_sum': 0.0, 'valid_pl_count': 0}
            
            ticker_stats[t]['total'] += 1
            
            if s.get('was_correct') is True:
                ticker_stats[t]['correct'] += 1
                
            pl = s.get('profit_loss_percent')
            if pl is not None:
                ticker_stats[t]['pl_sum'] += float(pl)
                ticker_stats[t]['valid_pl_count'] += 1

        print("\n[Ticker Performance Summary]")
        for t, stats in ticker_stats.items():
            acc = (stats['correct'] / stats['total']) * 100
            avg_pl = (stats['pl_sum'] / stats['valid_pl_count']) if stats['valid_pl_count'] > 0 else 0.0
            print(f"Ticker: {t:8} | Accuracy: {acc:6.2f}% | Avg P/L: {avg_pl:6.4f}% | Signals: {stats['total']} (Valid P/L: {stats['valid_pl_count']})")

        # 3. Deep dive into the most recent valid ticker's price vs signal
        valid_signals = [s for s in signals if s.get('profit_loss_percent') is not None]
        if not valid_signals:
            print("\nNo signals with valid P/L found for deep dive.")
            return

        target_signal = valid_signals[0]
        target_ticker = target_signal['ticker_code']
        target_time = target_signal['evaluation_timestamp']
        print(f"\n[Deep Dive: {target_ticker}]")
        print(f"Last Valid Signal Time: {target_time}")
        print(f"Signal Price: {target_signal['price_at_signal']}")
        print(f"Actual Price 4h Later: {target_signal['price_4h_later']}")
        print(f"Was Correct: {target_signal['was_correct']} ({target_signal['profit_loss_percent']}% PL)")

        # 4. Check price volatility/trend leading up to signals
        print(f"\nFetching price history for {target_ticker} around signal time...")
        
        try:
            # Use evaluation_timestamp or fallback to a timestamp format that works
            # We'll parse it carefully
            ts_str = target_time
            if isinstance(ts_str, str):
                dt_obj = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
            else:
                dt_obj = ts_str
                
            start_window = (dt_obj - timedelta(hours=24)).isoformat()
            
            prices_res = supabase.table("asset_prices")                .select("price_time, current_price")                .eq("from_asset_code", target_ticker)                .gte("price_time", start_window)                .lte("price_time", ts_str)                .order("price_time", desc=False)                .execute()
            
            prices = prices_res.data
            print(f"Found {len(prices)} price points in the 24h window.")
            
            if len(prices) > 1:
                first_p = float(prices[0]['current_price'])
                last_p = float(prices[-1]['current_price'])
                change = ((last_p - first_p) / first_p) * 100
                print(f"24h Window Price Change: {change:.4f}%")
                
                if abs(change) < 0.1:
                    print("WARNING: Signal occurred during a very flat price period (low volatility).")
            else:
                print("WARNING: Insufficient price points in the window to validate trend.")
                
        except Exception as e:
            print(f"Error fetching price history: {e}")

    except Exception as e:
        print(f"Critical Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(analyze())
