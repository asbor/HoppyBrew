-- Migration: Add fermentation_readings table
-- Date: 2025-11-08
-- Description: Create fermentation_readings table to track gravity, temperature, pH readings during fermentation

-- Create fermentation_readings table
CREATE TABLE IF NOT EXISTS fermentation_readings (
    id SERIAL PRIMARY KEY,
    batch_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    gravity FLOAT,
    temperature FLOAT,
    ph FLOAT,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fermentation_readings_batch
        FOREIGN KEY (batch_id)
        REFERENCES batches(id)
        ON DELETE CASCADE
);

-- Create indexes for efficient querying
CREATE INDEX IF NOT EXISTS ix_fermentation_readings_batch_id 
    ON fermentation_readings(batch_id);

CREATE INDEX IF NOT EXISTS ix_fermentation_readings_timestamp 
    ON fermentation_readings(timestamp);

CREATE INDEX IF NOT EXISTS ix_fermentation_readings_batch_timestamp 
    ON fermentation_readings(batch_id, timestamp);

-- Add comment to table
COMMENT ON TABLE fermentation_readings IS 'Stores fermentation readings including gravity, temperature, and pH measurements taken during the fermentation process';
COMMENT ON COLUMN fermentation_readings.batch_id IS 'Foreign key reference to the batch being monitored';
COMMENT ON COLUMN fermentation_readings.timestamp IS 'When the reading was taken';
COMMENT ON COLUMN fermentation_readings.gravity IS 'Specific gravity reading (e.g., 1.048)';
COMMENT ON COLUMN fermentation_readings.temperature IS 'Temperature in degrees (Celsius or Fahrenheit)';
COMMENT ON COLUMN fermentation_readings.ph IS 'pH level of the fermenting beer';
COMMENT ON COLUMN fermentation_readings.notes IS 'Additional notes about the reading or fermentation state';
COMMENT ON COLUMN fermentation_readings.created_at IS 'When the reading record was created in the database';
