import pytest
import numpy as np
from unittest.mock import MagicMock, patch


class TestMLTradingService:
    def test_sine_wave_basic(self):
        from src.services.ml_trading_service import sine_wave
        
        x = np.array([0, 0.25, 0.5, 0.75, 1.0])
        result = sine_wave(x, amplitude=1.0, frequency=1.0, phase=0, offset=0)
        
        expected = np.array([0, 1, 0, -1, 0])
        np.testing.assert_array_almost_equal(result, expected)

    def test_sine_wave_with_offset(self):
        from src.services.ml_trading_service import sine_wave
        
        x = np.array([0, 0.25, 0.5, 0.75, 1.0])
        result = sine_wave(x, amplitude=1.0, frequency=1.0, phase=0, offset=5)
        
        expected = np.array([5, 6, 5, 4, 5])
        np.testing.assert_array_almost_equal(result, expected)

    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_fetch_asset_price_history_success(self, mock_supabase):
        from src.services.ml_trading_service import MLTradingService
        
        mock_response = MagicMock()
        mock_response.data = [
            {"current_price": "100.0", "price_time": "2024-01-01T00:00:00Z"},
            {"current_price": "101.0", "price_time": "2024-01-01T01:00:00Z"},
        ]
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.gte.return_value.order.return_value.execute.return_value = mock_response
        
        service = MLTradingService()
        result = service.fetch_asset_price_history("BTC", hours=24)
        
        assert len(result) == 2
        assert result[0]["current_price"] == "100.0"

    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_fetch_asset_price_history_no_db(self, mock_supabase):
        from src.services.ml_trading_service import MLTradingService
        
        mock_supabase = None
        
        service = MLTradingService()
        with patch('src.services.ml_trading_service.DSConfig') as mock_config:
            mock_config.supabase = None
            result = service.fetch_asset_price_history("BTC")
        
        assert result == []

    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_fetch_asset_price_history_empty(self, mock_supabase):
        from src.services.ml_trading_service import MLTradingService
        
        mock_response = MagicMock()
        mock_response.data = None
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.gte.return_value.order.return_value.execute.return_value = mock_response
        
        service = MLTradingService()
        result = service.fetch_asset_price_history("BTC")
        
        assert result == []

    def test_fit_sine_wave_insufficient_data(self):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        prices = np.array([100, 101, 102])
        times = np.array([0, 1, 2])
        
        result = service.fit_sine_wave(prices, times)
        
        assert result == (None, None, None, None)

    def test_fit_sine_wave_success(self):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        
        x = np.linspace(0, 10, 50)
        y = 10 * np.sin(2 * np.pi * 0.25 * x) + 100
        
        amplitude, frequency, phase, offset = service.fit_sine_wave(y, x)
        
        assert amplitude is not None
        assert frequency is not None
        assert phase is not None
        assert offset is not None

    def test_fit_sine_wave_failure(self):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        
        prices = np.array([100] * 5)
        times = np.array([0, 1, 2, 3, 4])
        
        result = service.fit_sine_wave(prices, times)
        
        assert result == (None, None, None, None)

    def test_calculate_trend_strength_positive(self):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        
        prices = np.array([100, 105, 110, 115, 120])
        times = np.array([0, 1, 2, 3, 4])
        
        result = service.calculate_trend_strength(prices, times)
        
        assert result > 0

    def test_calculate_trend_strength_negative(self):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        
        prices = np.array([120, 115, 110, 105, 100])
        times = np.array([0, 1, 2, 3, 4])
        
        result = service.calculate_trend_strength(prices, times)
        
        assert result < 0

    def test_calculate_trend_strength_flat(self):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        
        prices = np.array([100, 100, 100, 100, 100])
        times = np.array([0, 1, 2, 3, 4])
        
        result = service.calculate_trend_strength(prices, times)
        
        assert abs(result) < 0.1

    def test_identify_peaks_and_valleys(self):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        
        prices = np.array([100, 110, 100, 90, 100])
        peaks, valleys = service.identify_peaks_and_valleys(prices)
        
        assert len(peaks) >= 1
        assert len(valleys) >= 1

    def test_identify_peaks_and_valleys_no_pattern(self):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        
        prices = np.array([100, 100, 100, 100, 100])
        peaks, valleys = service.identify_peaks_and_valleys(prices)
        
        assert len(peaks) == 0

    @patch('src.services.ml_trading_service.MLTradingService.fetch_asset_price_history')
    @patch('src.services.ml_trading_service.MLTradingService.fit_sine_wave')
    @patch('src.services.ml_trading_service.MLTradingService.calculate_trend_strength')
    @patch('src.services.ml_trading_service.MLTradingService.identify_peaks_and_valleys')
    def test_analyze_price_action_insufficient_data(
        self, mock_peaks, mock_trend, mock_fit, mock_fetch
    ):
        from src.services.ml_trading_service import MLTradingService
        
        mock_fetch.return_value = []
        
        service = MLTradingService()
        result = service.analyze_price_action("BTC", asset_id=1)
        
        assert result["has_sufficient_data"] is False
        assert result["signal"] == "hold"
        assert result["confidence"] == 0.0

    @patch('src.services.ml_trading_service.MLTradingService.fetch_asset_price_history')
    @patch('src.services.ml_trading_service.MLTradingService.fit_sine_wave')
    @patch('src.services.ml_trading_service.MLTradingService.calculate_trend_strength')
    @patch('src.services.ml_trading_service.MLTradingService.identify_peaks_and_valleys')
    def test_analyze_price_action_buy_signal(
        self, mock_peaks, mock_trend, mock_fit, mock_fetch
    ):
        from src.services.ml_trading_service import MLTradingService
        
        mock_fetch.return_value = [
            {"current_price": "90.0", "price_time": "2024-01-01T00:00:00Z"},
            {"current_price": "92.0", "price_time": "2024-01-01T01:00:00Z"},
        ] * 15
        
        mock_fit.return_value = (10.0, 0.25, -np.pi/2, 100.0)
        mock_trend.return_value = -0.3
        mock_peaks.return_value = ([1, 3], [2, 4])
        
        service = MLTradingService()
        result = service.analyze_price_action("BTC", asset_id=1)
        
        assert result["has_sufficient_data"] is True

    def test_extract_features_basic(self):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        
        analysis = {
            "amplitude": 10.0,
            "frequency": 0.25,
            "phase": 0.0,
            "offset": 100.0,
            "trend_strength": 0.5,
            "peaks_count": 3,
            "valleys_count": 2,
            "data_points": 50,
            "prices": [90, 95, 100, 105, 110],
        }
        
        features = service.extract_features("BTC", analysis)
        
        assert "amplitude" in features
        assert "frequency" in features
        assert "price_range_pct" in features
        assert "volatility" in features
        assert features["hour_of_day"] >= 0
        assert features["day_of_week"] >= 0

    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_get_ticker_success_rate_exists(self, mock_supabase):
        from src.services.ml_trading_service import MLTradingService
        
        mock_response = MagicMock()
        mock_response.data = [{"success_rate": 0.65, "total_signals": 20}]
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = mock_response
        
        service = MLTradingService()
        success_rate, total = service.get_ticker_success_rate("BTC")
        
        assert success_rate == 0.65
        assert total == 20

    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_get_ticker_success_rate_no_data(self, mock_supabase):
        from src.services.ml_trading_service import MLTradingService
        
        mock_response = MagicMock()
        mock_response.data = []
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = mock_response
        
        service = MLTradingService()
        success_rate, total = service.get_ticker_success_rate("BTC")
        
        assert success_rate == 0.5
        assert total == 0

    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_get_ticker_success_rate_no_db(self, mock_supabase):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        with patch('src.services.ml_trading_service.DSConfig') as mock_config:
            mock_config.supabase = None
            success_rate, total = service.get_ticker_success_rate("BTC")
        
        assert success_rate == 0.5
        assert total == 0

    @patch('src.services.ml_trading_service.MLTradingService.analyze_price_action')
    @patch('src.services.ml_trading_service.MLTradingService.get_ticker_success_rate')
    @patch('src.services.ml_trading_service.MLTradingService.extract_features')
    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_generate_new_signals_no_assets(self, mock_db, mock_features, mock_success, mock_analyze):
        from src.services.ml_trading_service import MLTradingService
        
        mock_analyze.return_value = {
            "has_sufficient_data": True,
            "signal": "buy",
            "confidence": 0.8,
        }
        mock_success.return_value = (0.5, 0)
        mock_features.return_value = {}
        
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
        
        service = MLTradingService()
        result = service.generate_new_signals([])
        
        assert result == []

    @patch('src.services.ml_trading_service.MLTradingService.analyze_price_action')
    @patch('src.services.ml_trading_service.MLTradingService.get_ticker_success_rate')
    @patch('src.services.ml_trading_service.MLTradingService.extract_features')
    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_generate_new_signals_hold_signal(self, mock_db, mock_features, mock_success, mock_analyze):
        from src.services.ml_trading_service import MLTradingService
        
        mock_analyze.return_value = {
            "has_sufficient_data": True,
            "signal": "hold",
            "confidence": 0.3,
        }
        mock_success.return_value = (0.5, 0)
        
        service = MLTradingService()
        result = service.generate_new_signals([{"id": 1, "ticker_code": "BTC", "is_crypto": True}])
        
        assert result == []

    @patch('src.services.ml_trading_service.MLTradingService.analyze_price_action')
    @patch('src.services.ml_trading_service.MLTradingService.get_ticker_success_rate')
    @patch('src.services.ml_trading_service.MLTradingService.extract_features')
    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_generate_new_signals_low_confidence(self, mock_db, mock_features, mock_success, mock_analyze):
        from src.services.ml_trading_service import MLTradingService
        
        mock_analyze.return_value = {
            "has_sufficient_data": True,
            "signal": "buy",
            "confidence": 0.5,
        }
        mock_success.return_value = (0.5, 0)
        
        service = MLTradingService()
        result = service.generate_new_signals([{"id": 1, "ticker_code": "BTC", "is_crypto": True}])
        
        assert result == []

    @patch('src.services.ml_trading_service.MLTradingService.analyze_price_action')
    @patch('src.services.ml_trading_service.MLTradingService.get_ticker_success_rate')
    @patch('src.services.ml_trading_service.MLTradingService.extract_features')
    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_generate_new_signals_existing_active_signal(self, mock_db, mock_features, mock_success, mock_analyze):
        from src.services.ml_trading_service import MLTradingService
        
        mock_analyze.return_value = {
            "has_sufficient_data": True,
            "signal": "buy",
            "confidence": 0.8,
            "current_price": 100.0,
            "amplitude": 10.0,
            "frequency": 0.25,
            "phase": 0.0,
            "trend_strength": 0.5,
            "price_range": 10.0,
            "peaks_count": 2,
            "valleys_count": 2,
            "data_points": 50,
        }
        mock_success.return_value = (0.5, 0)
        mock_features.return_value = {}
        
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        
        service = MLTradingService()
        result = service.generate_new_signals([{"id": 1, "ticker_code": "BTC", "is_crypto": True}])
        
        assert result == []

    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_get_users_with_signals_empty(self, mock_supabase):
        from src.services.ml_trading_service import MLTradingService
        
        mock_response = MagicMock()
        mock_response.data = []
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.eq.return_value.execute.return_value = mock_response
        
        service = MLTradingService()
        result = service.get_users_with_signals()
        
        assert result == []

    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_get_users_with_signals_no_db(self, mock_supabase):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        with patch('src.services.ml_trading_service.DSConfig') as mock_config:
            mock_config.supabase = None
            result = service.get_users_with_signals()
        
        assert result == []

    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_update_model_metrics_no_data(self, mock_supabase):
        from src.services.ml_trading_service import MLTradingService
        
        mock_response = MagicMock()
        mock_response.data = []
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.execute.return_value = mock_response
        
        service = MLTradingService()
        service.update_model_metrics()

    @patch('src.services.ml_trading_service.DSConfig.supabase')
    def test_update_model_metrics_with_data(self, mock_supabase):
        from src.services.ml_trading_service import MLTradingService
        
        mock_response = MagicMock()
        mock_response.data = [
            {"signal_id": "s1", "was_correct": True, "profit_loss_percent": 5.0},
            {"signal_id": "s2", "was_correct": False, "profit_loss_percent": -3.0},
        ]
        
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value.execute.return_value = mock_response
        mock_table.insert.return_value.execute.return_value = MagicMock()
        
        service = MLTradingService()
        service.update_model_metrics()


class TestMLTradingServiceDefaults:
    def test_default_values(self):
        from src.services.ml_trading_service import MLTradingService
        
        service = MLTradingService()
        
        assert service.lookback_hours == 4
        assert service.target_hours == 4
        assert service.min_data_points == 20
        assert service.default_frequency == 0.25
        assert service.min_price_movement_pct == 3.0
