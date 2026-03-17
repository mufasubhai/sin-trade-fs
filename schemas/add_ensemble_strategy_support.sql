-- Migration to support ensemble ML trading strategy
-- Adds model_weights column and updates model_metrics table
-- Run this after ml_trading_schema.sql

-- Add model_weights JSONB column if not exists
ALTER TABLE ml_model_metrics 
ADD COLUMN IF NOT EXISTS model_weights JSONB;

-- Add feature importance tracking
ALTER TABLE ml_model_metrics 
ADD COLUMN IF NOT EXISTS feature_importance JSONB;

-- Index on ml_signal_history.signal_id for faster lookups during signal evaluation
CREATE INDEX IF NOT EXISTS idx_ml_signal_history_signal_id ON ml_signal_history(signal_id);

-- Create a view to track model performance over time
CREATE OR REPLACE VIEW ml_model_performance_history AS
SELECT 
    id,
    user_id,
    model_name,
    model_version,
    asset_id,
    accuracy,
    precision_score,
    recall_score,
    f1_score,
    total_signals,
    correct_signals,
    avg_profit_loss,
    time_period_start,
    time_period_end,
    created_at,
    updated_at,
    training_data_points,
    hyperparameters,
    feature_importance,
    model_weights,
    notes,
    -- Additional computed fields
    CASE 
        WHEN total_signals > 0 THEN (correct_signals::FLOAT / total_signals) 
        ELSE NULL 
    END as calculated_accuracy,
    CASE 
        WHEN accuracy IS NOT NULL THEN 
            CASE 
                WHEN accuracy > 0.8 THEN 'Excellent'
                WHEN accuracy > 0.7 THEN 'Good'
                WHEN accuracy > 0.6 THEN 'Fair'
                ELSE 'Poor'
            END 
        ELSE 'Not Evaluated' 
    END as performance_rating
FROM ml_model_metrics 
ORDER BY time_period_end DESC, created_at DESC;

-- Note: Indexes cannot be created on views. Query the underlying ml_model_metrics table with appropriate indexes instead.
-- Existing indexes on ml_model_metrics will be used for view queries.

-- Function to analyze model performance trends
CREATE OR REPLACE FUNCTION analyze_model_performance()
RETURNS TABLE (
    model_name VARCHAR,
    total_evaluations INTEGER,
    avg_accuracy DECIMAL(5,4),
    best_accuracy DECIMAL(5,4),
    worst_accuracy DECIMAL(5,4),
    accuracy_trend VARCHAR,
    most_recent_accuracy DECIMAL(5,4),
    most_recent_version VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.model_name,
        COUNT(*)::INTEGER as total_evaluations,
        AVG(m.accuracy)::DECIMAL(5,4) as avg_accuracy,
        MAX(m.accuracy)::DECIMAL(5,4) as best_accuracy,
        MIN(m.accuracy)::DECIMAL(5,4) as worst_accuracy,
        CASE 
            WHEN AVG(m.accuracy) > (SELECT AVG(accuracy) FROM ml_model_metrics WHERE accuracy IS NOT NULL) 
            THEN 'Improving'
            WHEN AVG(m.accuracy) < (SELECT AVG(accuracy) FROM ml_model_metrics WHERE accuracy IS NOT NULL) 
            THEN 'Declining'
            ELSE 'Stable' 
        END as accuracy_trend,
        (SELECT m2.accuracy FROM ml_model_metrics m2 WHERE m2.model_name = m.model_name AND m2.accuracy IS NOT NULL ORDER BY m2.time_period_end DESC LIMIT 1)::DECIMAL(5,4) as most_recent_accuracy,
        (SELECT m2.model_version FROM ml_model_metrics m2 WHERE m2.model_name = m.model_name ORDER BY m2.time_period_end DESC LIMIT 1)::VARCHAR as most_recent_version
    FROM ml_model_metrics m
    WHERE m.accuracy IS NOT NULL
    GROUP BY m.model_name
    ORDER BY avg_accuracy DESC;
END;
$$ LANGUAGE plpgsql;
