Goal
- Analyze ML model performance and propose logic improvements to mitigate trading in low-volatility "noise" environments.
Constraints & Preferences
- (none)
Progress
Done
- Analyzed ml_trading_service.py logic: weighted ensemble of Sine Wave (40%), Moving Averages (30%), RSI (20%), and Trend (10%).
- Investigated data ingestion: alphavantage_services.py (daily historical) and kraken_services.py (5-minute ticker updates via run_history_flow).
- Confirmed asset_prices table is populated with 5-minute intervals via Kraken.
- Identified issue in ml_model_metrics: metrics appear static/unchanging across hourly snapshots.
- Performed schema inspection via inspect_schema.py.
- Performed deep analysis via final_analysis.py, uncovering:
- Model is trading "noise" in low-volatility environments.
- Average P/L is extremely thin (~0.17% to 0.26%), likely insufficient to cover fees/slippage.
- BTC shows highest accuracy (57.99%); ALGO shows poor accuracy (41.61%).
- Encountered BaseSelectRequestBuilder.order() got an unexpected keyword argument 'asc' error in analysis script.
In Progress
- Implementing logic improvements in ml_trading_service.py to increase profitability.
Blocked
- (none)
Key Decisions
- Decision: Implement a Volatility Filter (Noise Gate) to prevent signal generation when price movement is below a certain threshold.
- Decision: Implement Trend-Confirmation Requirement to penalize signals where the Sine Wave direction contradicts the Trend component.
Next Steps
- Implement the Volatility Filter (using ATR or standard deviation) in sin-trade-ds/src/services/ml_trading_service.py.
- Implement Dynamic Weighting: Increase Trend component weight for volatile assets and Mean Reversion weight for stable assets.
- Implement Trend-Confirmation logic: Reduce signal strength if Trend_Direction != Sine_Direction.
Critical Context
- Data Density: asset_prices contains ~288 data points per 24h window (5-min intervals).
- Data Integrity Issue: ml_signal_history.profit_loss_percent contains NULL values.
- Model Metrics: ml_model_metrics shows identical accuracy and avg_profit_loss across multiple hourly records.
- Execution Error: supabase._sync.client.SupabaseException: supabase_url is required occurred due to environment variable scope issues.
Relevant Files
- sin-trade-ds/src/services/ml_trading_service.py: Core ML logic and price history fetching.
- sin-trade-ds/src/services/alphavantage_services.py: Historical stock/crypto data ingestion.
- sin-trade-ds/src/services/kraken_services.py: 5-minute interval crypto price updates.
- sin-trade-ds/src/ds_job_scheduler.py: Manages job intervals for Kraken updates and ML runs.
- sin-trade-ds/src/app.py: Configures BackgroundScheduler.
- final_analysis.py: Custom script for cross-referencing signals, outcomes, and price volatility.
- inspect_schema.py: Utility to map correct database columns.