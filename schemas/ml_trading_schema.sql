-- ML Trading Schema for SinTrade
-- Run this in Supabase SQL Editor
-- Updated to use integer user_id from profiles table instead of UUID from auth.users

-- Drop existing tables (if they exist with old UUID columns)
DROP TABLE IF EXISTS ml_email_notifications CASCADE;
DROP TABLE IF EXISTS ml_user_preferences CASCADE;
DROP TABLE IF EXISTS ml_signal_history CASCADE;
DROP TABLE IF EXISTS ml_ticker_stats CASCADE;
DROP TABLE IF EXISTS ml_model_metrics CASCADE;
DROP TABLE IF EXISTS ml_trade_signals CASCADE;
DROP FUNCTION get_users_with_active_signals;

-- Table: ml_trade_signals
-- Stores generated buy/sell/do nothing signals for assets
CREATE TABLE IF NOT EXISTS ml_trade_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id BIGINT NOT NULL REFERENCES active_assets(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    ticker_code VARCHAR(20) NOT NULL,
    is_crypto BOOLEAN NOT NULL DEFAULT FALSE,
    signal_type VARCHAR(10) NOT NULL CHECK (signal_type IN ('buy', 'sell', 'hold')),
    price_at_signal DECIMAL(20, 8),
    confidence_score DECIMAL(5, 4),
    sine_wave_amplitude DECIMAL(20, 8),
    sine_wave_frequency DECIMAL(20, 8),
    sine_wave_phase DECIMAL(20, 8),
    sine_wave_offset DECIMAL(20, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP WITH TIME ZONE,
    ai_context JSONB,
    metadata JSONB
);

-- Table: ml_signal_history
-- Stores historical signals with correctness evaluation (retroactive analysis)
CREATE TABLE IF NOT EXISTS ml_signal_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    signal_id UUID NOT NULL REFERENCES ml_trade_signals(id) ON DELETE CASCADE,
    asset_id BIGINT NOT NULL REFERENCES active_assets(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    ticker_code VARCHAR(20) NOT NULL,
    is_crypto BOOLEAN NOT NULL DEFAULT FALSE,
    original_signal_type VARCHAR(10) NOT NULL,
    price_at_signal DECIMAL(20, 8),
    price_4h_later DECIMAL(20, 8),
    was_correct BOOLEAN,
    profit_loss_percent DECIMAL(10, 4),
    evaluation_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    features JSONB,
    ai_context JSONB,
    metadata JSONB
);

-- Table: ml_ticker_stats
-- Stores aggregated performance stats per ticker (for adaptive thresholds)
CREATE TABLE IF NOT EXISTS ml_ticker_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker_code VARCHAR(20) NOT NULL UNIQUE,
    is_crypto BOOLEAN NOT NULL DEFAULT FALSE,
    total_signals INTEGER DEFAULT 0,
    correct_signals INTEGER DEFAULT 0,
    success_rate DECIMAL(5, 4),
    avg_profit_loss DECIMAL(10, 4),
    buy_signals INTEGER DEFAULT 0,
    buy_correct INTEGER DEFAULT 0,
    sell_signals INTEGER DEFAULT 0,
    sell_correct INTEGER DEFAULT 0,
    last_calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: ml_model_metrics
-- Stores model performance metrics for future AI tooling and analysis
CREATE TABLE IF NOT EXISTS ml_model_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT REFERENCES profiles(user_id) ON DELETE SET NULL,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    asset_id BIGINT REFERENCES active_assets(id) ON DELETE SET NULL,
    accuracy DECIMAL(5, 4),
    precision_score DECIMAL(5, 4),
    recall_score DECIMAL(5, 4),
    f1_score DECIMAL(5, 4),
    total_signals INTEGER DEFAULT 0,
    correct_signals INTEGER DEFAULT 0,
    avg_profit_loss DECIMAL(10, 4),
    time_period_start TIMESTAMP WITH TIME ZONE,
    time_period_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    training_data_points INTEGER,
    hyperparameters JSONB,
    feature_importance JSONB,
    notes TEXT
);

-- Table: ml_user_preferences
-- Stores user preferences for ML trading alerts
CREATE TABLE IF NOT EXISTS ml_user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE UNIQUE,
    email_alerts_enabled BOOLEAN DEFAULT TRUE,
    min_confidence_threshold DECIMAL(5, 4) DEFAULT 0.7,
    max_hold_hours INTEGER DEFAULT 4,
    preferred_signal_types VARCHAR(50)[] DEFAULT ARRAY['buy', 'sell'],
    alert_frequency VARCHAR(20) DEFAULT 'immediate' CHECK (alert_frequency IN ('immediate', 'daily', 'weekly')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: ml_email_notifications
-- Stores queued email notifications for trade signals
CREATE TABLE IF NOT EXISTS ml_email_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT NOT NULL REFERENCES profiles(user_id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(500) NOT NULL,
    body TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'failed', 'skipped')),
    signals JSONB,
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_ml_trade_signals_user_id ON ml_trade_signals(user_id);
CREATE INDEX IF NOT EXISTS idx_ml_trade_signals_asset_id ON ml_trade_signals(asset_id);
CREATE INDEX IF NOT EXISTS idx_ml_trade_signals_ticker_code ON ml_trade_signals(ticker_code);
CREATE INDEX IF NOT EXISTS idx_ml_trade_signals_created_at ON ml_trade_signals(created_at);
CREATE INDEX IF NOT EXISTS idx_ml_trade_signals_signal_type ON ml_trade_signals(signal_type);

CREATE INDEX IF NOT EXISTS idx_ml_signal_history_user_id ON ml_signal_history(user_id);
CREATE INDEX IF NOT EXISTS idx_ml_signal_history_asset_id ON ml_signal_history(asset_id);
CREATE INDEX IF NOT EXISTS idx_ml_signal_history_ticker_code ON ml_signal_history(ticker_code);
CREATE INDEX IF NOT EXISTS idx_ml_signal_history_original_signal ON ml_signal_history(original_signal_type);
CREATE INDEX IF NOT EXISTS idx_ml_signal_history_was_correct ON ml_signal_history(was_correct);

CREATE INDEX IF NOT EXISTS idx_ml_ticker_stats_ticker_code ON ml_ticker_stats(ticker_code);

CREATE INDEX IF NOT EXISTS idx_ml_model_metrics_user_id ON ml_model_metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_ml_model_metrics_model_name ON ml_model_metrics(model_name);
CREATE INDEX IF NOT EXISTS idx_ml_model_metrics_asset_id ON ml_model_metrics(asset_id);

CREATE INDEX IF NOT EXISTS idx_ml_email_notifications_user_id ON ml_email_notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_ml_email_notifications_status ON ml_email_notifications(status);
CREATE INDEX IF NOT EXISTS idx_ml_email_notifications_created_at ON ml_email_notifications(created_at);

-- Enable Row Level Security
ALTER TABLE ml_trade_signals ENABLE ROW LEVEL SECURITY;
ALTER TABLE ml_signal_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE ml_model_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE ml_user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE ml_email_notifications ENABLE ROW LEVEL SECURITY;

-- RLS Policies
-- Users can only see their own signals (using auth.uid() to match against profiles.id)
CREATE POLICY "Users can view own trade signals" ON ml_trade_signals
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE profiles.user_id = ml_trade_signals.user_id 
            AND profiles.id = auth.uid()
        )
    );

CREATE POLICY "Users can view own signal history" ON ml_signal_history
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE profiles.user_id = ml_signal_history.user_id 
            AND profiles.id = auth.uid()
        )
    );

CREATE POLICY "Users can view own model metrics" ON ml_model_metrics
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE profiles.user_id = ml_model_metrics.user_id 
            AND profiles.id = auth.uid()
        )
    );

CREATE POLICY "Users can manage own preferences" ON ml_user_preferences
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE profiles.user_id = ml_user_preferences.user_id 
            AND profiles.id = auth.uid()
        )
    );

CREATE POLICY "Users can view own email notifications" ON ml_email_notifications
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE profiles.user_id = ml_email_notifications.user_id 
            AND profiles.id = auth.uid()
        )
    );

-- Service role policies (for backend/DS service access)
CREATE POLICY "Service role can manage all trade signals" ON ml_trade_signals
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role can manage all signal history" ON ml_signal_history
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role can manage all model metrics" ON ml_model_metrics
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role can manage all email notifications" ON ml_email_notifications
    FOR ALL USING (auth.role() = 'service_role');

-- Function to calculate signal correctness (called during retroactive analysis)
CREATE OR REPLACE FUNCTION evaluate_signal_correctness(
    p_signal_id UUID,
    p_price_4h_later DECIMAL
) RETURNS BOOLEAN AS $$
DECLARE
    v_signal RECORD;
    v_was_correct BOOLEAN;
BEGIN
    SELECT * INTO v_signal FROM ml_trade_signals WHERE id = p_signal_id;
    
    IF v_signal.signal_type = 'sell' THEN
        v_was_correct := p_price_4h_later < v_signal.price_at_signal;
    ELSIF v_signal.signal_type = 'buy' THEN
        v_was_correct := p_price_4h_later > v_signal.price_at_signal;
    ELSE
        v_was_correct := NULL;
    END IF;
    
    RETURN v_was_correct;
END;
$$ LANGUAGE plpgsql;

-- Function to get users with active buy/sell signals (for email queue)
-- Now joins with profiles table to get email and uses integer user_id
CREATE OR REPLACE FUNCTION get_users_with_active_signals()
RETURNS TABLE (
    user_id BIGINT,
    email TEXT,
    asset_id BIGINT,
    ticker_code VARCHAR(20),
    is_crypto BOOLEAN,
    signal_type VARCHAR(10),
    price_at_signal DECIMAL,
    confidence_score DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.user_id,
        p.email,
        s.asset_id,
        s.ticker_code,
        s.is_crypto,
        s.signal_type,
        s.price_at_signal,
        s.confidence_score
    FROM ml_trade_signals s
    JOIN profiles p ON s.user_id = p.user_id
    WHERE s.is_active = TRUE
    AND s.expires_at > NOW();
END;
$$ LANGUAGE plpgsql;

-- Function to compute and update ticker statistics
-- Should be run periodically (e.g., nightly) to update success rates
CREATE OR REPLACE FUNCTION compute_ticker_stats()
RETURNS void AS $$
DECLARE
    ticker_row RECORD;
BEGIN
    FOR ticker_row IN
        SELECT 
            ticker_code,
            is_crypto,
            COUNT(*) as total_signals,
            SUM(CASE WHEN was_correct = true THEN 1 ELSE 0 END) as correct_signals,
            AVG(profit_loss_percent) as avg_profit_loss,
            SUM(CASE WHEN original_signal_type = 'buy' THEN 1 ELSE 0 END) as buy_signals,
            SUM(CASE WHEN original_signal_type = 'buy' AND was_correct = true THEN 1 ELSE 0 END) as buy_correct,
            SUM(CASE WHEN original_signal_type = 'sell' THEN 1 ELSE 0 END) as sell_signals,
            SUM(CASE WHEN original_signal_type = 'sell' AND was_correct = true THEN 1 ELSE 0 END) as sell_correct
        FROM ml_signal_history
        WHERE was_correct IS NOT NULL
        GROUP BY ticker_code, is_crypto
    LOOP
        INSERT INTO ml_ticker_stats (
            ticker_code,
            is_crypto,
            total_signals,
            correct_signals,
            success_rate,
            avg_profit_loss,
            buy_signals,
            buy_correct,
            sell_signals,
            sell_correct,
            last_calculated_at
        ) VALUES (
            ticker_row.ticker_code,
            ticker_row.is_crypto,
            ticker_row.total_signals,
            ticker_row.correct_signals,
            CASE 
                WHEN ticker_row.total_signals > 0 
                THEN ticker_row.correct_signals::DECIMAL / ticker_row.total_signals 
                ELSE 0 
            END,
            ticker_row.avg_profit_loss,
            ticker_row.buy_signals,
            ticker_row.buy_correct,
            ticker_row.sell_signals,
            ticker_row.sell_correct,
            NOW()
        )
        ON CONFLICT (ticker_code) DO UPDATE SET
            total_signals = EXCLUDED.total_signals,
            correct_signals = EXCLUDED.correct_signals,
            success_rate = EXCLUDED.success_rate,
            avg_profit_loss = EXCLUDED.avg_profit_loss,
            buy_signals = EXCLUDED.buy_signals,
            buy_correct = EXCLUDED.buy_correct,
            sell_signals = EXCLUDED.sell_signals,
            sell_correct = EXCLUDED.sell_correct,
            last_calculated_at = EXCLUDED.last_calculated_at;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
