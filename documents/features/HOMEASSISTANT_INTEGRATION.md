# HomeAssistant Integration Guide

This guide explains how to integrate HoppyBrew with HomeAssistant for monitoring your brewing batches.

## Overview

HoppyBrew provides REST API endpoints that are compatible with HomeAssistant's RESTful sensor platform. This allows you to:

- Monitor active brewing batches
- Track fermentation progress
- View batch status and age
- Display brewery statistics on your HomeAssistant dashboard

## Quick Start

### Prerequisites

- HoppyBrew running and accessible from your HomeAssistant instance
- HomeAssistant with REST integration enabled (default)

### Basic Setup

Add the following to your HomeAssistant `configuration.yaml`:

```yaml
# Monitor all active batches
sensor:
  - platform: rest
    name: "HoppyBrew Active Batches"
    resource: http://your-hoppybrew-host:8000/api/homeassistant/summary
    value_template: "{{ value_json.active_batches }}"
    unit_of_measurement: "batches"
    icon: mdi:brewery
    json_attributes:
      - total_batches
      - brewing_batches
      - fermenting_batches
      - conditioning_batches
      - ready_batches
      - state
    scan_interval: 300  # Update every 5 minutes
```

After adding this configuration, restart HomeAssistant. You'll now have a sensor showing the number of active batches.

## Available Endpoints

### 1. Brewery Summary (`/api/homeassistant/summary`)

Returns overall brewery statistics.

**Response:**
```json
{
  "active_batches": 3,
  "total_batches": 3,
  "brewing_batches": 1,
  "fermenting_batches": 1,
  "conditioning_batches": 1,
  "ready_batches": 0,
  "state": "active",
  "icon": "mdi:brewery"
}
```

### 2. All Batches (`/api/homeassistant/batches`)

Returns all batches as individual sensors.

**Configuration:**
```yaml
sensor:
  - platform: rest
    name: "HoppyBrew Batches"
    resource: http://your-hoppybrew-host:8000/api/homeassistant/batches
    value_template: "{{ value_json | length }}"
    json_attributes_path: "$"
    json_attributes:
      - entity_id
      - name
      - state
      - attributes
    scan_interval: 300
```

### 3. Specific Batch (`/api/homeassistant/batches/{batch_id}`)

Monitor a specific batch by ID.

**Configuration:**
```yaml
sensor:
  - platform: rest
    name: "Current Brew - IPA"
    resource: http://your-hoppybrew-host:8000/api/homeassistant/batches/1
    value_template: "{{ value_json.state }}"
    icon: mdi:beer
    json_attributes_path: "$.attributes"
    json_attributes:
      - batch_name
      - batch_number
      - age_days
      - batch_size
      - brewer
      - brew_date
      - recipe_name
      - last_activity
    scan_interval: 300
```

## Batch States

HoppyBrew batches automatically progress through these states based on age:

| State | Age | Description |
|-------|-----|-------------|
| `brewing` | 0-1 days | Batch is currently being brewed |
| `fermenting` | 1-14 days | Active fermentation |
| `conditioning` | 14-28 days | Conditioning/aging |
| `ready` | 28+ days | Ready to package/serve |

## Advanced Configuration

### Creating Template Sensors

You can create template sensors for more complex monitoring:

```yaml
template:
  - sensor:
      - name: "Oldest Fermenting Batch"
        state: >
          {% set batches = state_attr('sensor.hoppybrew_batches', 'attributes') %}
          {% if batches %}
            {% set fermenting = batches | selectattr('state', 'eq', 'fermenting') | list %}
            {% if fermenting | length > 0 %}
              {{ fermenting | map(attribute='attributes.age_days') | max }}
            {% else %}
              0
            {% endif %}
          {% else %}
            0
          {% endif %}
        unit_of_measurement: "days"
        icon: mdi:clock-outline
```

### Dashboard Card Example

Create a custom dashboard card for monitoring batches:

```yaml
type: entities
title: HoppyBrew Brewery Status
entities:
  - entity: sensor.hoppybrew_active_batches
    name: Active Batches
  - type: attribute
    entity: sensor.hoppybrew_active_batches
    attribute: brewing_batches
    name: Currently Brewing
    icon: mdi:pot-steam
  - type: attribute
    entity: sensor.hoppybrew_active_batches
    attribute: fermenting_batches
    name: Fermenting
    icon: mdi:flask
  - type: attribute
    entity: sensor.hoppybrew_active_batches
    attribute: conditioning_batches
    name: Conditioning
    icon: mdi:barrel
  - type: attribute
    entity: sensor.hoppybrew_active_batches
    attribute: ready_batches
    name: Ready to Bottle
    icon: mdi:beer
```

### Multiple Batch Monitoring

To monitor multiple specific batches:

```yaml
sensor:
  - platform: rest
    name: "Batch 1 - IPA"
    resource: http://your-hoppybrew-host:8000/api/homeassistant/batches/1
    value_template: "{{ value_json.state }}"
    json_attributes_path: "$.attributes"
    json_attributes:
      - batch_name
      - age_days
    scan_interval: 300
    
  - platform: rest
    name: "Batch 2 - Stout"
    resource: http://your-hoppybrew-host:8000/api/homeassistant/batches/2
    value_template: "{{ value_json.state }}"
    json_attributes_path: "$.attributes"
    json_attributes:
      - batch_name
      - age_days
    scan_interval: 300
```

## Automation Examples

### Notify When Batch is Ready

```yaml
automation:
  - alias: "Notify when batch ready"
    trigger:
      - platform: state
        entity_id: sensor.current_brew_ipa
        to: "ready"
    action:
      - service: notify.mobile_app
        data:
          title: "Batch Ready!"
          message: "Your {{ state_attr('sensor.current_brew_ipa', 'batch_name') }} is ready to bottle!"
```

### Track Fermentation Duration

```yaml
automation:
  - alias: "Alert if fermentation too long"
    trigger:
      - platform: template
        value_template: >
          {{ state_attr('sensor.current_brew_ipa', 'age_days') | int > 21 and 
             states('sensor.current_brew_ipa') == 'fermenting' }}
    action:
      - service: notify.mobile_app
        data:
          title: "Fermentation Alert"
          message: "Batch has been fermenting for {{ state_attr('sensor.current_brew_ipa', 'age_days') }} days"
```

## Future MQTT Support

MQTT support is planned for future releases, which will enable:

- Real-time sensor data from devices like iSpindel
- Bidirectional communication for batch control
- Automatic sensor discovery via MQTT Discovery protocol
- Temperature and gravity monitoring during fermentation

The endpoint `/api/homeassistant/discovery/batch/{batch_id}` provides the MQTT discovery configuration format that will be supported.

## Troubleshooting

### Sensors Not Updating

1. Check that HoppyBrew is accessible: `curl http://your-hoppybrew-host:8000/api/health`
2. Verify the endpoint returns data: `curl http://your-hoppybrew-host:8000/api/homeassistant/summary`
3. Check HomeAssistant logs for REST sensor errors
4. Ensure `scan_interval` is set appropriately (default: 60 seconds)

### Connection Refused

- Verify HoppyBrew is running: `docker ps | grep hoppybrew`
- Check firewall rules allow HomeAssistant to access port 8000
- If using Docker, ensure containers are on the same network or ports are properly exposed

### Invalid JSON Response

- Ensure you're using the correct API version
- Check that batches exist in your HoppyBrew database
- Verify the `value_template` matches the expected response format

## API Reference

All HomeAssistant endpoints are documented in the interactive API documentation:
- Swagger UI: `http://your-hoppybrew-host:8000/docs`
- ReDoc: `http://your-hoppybrew-host:8000/redoc`

Look for the "homeassistant" tag in the API documentation.

## Example Complete Configuration

Here's a complete example showing all features:

```yaml
# configuration.yaml

sensor:
  # Overall brewery status
  - platform: rest
    name: "Brewery Status"
    resource: http://192.168.1.100:8000/api/homeassistant/summary
    value_template: "{{ value_json.active_batches }}"
    unit_of_measurement: "batches"
    icon: mdi:brewery
    json_attributes:
      - total_batches
      - brewing_batches
      - fermenting_batches
      - conditioning_batches
      - ready_batches
    scan_interval: 300

  # All batches list
  - platform: rest
    name: "All Batches"
    resource: http://192.168.1.100:8000/api/homeassistant/batches
    value_template: "{{ value_json | length }}"
    json_attributes_path: "$"
    json_attributes:
      - entity_id
      - name
      - state
      - attributes
    scan_interval: 300

  # Specific batch monitoring
  - platform: rest
    name: "Current Batch"
    resource: http://192.168.1.100:8000/api/homeassistant/batches/1
    value_template: "{{ value_json.state }}"
    json_attributes_path: "$.attributes"
    json_attributes:
      - batch_name
      - batch_number
      - batch_size
      - age_days
      - recipe_name
      - brewer
      - last_activity
    scan_interval: 300

# Template sensors for derived values
template:
  - sensor:
      - name: "Total Batch Volume"
        state: >
          {% set batches = state_attr('sensor.all_batches', 'attributes') %}
          {% if batches %}
            {{ batches | sum(attribute='attributes.batch_size') | round(1) }}
          {% else %}
            0
          {% endif %}
        unit_of_measurement: "L"
        icon: mdi:cup-water

# Automations
automation:
  - alias: "Batch Ready Notification"
    trigger:
      - platform: state
        entity_id: sensor.current_batch
        to: "ready"
    action:
      - service: notify.mobile_app
        data:
          title: "🍺 Batch Ready!"
          message: "{{ state_attr('sensor.current_batch', 'batch_name') }} is ready!"
```

## Support

For issues or feature requests related to HomeAssistant integration:
- GitHub Issues: https://github.com/asbor/HoppyBrew/issues
- Documentation: https://github.com/asbor/HoppyBrew

## Contributing

Contributions to improve HomeAssistant integration are welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
