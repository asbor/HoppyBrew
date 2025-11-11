# Fermentation Temperature Control Integration

This document describes the integration of temperature controllers (Tilt Hydrometer and iSpindel) for automated fermentation monitoring in HoppyBrew.

## Overview

HoppyBrew supports automatic fermentation data collection from:
- **iSpindel**: WiFi-enabled digital hydrometer
- **Tilt Hydrometer**: Bluetooth hydrometer (via Tilt Pi or cloud)

Readings are automatically imported every 15 minutes, and temperature alerts can be configured to notify when fermentation temperatures are outside safe ranges.

## Features

### 1. Device Configuration
- Create and manage device configurations in HoppyBrew
- Support for multiple devices simultaneously
- Device-specific calibration data
- Alert threshold configuration
- Active/inactive status control

### 2. Automatic Data Import
- Webhook endpoints for real-time data push (iSpindel, Tilt Pi)
- Background polling for cloud-based services (Tilt Cloud)
- Default 15-minute polling interval (configurable)
- Automatic duplicate detection
- Last reading timestamp tracking

### 3. Temperature Alerts
- Configurable min/max temperature thresholds
- Automatic alert checking on data ingestion
- Alert severity levels
- Enable/disable alerts per device

### 4. Batch Association
- Link devices to active batches
- Automatic reading assignment to correct batch
- Manual override (dissociate device from batch)
- View devices associated with each batch

### 5. Chart Integration
- Device readings appear in fermentation charts
- Source tracking (manual vs. automatic readings)
- Temperature, gravity, and pH visualization

## Setup Instructions

### iSpindel Setup

1. **Configure iSpindel Device in HoppyBrew**
   ```json
   {
     "name": "My iSpindel",
     "device_type": "ispindel",
     "description": "iSpindel for IPA fermentation",
     "api_token": "your-secret-token",
     "calibration_data": {
       "polynomial": [0.0, 0.0, 0.0, 1.0]
     },
     "configuration": {
       "update_interval": 900
     },
     "alert_config": {
       "enable_alerts": true,
       "temperature_min": 16.0,
       "temperature_max": 22.0
     }
   }
   ```

2. **Configure iSpindel Hardware**
   - Set iSpindel to send data to: `https://your-hoppybrew-server.com/devices/ispindel/data`
   - Add custom HTTP header: `X-API-Key: your-secret-token`
   - Set update interval to 900 seconds (15 minutes)

3. **Associate with Batch**
   - In HoppyBrew UI, go to the batch details
   - Click "Associate Device"
   - Select your iSpindel device
   - Data will automatically flow into the batch

### Tilt Hydrometer Setup

#### Option 1: Tilt Pi (Real-time Push)

1. **Configure Tilt Device in HoppyBrew**
   ```json
   {
     "name": "Tilt Red",
     "device_type": "tilt",
     "api_token": "your-secret-token",
     "alert_config": {
       "enable_alerts": true,
       "temperature_min": 16.0,
       "temperature_max": 22.0
     }
   }
   ```

2. **Configure Tilt Pi**
   - Add webhook URL: `https://your-hoppybrew-server.com/devices/tilt/data`
   - Add HTTP header: `X-API-Key: your-secret-token`
   - Tilt Pi will push data automatically

#### Option 2: Tilt Cloud (Polling)

1. **Configure Tilt Device with Cloud Settings**
   ```json
   {
     "name": "Tilt Red",
     "device_type": "tilt",
     "api_token": "your-tilt-cloud-api-token",
     "configuration": {
       "cloud_url": "https://cloud.tilthydrometer.com",
       "hydrometer_id": "your-hydrometer-id"
     },
     "alert_config": {
       "enable_alerts": true,
       "temperature_min": 16.0,
       "temperature_max": 22.0
     }
   }
   ```

2. **HoppyBrew Will Poll Automatically**
   - Background task polls every 15 minutes
   - No additional configuration needed
   - Data appears in your batch automatically

## API Endpoints

### Device Management
- `GET /devices` - List all devices
- `POST /devices` - Create new device
- `GET /devices/{id}` - Get device details
- `PUT /devices/{id}` - Update device
- `DELETE /devices/{id}` - Delete device

### Device-Batch Association
- `POST /devices/{device_id}/batch/{batch_id}/associate` - Link device to batch
- `DELETE /devices/{device_id}/batch` - Unlink device from batch (manual override)

### Data Ingestion (Webhooks)
- `POST /devices/ispindel/data` - Receive iSpindel data
- `POST /devices/tilt/data` - Receive Tilt data

### Example iSpindel Data Format
```json
{
  "name": "iSpindel000",
  "ID": 1234567,
  "angle": 45.2,
  "temperature": 20.5,
  "temp_units": "C",
  "battery": 3.8,
  "gravity": 1.048,
  "interval": 900,
  "RSSI": -75
}
```

### Example Tilt Data Format
```json
{
  "Color": "Red",
  "Temp": 68,
  "SG": 1.048,
  "Timepoint": "2024-03-21T14:30:00Z",
  "Comment": "",
  "Beer": "My IPA"
}
```

## Database Schema

### New Fields in `fermentation_readings`
- `device_id` (Integer, nullable): Links reading to device
- `source` (String): Indicates reading source ("manual", "ispindel", "tilt")

### New Fields in `devices`
- `batch_id` (Integer, nullable): Active batch association
- `alert_config` (JSON): Temperature alert configuration
- `last_reading_at` (DateTime): Last data receipt timestamp

## Temperature Alert Configuration

Alert configuration is stored in the device's `alert_config` JSON field:

```json
{
  "enable_alerts": true,
  "temperature_min": 16.0,
  "temperature_max": 22.0
}
```

When a reading is received:
1. Temperature is checked against thresholds
2. Alerts are generated if outside range
3. Alert messages include severity level
4. Future: notifications can be sent via email/webhook

## Manual Override

To stop automatic data collection from a device:

```bash
# Via API
DELETE /devices/{device_id}/batch

# Via UI
# Go to batch details -> Associated Devices -> Click "Dissociate"
```

This is useful when:
- Fermentation is complete
- Device needs maintenance
- Switching device to different batch

## Background Polling

The device poller runs automatically on HoppyBrew startup:
- Checks all active devices every 15 minutes
- Only polls devices with `batch_id` assigned
- Polls Tilt Cloud API (when configured)
- Avoids duplicate readings
- Updates `last_reading_at` timestamp

To modify poll interval, set environment variable:
```bash
DEVICE_POLL_INTERVAL=900  # seconds (default: 900 = 15 minutes)
```

## Troubleshooting

### Device Not Receiving Data

1. **Check device is active**
   ```bash
   GET /devices/{id}
   # Verify is_active = true
   ```

2. **Check batch association**
   ```bash
   GET /devices/{id}
   # Verify batch_id is set
   ```

3. **Check API token**
   - Ensure device hardware has correct token
   - Verify token in HTTP headers

4. **Check logs**
   ```bash
   docker logs hoppybrew-backend | grep -i device
   ```

### No Alerts Triggering

1. **Check alert_config**
   ```bash
   GET /devices/{id}
   # Verify alert_config.enable_alerts = true
   ```

2. **Check thresholds**
   - Ensure min/max temperatures are reasonable
   - Temperature must be outside range to trigger alert

### Duplicate Readings

The system automatically prevents duplicates by checking:
- Same batch_id
- Same device_id
- Same timestamp

If you see duplicates, check that device timestamps are accurate.

## Security Considerations

1. **API Tokens**: Store securely, don't commit to git
2. **HTTPS**: Always use HTTPS for webhook endpoints
3. **Token Rotation**: Regularly rotate API tokens
4. **Network Security**: Ensure devices are on secure network

## Future Enhancements

- [ ] Email/webhook notifications for alerts
- [ ] SMS notifications
- [ ] Historical alert log
- [ ] Device battery monitoring alerts
- [ ] Multiple alert rules per device
- [ ] Alert acknowledgment system
- [ ] Device health monitoring dashboard
- [ ] Auto-calibration suggestions

## Support

For issues or questions:
- GitHub Issues: https://github.com/asbor/HoppyBrew/issues
- Documentation: https://github.com/asbor/HoppyBrew/wiki

## Related Issues

- Issue #7: Fermentation Temperature Control Integration
- Issue #2: Base fermentation monitoring (dependency)
