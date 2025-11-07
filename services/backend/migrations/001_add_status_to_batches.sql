-- Migration: Add status column to batches table
-- Date: 2025-11-07
-- Description: Add status column to track batch workflow stages

-- Add status column with default value
ALTER TABLE batches 
ADD COLUMN IF NOT EXISTS status VARCHAR(50) NOT NULL DEFAULT 'planning';

-- Create index for status queries
CREATE INDEX IF NOT EXISTS ix_batches_status ON batches(status);

-- Update existing batches (if any) to have appropriate status
-- This is safe to run multiple times
UPDATE batches 
SET status = 'planning' 
WHERE status IS NULL OR status = '';

-- Valid status values (enforced by application):
-- - planning
-- - brew_day
-- - primary_fermentation
-- - secondary_fermentation
-- - conditioning
-- - packaged
-- - completed
-- - archived
