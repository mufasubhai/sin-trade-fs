-- Migration versioning system for SinTrade ML Trading Schema
-- This file tracks migration versions and ensures proper upgrade order

-- Table to track applied migrations
CREATE TABLE IF NOT EXISTS ml_migration_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- Insert initial schema version
INSERT INTO ml_migration_versions (version, description, checksum)
VALUES ('1.0.0', 'Initial ML trading schema with buy/sell/hold signals', 'initial-schema-v1')
ON CONFLICT (version) DO NOTHING;

-- Insert ensemble strategy support version
INSERT INTO ml_migration_versions (version, description, checksum)
VALUES ('1.1.0', 'Add ensemble strategy support with model weights and feature importance', 'ensemble-strategy-v1')
ON CONFLICT (version) DO NOTHING;

-- Create function to check current migration version
CREATE OR REPLACE FUNCTION get_current_migration_version()
RETURNS VARCHAR(50) AS $$
DECLARE
    current_version VARCHAR(50);
BEGIN
    SELECT version INTO current_version 
    FROM ml_migration_versions 
    ORDER BY applied_at DESC 
    LIMIT 1;
    
    RETURN COALESCE(current_version, '0.0.0');
END;
$$ LANGUAGE plpgsql;

-- Create function to apply migration with version tracking
CREATE OR REPLACE FUNCTION apply_migration(
    p_version VARCHAR,
    p_description TEXT,
    p_checksum VARCHAR
) RETURNS BOOLEAN AS $$
DECLARE
    already_applied BOOLEAN;
BEGIN
    SELECT EXISTS(
        SELECT 1 FROM ml_migration_versions WHERE version = p_version
    ) INTO already_applied;
    
    IF NOT already_applied THEN
        INSERT INTO ml_migration_versions (version, description, checksum)
        VALUES (p_version, p_description, p_checksum);
        
        RETURN TRUE;
    END IF;
    
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Create function to verify migration dependencies
CREATE OR REPLACE FUNCTION verify_migration_dependencies()
RETURNS TABLE (
    version VARCHAR,
    description TEXT,
    status VARCHAR,
    missing_dependency VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        mv.version,
        mv.description,
        CASE
            WHEN mv.version = '1.0.0' THEN 'OK'
            WHEN mv.version = '1.1.0' AND EXISTS(SELECT 1 FROM ml_migration_versions WHERE version = '1.0.0') THEN 'OK'
            ELSE 'PENDING'
        END as status,
        CASE
            WHEN mv.version = '1.1.0' AND NOT EXISTS(SELECT 1 FROM ml_migration_versions WHERE version = '1.0.0') THEN '1.0.0'
            ELSE NULL
        END as missing_dependency
    FROM ml_migration_versions mv
    ORDER BY mv.applied_at;
END;
$$ LANGUAGE plpgsql;
