-- Add last_purchased column to user_assets table
-- Run this in Supabase SQL Editor

ALTER TABLE user_assets 
ADD COLUMN IF NOT EXISTS last_purchased TIMESTAMP WITH TIME ZONE;

-- Add index for faster queries
CREATE INDEX IF NOT EXISTS idx_user_assets_last_purchased ON user_assets(last_purchased);
