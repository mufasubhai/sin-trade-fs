
import numpy as np
from scipy.optimize import curve_fit
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Tuple, Optional
from src.config import DSConfig


def sine_wave(x, amplitude, frequency, phase, offset):
    return amplitude * np.sin(2 * np.pi * frequency * x + phase) + offset


class MLTradingService:
    def __init__(self):
        self.lookback_hours = 4
        self.target_hours = 4
        self.min_data_points = 20
        self.default_frequency = 0.25
        self.min_price_movement_pct = 3.0

    def fetch_asset_price_history(
        self, ticker_code: str, hours: int = 24
    ) -> List[Dict]:
        try:
            if not DSConfig.supabase:
                return []

            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)

            response = (
                DSConfig.supabase.table("asset_prices")
                .select("*")
                .eq("from_asset_code", ticker_code)
                .gte("price_time", cutoff_time.isoformat())
                .order("price_time", desc=True)
                .execute()
            )

            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching price history for asset {ticker_code}: {e}")
            return []

    def fit_sine_wave(
        self, prices: np.ndarray, times: np.ndarray
    ) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
        if len(prices) < self.min_data_points:
            return None, None, None, None

        try:
            times_normalized = (times - times.min()) / (times.max() - times.min() + 1e-10)

            initial_guess = [
                np.std(prices),
                self.default_frequency,
                0,
                np.mean(prices),
            ]

            bounds = (
                [0, 0.01, -np.pi, prices.min() * 0.5],
                [prices.max() * 2, 2, np.pi, prices.max() * 2],
            )

            popt, _ = curve_fit(
                sine_wave,
                times_normalized,
                prices,
                p0=initial_guess,
                bounds=bounds,
                maxfev=5000,
            )

            amplitude, frequency, phase, offset = popt
            return amplitude, frequency, phase, offset

        except Exception as e:
            print(f"Error fitting sine wave: {e}")
            return None, None, None, None

    def calculate_trend_strength(
        self, prices: np.ndarray, times: np.ndarray
    ) -> float:
        if len(prices) < 2:
            return 0.0

        normalized_times = (times - times.min()) / (times.max() - times.min() + 1e-10)
        coeffs = np.polyfit(normalized_times, prices, 1)
        trend_slope = coeffs[0]

        price_range = prices.max() - prices.min()
        if price_range == 0:
            return 0.0

        normalized_slope = trend_slope / price_range
        return np.clip(normalized_slope * 10, -1, 1)

    def identify_peaks_and_valleys(
        self, prices: np.ndarray
    ) -> Tuple[List[int], List[int]]:
        peaks = []
        valleys = []

        if len(prices) < 3:
            return peaks, valleys

        for i in range(1, len(prices) - 1):
            if prices[i] > prices[i - 1] and prices[i] > prices[i + 1]:
                peaks.append(i)
            elif prices[i] < prices[i - 1] and prices[i] < prices[i + 1]:
                valleys.append(i)

        return peaks, valleys

    def analyze_price_action(
        self, ticker_code: str, asset_id: Optional[int] = None
    ) -> Dict:
        history = self.fetch_asset_price_history(ticker_code, hours=24)

        if not history or len(history) < self.min_data_points:
            return {
                "asset_id": asset_id,
                "ticker_code": ticker_code,
                "has_sufficient_data": False,
                "signal": "hold",
                "confidence": 0.0,
            }

        prices = np.array([float(h["current_price"]) for h in history])
        now = datetime.now(timezone.utc)
        times = np.array(
            [
                (datetime.fromisoformat(h["price_time"].replace("Z", "+00:00")) - now).total_seconds()
                / 3600
                for h in history
            ]
        )

        amplitude, frequency, phase, offset = self.fit_sine_wave(prices, times)
        trend_strength = self.calculate_trend_strength(prices, times)
        peaks, valleys = self.identify_peaks_and_valleys(prices)

        current_price = prices[0]
        normalized_position = (current_price - prices.min()) / (prices.max() - prices.min() + 1e-10)

        signal = "hold"
        confidence = 0.5
        expected_movement_pct = 0.0

        if amplitude and frequency and phase and offset:
            predicted_peak = offset + amplitude
            predicted_valley = offset - amplitude
            time_to_peak = (np.pi / 2 - phase) / (2 * np.pi * frequency) if frequency > 0 else 999
            time_to_valley = (-np.pi / 2 - phase) / (2 * np.pi * frequency) if frequency > 0 else 999

            sell_movement_pct = ((predicted_peak - current_price) / current_price) * 100 if current_price > 0 else 0
            buy_movement_pct = ((current_price - predicted_valley) / current_price) * 100 if current_price > 0 else 0

            if normalized_position > 0.85 and time_to_peak < 1 and sell_movement_pct >= self.min_price_movement_pct:
                signal = "sell"
                expected_movement_pct = sell_movement_pct
                confidence = min(0.95, normalized_position + 0.1)
            elif normalized_position < 0.15 and time_to_valley < 1 and buy_movement_pct >= self.min_price_movement_pct:
                signal = "buy"
                expected_movement_pct = buy_movement_pct
                confidence = min(0.95, (1 - normalized_position) + 0.1)
            elif trend_strength > 0.5:
                signal = "hold"
                confidence = min(0.9, 0.5 + trend_strength * 0.3)
            elif trend_strength < -0.5:
                signal = "hold"
                confidence = min(0.9, 0.5 + abs(trend_strength) * 0.3)

        return {
            "asset_id": asset_id,
            "ticker_code": ticker_code,
            "has_sufficient_data": True,
            "signal": signal,
            "confidence": confidence,
            "current_price": current_price,
            "price_range": float(prices.max() - prices.min()),
            "trend_strength": float(trend_strength),
            "amplitude": float(amplitude) if amplitude else None,
            "frequency": float(frequency) if frequency else None,
            "phase": float(phase) if phase else None,
            "offset": float(offset) if offset else None,
            "peaks_count": len(peaks),
            "valleys_count": len(valleys),
            "data_points": len(prices),
            "prices": prices.tolist(),
            "times": times.tolist(),
            "expected_movement_pct": expected_movement_pct,
        }

    def extract_features(self, ticker_code: str, analysis: Dict) -> Dict:
        try:
            prices = analysis.get("prices", [])
            if not prices:
                history = self.fetch_asset_price_history(ticker_code, hours=24)
                prices = [float(h["current_price"]) for h in history]
            
            if len(prices) < 2:
                return {}

            prices_arr = np.array(prices)
            
            price_range_pct = 0
            if prices_arr.min() > 0:
                price_range_pct = float((prices_arr.max() - prices_arr.min()) / prices_arr.min() * 100)
            
            volatility = float(np.std(prices_arr)) if len(prices_arr) > 1 else 0
            
            moving_avg = float(np.mean(prices_arr)) if len(prices_arr) > 0 else 0
            current_price = prices_arr[0] if len(prices_arr) > 0 else 0
            price_vs_avg = 0
            if moving_avg > 0:
                price_vs_avg = float((current_price - moving_avg) / moving_avg * 100)

            return {
                "amplitude": analysis.get("amplitude"),
                "frequency": analysis.get("frequency"),
                "phase": analysis.get("phase"),
                "offset": analysis.get("offset"),
                "price_range_pct": price_range_pct,
                "volatility": volatility,
                "current_price_vs_avg": price_vs_avg,
                "trend_strength": analysis.get("trend_strength"),
                "peaks_count": analysis.get("peaks_count", 0),
                "valleys_count": analysis.get("valleys_count", 0),
                "data_points": analysis.get("data_points", 0),
                "hour_of_day": datetime.now().hour,
                "day_of_week": datetime.now().weekday(),
            }
        except Exception as e:
            print(f"Error extracting features: {e}")
            return {}

    def get_ticker_success_rate(self, ticker_code: str) -> Tuple[float, int]:
        try:
            if not DSConfig.supabase:
                return 0.5, 0
            
            response = (
                DSConfig.supabase.table("ml_ticker_stats")
                .select("success_rate, total_signals")
                .eq("ticker_code", ticker_code)
                .execute()
            )
            
            if response.data:
                stats = response.data[0]
                return float(stats.get("success_rate", 0.5)), int(stats.get("total_signals", 0))
            
            return 0.5, 0
        except Exception as e:
            print(f"Error getting ticker stats: {e}")
            return 0.5, 0

    def evaluate_past_signals(self) -> int:
        try:
            if not DSConfig.supabase:
                return 0

            four_hours_ago = datetime.now(timezone.utc) - timedelta(hours=self.lookback_hours)

            response = (
                DSConfig.supabase.table("ml_trade_signals")
                .select("*")
                .eq("is_active", True)
                .lt("created_at", four_hours_ago.isoformat())
                .execute()
            )

            if not response.data:
                return 0

            evaluated_count = 0
            for signal in response.data:
                asset_id = signal["asset_id"]
                ticker_code = signal.get("ticker_code", "")
                
                if not ticker_code:
                    ticker_response = (
                        DSConfig.supabase.table("active_assets")
                        .select("ticker_code")
                        .eq("id", asset_id)
                        .execute()
                    )
                    
                    if not ticker_response.data:
                        continue
                    
                    ticker_code = ticker_response.data[0]["ticker_code"]
                
                history = self.fetch_asset_price_history(ticker_code, hours=24)

                if not history:
                    continue

                signal_time = datetime.fromisoformat(
                    signal["created_at"].replace("Z", "+00:00")
                )

                price_4h_later = None
                for h in history:
                    h_time = datetime.fromisoformat(h["price_time"].replace("Z", "+00:00"))
                    if h_time >= signal_time + timedelta(hours=4):
                        price_4h_later = float(h["current_price"])
                        break

                if price_4h_later is None:
                    continue

                price_at_signal = float(signal["price_at_signal"])
                
                was_correct = None
                profit_loss_percent = None

                if signal["signal_type"] == "sell":
                    was_correct = price_4h_later < price_at_signal
                    if price_at_signal > 0:
                        profit_loss_percent = ((price_at_signal - price_4h_later) / price_at_signal) * 100
                elif signal["signal_type"] == "buy":
                    was_correct = price_4h_later > price_at_signal
                    if price_at_signal > 0:
                        profit_loss_percent = ((price_4h_later - price_at_signal) / price_at_signal) * 100

                DSConfig.supabase.table("ml_signal_history").insert({
                    "signal_id": signal["id"],
                    "asset_id": asset_id,
                    "user_id": signal["user_id"],
                    "ticker_code": signal.get("ticker_code", ""),
                    "is_crypto": signal.get("is_crypto", False),
                    "original_signal_type": signal["signal_type"],
                    "price_at_signal": price_at_signal,
                    "price_4h_later": price_4h_later,
                    "was_correct": was_correct,
                    "profit_loss_percent": profit_loss_percent,
                    "evaluation_timestamp": signal["created_at"],
                    "features": signal.get("metadata", {}),
                }).execute()

                DSConfig.supabase.table("ml_trade_signals").update({
                    "is_active": False,
                    "expires_at": datetime.now().isoformat(),
                }).eq("id", signal["id"]).execute()

                evaluated_count += 1

            return evaluated_count

        except Exception as e:
            print(f"Error evaluating past signals: {e}")
            return 0

    def generate_new_signals(
        self, assets: List[Dict]
    ) -> List[Dict]:
        new_signals = []

        for asset in assets:
            asset_id = asset["id"]
            ticker_code = asset["ticker_code"]
            is_crypto = asset.get("is_crypto", False)
            
            success_rate, total_signals = self.get_ticker_success_rate(ticker_code)
            
            min_confidence_threshold = 0.6
            
            if total_signals >= 10:
                if success_rate < 0.3:
                    min_confidence_threshold = 0.8
                elif success_rate < 0.4:
                    min_confidence_threshold = 0.7
                elif success_rate < 0.5:
                    min_confidence_threshold = 0.65
            
            analysis = self.analyze_price_action(ticker_code, asset_id)

            if not analysis["has_sufficient_data"]:
                continue

            if analysis["signal"] == "hold" or analysis["confidence"] < min_confidence_threshold:
                continue

            features = self.extract_features(ticker_code, analysis)
            
            adjusted_confidence = analysis["confidence"]
            if total_signals >= 5 and success_rate > 0:
                adjusted_confidence = analysis["confidence"] * (0.5 + success_rate / 2)
                adjusted_confidence = min(0.95, adjusted_confidence)

            try:
                response = (
                    DSConfig.supabase.table("user_assets")
                    .select("user_id, asset_id")
                    .eq("asset_id", asset_id)
                    .execute()
                )

                if not response.data:
                    continue

                for user_asset in response.data:
                    user_int_id = user_asset.get("user_id")
                    
                    if not user_int_id:
                        continue
                    
                    existing_signal = (
                        DSConfig.supabase.table("ml_trade_signals")
                        .select("id")
                        .eq("asset_id", asset_id)
                        .eq("user_id", user_int_id)
                        .eq("is_active", True)
                        .execute()
                    )
                    
                    if existing_signal.data:
                        continue
                    
                    expires_at = datetime.now() + timedelta(hours=self.target_hours)

                    insert_response = (
                        DSConfig.supabase.table("ml_trade_signals")
                        .insert({
                            "asset_id": user_asset["asset_id"],
                            "user_id": user_int_id,
                            "ticker_code": ticker_code,
                            "is_crypto": is_crypto,
                            "signal_type": analysis["signal"],
                            "price_at_signal": analysis["current_price"],
                            "confidence_score": adjusted_confidence,
                            "sine_wave_amplitude": analysis["amplitude"],
                            "sine_wave_frequency": analysis["frequency"],
                            "sine_wave_phase": analysis["phase"],
                            "sine_wave_offset": analysis.get("offset"),
                            "expires_at": expires_at.isoformat(),
                            "metadata": {
                                "ticker_code": ticker_code,
                                "trend_strength": analysis["trend_strength"],
                                "price_range": analysis["price_range"],
                                "peaks_count": analysis["peaks_count"],
                                "valleys_count": analysis["valleys_count"],
                                "data_points": analysis["data_points"],
                                "historical_success_rate": success_rate,
                                "total_historical_signals": total_signals,
                            },
                        })
                        .execute()
                    )

                    if insert_response.data:
                        new_signals.append({
                            "signal_id": insert_response.data[0]["id"],
                            "asset_id": asset_id,
                            "ticker_code": ticker_code,
                            "is_crypto": is_crypto,
                            "user_id": user_int_id,
                            "signal_type": analysis["signal"],
                            "confidence": adjusted_confidence,
                            "features": features,
                        })

            except Exception as e:
                print(f"Error generating signal for asset {ticker_code}: {e}")
                continue

        return new_signals

    def get_users_with_signals(self) -> List[Dict]:
        try:
            if not DSConfig.supabase:
                return []

            response = (
                DSConfig.supabase.table("ml_trade_signals")
                .select(
                    """
                    id,
                    user_id,
                    asset_id,
                    ticker_code,
                    is_crypto,
                    signal_type,
                    price_at_signal,
                    confidence_score,
                    created_at
                    """
                )
                .eq("is_active", True)
                .execute()
            )

            if not response.data:
                return []

            users_map = {}
            for signal in response.data:
                user_id = signal["user_id"]
                asset_id = signal["asset_id"]
                ticker_code = signal.get("ticker_code")
                if not ticker_code:
                    ticker_code = signal.get("metadata", {}).get("ticker_code")
                is_crypto = signal.get("is_crypto", False) or False
                
                if user_id not in users_map:
                    users_map[user_id] = {
                        "user_id": user_id,
                        "email": None,
                        "signals": {},
                    }
                
                existing = users_map[user_id]["signals"].get(asset_id)
                if existing is None or (signal.get("created_at", "") > existing.get("created_at", "")):
                    users_map[user_id]["signals"][asset_id] = {
                        "asset_id": asset_id,
                        "ticker_code": ticker_code or "UNKNOWN",
                        "is_crypto": is_crypto,
                        "signal_type": signal["signal_type"],
                        "price_at_signal": signal["price_at_signal"],
                        "confidence_score": signal["confidence_score"],
                        "created_at": signal.get("created_at", ""),
                    }

            for user_id in users_map:
                users_map[user_id]["signals"] = list(users_map[user_id]["signals"].values())

            for user_id in users_map:
                try:
                    user_response = (
                        DSConfig.supabase.table("profiles")
                        .select("email")
                        .eq("user_id", user_id)
                        .execute()
                    )
                    if user_response.data:
                        users_map[user_id]["email"] = user_response.data[0].get("email")
                except Exception as e:
                    print(f"Error fetching user email for {user_id}: {e}")

            return [v for v in users_map.values() if v["email"]]

        except Exception as e:
            print(f"Error getting users with signals: {e}")
            return []

    def update_model_metrics(self) -> None:
        try:
            if not DSConfig.supabase:
                return

            response = (
                DSConfig.supabase.table("ml_signal_history")
                .select("signal_id, was_correct, profit_loss_percent")
                .execute()
            )

            if not response.data:
                return

            total = len(response.data)
            correct = sum(1 for s in response.data if s["was_correct"] is True)
            accuracy = correct / total if total > 0 else 0

            profit_losses = [
                s["profit_loss_percent"]
                for s in response.data
                if s["profit_loss_percent"] is not None
            ]
            avg_profit_loss = (
                sum(profit_losses) / len(profit_losses) if profit_losses else 0
            )

            DSConfig.supabase.table("ml_model_metrics").insert({
                "model_name": "sine_wave_swing",
                "model_version": "1.0.0",
                "accuracy": accuracy,
                "total_signals": total,
                "correct_signals": correct,
                "avg_profit_loss": avg_profit_loss,
                "time_period_end": datetime.now().isoformat(),
            }).execute()

        except Exception as e:
            print(f"Error updating model metrics: {e}")


async def run_ml_trading_analysis():
    service = MLTradingService()

    print(f"Starting ML trading analysis at {datetime.now()}")

    print("Evaluating past signals...")
    evaluated = service.evaluate_past_signals()
    print(f"Evaluated {evaluated} past signals")

    print("Fetching active assets...")
    try:
        response = DSConfig.supabase.table("active_assets").select("id, ticker_code, is_crypto").execute()
        assets = response.data if response.data else []
    except Exception as e:
        print(f"Error fetching active assets: {e}")
        assets = []

    if not assets:
        print("No active assets found")
        return

    print(f"Analyzing {len(assets)} assets...")
    new_signals = service.generate_new_signals(assets)
    print(f"Generated {len(new_signals)} new signals")

    print("Updating model metrics...")
    service.update_model_metrics()

    print("Fetching users with active signals...")
    users_with_signals = service.get_users_with_signals()
    print(f"Found {len(users_with_signals)} users with active signals")

    return users_with_signals
