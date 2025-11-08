# Temperature Controller Integration Guide

This document describes the temperature controller integration feature for automated fermentation monitoring in HoppyBrew.

## Overview

HoppyBrew integrates with popular temperature controller devices to automatically import fermentation readings, monitor temperature and gravity, and trigger alerts. The system supports:

- **Tilt Hydrometer**: Bluetooth-based hydrometer with cloud/local bridge support
- **iSpindel**: WiFi-based open-source smart hydrometer

## Features

### 1. Automatic Data Import

Devices can automatically push data to HoppyBrew via webhook endpoints. The system:
- Receives readings every 15 minutes (configurable per device)
- Stores readings with device attribution
- Updates device last import timestamp
- Monitors for missing data

### 2. Temperature Alerts

Configure alert thresholds per device:
```json
{
  "temp_min": 18.0,
  "temp_max": 22.0,
  "notification_enabled": true,
  "missing_data_alert": true
}
```

Alerts are checked on every reading import and available via API query.

### 3. Manual Override

When manual control is needed:
- Enable `manual_override` flag on device
- Device stops accepting automatic readings
- Use manual reading endpoint to add data

### 4. Chart Integration

Fermentation charts show:
- Data source for each reading (manual, tilt, ispindel)
- Device attribution
- Visual indicators for device data vs manual entries

## API Endpoints

### Device Management

**Create Device**
```
POST /devices
```
```json
{
  "name": "My Tilt Red",
  "device_type": "tilt",
  "batch_id": 1,
  "auto_import_enabled": true,
  "import_interval_seconds": 900,
  "alert_config": {
    "temp_min": 18.0,
    "temp_max": 22.0
  },
  "is_active": true
}
```

**Update Device**
```
PUT /devices/{device_id}
```

**Associate Device with Batch**
```
PUT /devices/{device_id}
{
  "batch_id": 123
}
```

### Webhook Endpoints

**Tilt Webhook**
```
POST /temperature-controllers/tilt/webhook/{device_id}
```
```json
{
  "color": "Red",
  "temp_fahrenheit": 68.5,
  "temp_celsius": 20.3,
  "gravity": 1.048,
  "rssi": -45
}
```

**iSpindel Webhook**
```
POST /temperature-controllers/ispindel/webhook/{device_id}
```
```json
{
  "name": "iSpindel001",
  "angle": 45.23,
  "temperature": 20.5,
  "battery": 3.87,
  "gravity": 1.050,
  "interval": 900,
  "RSSI": -62
}
```

### Alert Management

**Get Device Alerts**
```
GET /temperature-controllers/alerts/{device_id}
```

Response:
```json
{
  "device_id": 1,
  "batch_id": 42,
  "latest_reading": {
    "timestamp": "2024-03-21T14:30:00Z",
    "temperature": 19.5,
    "gravity": 1.048
  },
  "alerts": ["Temperature too low: 19.5°C < 20.0°C"],
  "alert_config": {
    "temp_min": 20.0,
    "temp_max": 22.0
  }
}
```

### Manual Operations

**Create Manual Reading**
```
POST /temperature-controllers/manual-reading/{device_id}
```
```json
{
  "timestamp": "2024-03-21T14:30:00Z",
  "gravity": 1.020,
  "temperature": 19.5,
  "notes": "Manual reading during maintenance"
}
```

**Get Batch Devices**
```
GET /temperature-controllers/batch/{batch_id}/devices
```

Returns all devices associated with a batch, including their status and latest readings.

### Scheduler Status

**Get Scheduler Status**
```
GET /temperature-controllers/scheduler/status
```

Returns information about the background scheduler that monitors devices.

## Setup Guide

### Tilt Hydrometer Setup

1. **Create Device in HoppyBrew**
   ```bash
   curl -X POST http://your-hoppybrew/devices \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Tilt Red",
       "device_type": "tilt",
       "is_active": true
     }'
   ```

2. **Associate with Batch**
   Update the device with the batch ID when you start fermentation.

3. **Configure Tilt Bridge/Cloud**
   - If using Tilt Cloud: Configure webhook URL to `http://your-hoppybrew/temperature-controllers/tilt/webhook/{device_id}`
   - If using local bridge (TiltPi, etc.): Configure to POST to the same endpoint

4. **Configure Alerts (Optional)**
   ```bash
   curl -X PUT http://your-hoppybrew/devices/{device_id} \
     -H "Content-Type: application/json" \
     -d '{
       "alert_config": {
         "temp_min": 18.0,
         "temp_max": 22.0,
         "notification_enabled": true
       }
     }'
   ```

### iSpindel Setup

1. **Create Device in HoppyBrew**
   ```bash
   curl -X POST http://your-hoppybrew/devices \
     -H "Content-Type: application/json" \
     -d '{
       "name": "iSpindel001",
       "device_type": "ispindel",
       "calibration_data": {
         "polynomial": [0.0, 0.001, 0.0, 1.0]
       },
       "is_active": true
     }'
   ```

2. **Configure iSpindel Device**
   - Access iSpindel configuration portal
   - Set HTTP endpoint: `http://your-hoppybrew/temperature-controllers/ispindel/webhook/{device_id}`
   - Set update interval: 900 seconds (15 minutes)

3. **Calibrate iSpindel**
   - Perform calibration according to iSpindel documentation
   - Update calibration polynomial in HoppyBrew:
     ```bash
     curl -X PUT http://your-hoppybrew/devices/{device_id} \
       -H "Content-Type: application/json" \
       -d '{
         "calibration_data": {
           "polynomial": [a0, a1, a2, a3]
         }
       }'
     ```

4. **Associate with Batch**
   Update the device with the batch ID when you start fermentation.

## Database Schema

### Device Table Extensions

```sql
ALTER TABLE devices ADD COLUMN batch_id INTEGER REFERENCES batches(id);
ALTER TABLE devices ADD COLUMN auto_import_enabled BOOLEAN DEFAULT TRUE;
ALTER TABLE devices ADD COLUMN import_interval_seconds INTEGER DEFAULT 900;
ALTER TABLE devices ADD COLUMN last_import_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE devices ADD COLUMN alert_config JSON;
ALTER TABLE devices ADD COLUMN manual_override BOOLEAN DEFAULT FALSE;
```

### Fermentation Readings Table Extensions

```sql
ALTER TABLE fermentation_readings ADD COLUMN device_id INTEGER REFERENCES devices(id);
ALTER TABLE fermentation_readings ADD COLUMN source VARCHAR(50) DEFAULT 'manual';
```

## Background Scheduler

The system includes a background scheduler that:
- Runs every 5 minutes
- Checks all active devices with auto_import_enabled
- Monitors for missing data (device hasn't sent data in expected interval)
- Logs warnings/alerts for devices not receiving data
- Can be extended to support pull-based device integrations

## Troubleshooting

### Device Not Receiving Data

1. Check device is active: `GET /devices/{device_id}`
2. Check manual_override is false
3. Check device is associated with a batch
4. Verify webhook URL is correct
5. Check device logs/configuration
6. Review HoppyBrew logs for error messages

### Alerts Not Triggering

1. Verify alert_config is set on device
2. Check readings are being created: `GET /batches/{batch_id}/fermentation/readings`
3. Query alerts endpoint: `GET /temperature-controllers/alerts/{device_id}`

### Calibration Issues (iSpindel)

1. Verify polynomial coefficients are correct
2. Test with known gravity samples
3. Update calibration_data on device
4. Readings will use new calibration immediately

## Security Considerations

- API tokens for devices should be encrypted (use `api_token_encrypted` field)
- Webhook endpoints should validate device ownership
- Consider adding authentication for webhook endpoints in production
- Rate limiting should be applied to webhook endpoints

## Future Enhancements

- Push notifications for alerts (email, SMS, webhook)
- Bluetooth integration for direct Tilt connection
- Additional device types (Plaato, BrewPi, etc.)
- Advanced alert rules (fermentation stuck detection, etc.)
- Historical device performance analytics
- Automatic batch stage transitions based on readings
