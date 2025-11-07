# Home Assistant Integration Enhancement Plan

**Date**: November 5, 2025  
**Current State**: Basic REST API integration exists  
**Target State**: Full MQTT integration with device support  
**Priority**: P2 (Weeks 25-28 in roadmap)

---

## 📋 Current State Analysis

### What Works Today ✅
1. **REST API Endpoints** (Implemented):
   - `/api/homeassistant/summary` - Overall brewery statistics
   - `/api/homeassistant/batches` - All batches list
   - `/api/homeassistant/batches/{id}` - Specific batch details
   - `/api/homeassistant/discovery/batch/{id}` - MQTT discovery format (endpoint exists but MQTT not implemented)

2. **Documentation**:
   - Comprehensive HOMEASSISTANT_INTEGRATION.md exists
   - Example configurations for REST sensors
   - Dashboard card examples
   - Automation examples

3. **Batch States**:
   - States defined (brewing, fermenting, conditioning, ready)
   - Basic state transitions (but not automated)

### What's Missing ❌
1. **MQTT Integration**: No MQTT broker connection, no publishing
2. **Real-time Updates**: Polling only (REST), no push updates
3. **Device Integrations**: No iSpindel, Tilt, or other device support
4. **MQTT Discovery**: Endpoint exists but not functional
5. **Bi-directional Control**: Can't control HoppyBrew from HA
6. **Automated State Updates**: Batch states don't auto-progress
7. **Sensor Data Ingestion**: Can't receive data from HA sensors
8. **WebSocket Support**: No real-time communication

---

## 🎯 Enhancement Goals

### Primary Objectives
1. **MQTT Broker Integration**: Connect to MQTT broker and maintain connection
2. **MQTT Discovery Protocol**: Auto-discovery of all sensors in Home Assistant
3. **Real-time Sensor Updates**: Publish all state changes via MQTT
4. **Device Integration Framework**: Support iSpindel, Tilt, and other devices
5. **Bi-directional Communication**: Receive commands from Home Assistant
6. **WebSocket Support**: Real-time updates for web dashboard

### Success Criteria
- [ ] All batch state changes published to MQTT within 1 second
- [ ] HA auto-discovers all HoppyBrew sensors without manual config
- [ ] iSpindel data automatically logged to fermentation readings
- [ ] Temperature alerts triggered via HA automations
- [ ] Fermentation progress visible in HA dashboard
- [ ] Can start/stop batch tracking from HA
- [ ] WebSocket updates visible in HoppyBrew UI without refresh

---

## 🏗️ Architecture Design

### MQTT Topic Structure
```
hoppybrew/
├── brewery/
│   ├── status                          # overall brewery status
│   ├── active_batches                  # count of active batches
│   └── next_brew_date                  # next scheduled brew
├── batch/
│   ├── {batch_id}/
│   │   ├── state                       # current batch state
│   │   ├── name                        # batch name
│   │   ├── status                      # brewing/fermenting/etc
│   │   ├── age_days                    # days since brew date
│   │   ├── fermentation/
│   │   │   ├── gravity                 # current gravity
│   │   │   ├── temperature             # current beer temp
│   │   │   ├── attenuation             # current attenuation %
│   │   │   └── days_fermenting         # days in fermentation
│   │   └── recipe/
│   │       ├── name                    # recipe name
│   │       ├── style                   # beer style
│   │       ├── target_og               # target OG
│   │       └── target_fg               # target FG
├── devices/
│   ├── {device_id}/
│   │   ├── status                      # online/offline
│   │   ├── battery                     # battery level
│   │   ├── gravity                     # current gravity reading
│   │   ├── temperature                 # current temperature
│   │   ├── tilt                        # tilt angle (for Tilt devices)
│   │   └── signal                      # WiFi/BT signal strength
├── inventory/
│   ├── low_stock                       # list of low stock items
│   ├── expiring                        # list of expiring items
│   └── value                           # total inventory value
└── alerts/
    ├── temperature                     # temperature out of range
    ├── stuck_fermentation              # fermentation stuck alert
    └── low_stock                       # ingredient low stock alert
```

### MQTT Discovery Payloads

Example for batch sensor:
```json
{
  "name": "HoppyBrew Batch 001",
  "unique_id": "hoppybrew_batch_001",
  "state_topic": "hoppybrew/batch/001/state",
  "json_attributes_topic": "hoppybrew/batch/001/attributes",
  "device": {
    "identifiers": ["hoppybrew_batch_001"],
    "name": "Batch: American IPA",
    "model": "HoppyBrew Batch",
    "manufacturer": "HoppyBrew",
    "sw_version": "1.0.0"
  },
  "icon": "mdi:beer",
  "availability_topic": "hoppybrew/status"
}
```

### WebSocket Protocol

```
ws://hoppybrew:8000/ws

Message Types:
1. Subscribe to batch updates:
   { "type": "subscribe", "entity": "batch", "id": "001" }

2. Batch update event:
   { "type": "batch_update", "id": "001", "data": {...} }

3. Fermentation reading event:
   { "type": "fermentation_reading", "batch_id": "001", "reading": {...} }

4. Device data event:
   { "type": "device_data", "device_id": "ispindel_001", "data": {...} }

5. Alert event:
   { "type": "alert", "level": "warning", "message": "Temperature high" }
```

---

## 🔧 Implementation Details

### Phase 1: MQTT Foundation (Week 1)

#### Backend Changes

**1. Add Dependencies**
```python
# requirements.txt
paho-mqtt==1.6.1
python-socketio==5.10.0
aiofiles==23.2.1
```

**2. Create MQTT Configuration**
```python
# services/backend/config.py (additions)
class Settings(BaseSettings):
    # ... existing settings ...
    
    # MQTT Configuration
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None
    MQTT_CLIENT_ID: str = "hoppybrew"
    MQTT_TOPIC_PREFIX: str = "hoppybrew"
    MQTT_QOS: int = 1
    MQTT_RETAIN: bool = True
    MQTT_KEEPALIVE: int = 60
    MQTT_RECONNECT_DELAY: int = 5
```

**3. Create MQTT Service**
```python
# services/backend/services/mqtt_service.py
import paho.mqtt.client as mqtt
import json
from typing import Optional, Dict, Any
from config import settings

class MQTTService:
    def __init__(self):
        self.client = None
        self.connected = False
        
    def connect(self):
        """Connect to MQTT broker"""
        self.client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID)
        
        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(
                settings.MQTT_USERNAME, 
                settings.MQTT_PASSWORD
            )
        
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        
        try:
            self.client.connect(
                settings.MQTT_BROKER_HOST,
                settings.MQTT_BROKER_PORT,
                settings.MQTT_KEEPALIVE
            )
            self.client.loop_start()
        except Exception as e:
            logger.error(f"MQTT connection failed: {e}")
            
    def _on_connect(self, client, userdata, flags, rc):
        """Handle connection"""
        if rc == 0:
            self.connected = True
            logger.info("Connected to MQTT broker")
            self.publish_status("online")
        else:
            logger.error(f"MQTT connection failed with code {rc}")
            
    def _on_disconnect(self, client, userdata, rc):
        """Handle disconnection"""
        self.connected = False
        logger.warning("Disconnected from MQTT broker")
        
    def publish(self, topic: str, payload: Any, retain: bool = None):
        """Publish message to topic"""
        if not self.connected:
            logger.warning("MQTT not connected, message not published")
            return False
            
        topic_full = f"{settings.MQTT_TOPIC_PREFIX}/{topic}"
        retain_flag = retain if retain is not None else settings.MQTT_RETAIN
        
        payload_json = json.dumps(payload) if isinstance(payload, dict) else str(payload)
        
        result = self.client.publish(
            topic_full,
            payload_json,
            qos=settings.MQTT_QOS,
            retain=retain_flag
        )
        
        return result.rc == 0
        
    def publish_discovery(self, entity_type: str, entity_id: str, config: Dict):
        """Publish Home Assistant MQTT discovery"""
        discovery_topic = f"homeassistant/{entity_type}/{settings.MQTT_CLIENT_ID}_{entity_id}/config"
        self.client.publish(discovery_topic, json.dumps(config), qos=1, retain=True)
        
    def publish_status(self, status: str):
        """Publish broker status"""
        self.publish("status", status, retain=True)

# Global MQTT service instance
mqtt_service = MQTTService()
```

**4. Initialize MQTT on Startup**
```python
# services/backend/main.py (additions)
from services.mqtt_service import mqtt_service

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    # ... existing startup code ...
    
    # Connect to MQTT broker
    mqtt_service.connect()
    logger.info("MQTT service initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    mqtt_service.publish_status("offline")
    mqtt_service.client.loop_stop()
    mqtt_service.client.disconnect()
    logger.info("MQTT service stopped")
```

#### Tasks - Phase 1
- [ ] Add paho-mqtt to requirements.txt
- [ ] Add MQTT settings to config.py
- [ ] Create mqtt_service.py with MQTTService class
- [ ] Add MQTT initialization to main.py startup
- [ ] Add connection health check endpoint
- [ ] Add MQTT configuration to .env.example
- [ ] Test MQTT connection to broker
- [ ] Add logging for MQTT events

---

### Phase 2: Batch State Publishing (Week 1)

#### Backend Changes

**1. Create MQTT Publisher Functions**
```python
# services/backend/services/mqtt_publishers.py
from services.mqtt_service import mqtt_service
from datetime import datetime

def publish_batch_state(batch):
    """Publish batch state to MQTT"""
    # Main state topic
    mqtt_service.publish(
        f"batch/{batch.id}/state",
        batch.status
    )
    
    # Attributes topic
    attributes = {
        "batch_id": batch.id,
        "batch_name": batch.batch_name,
        "batch_number": batch.batch_number,
        "status": batch.status,
        "brew_date": batch.brew_date.isoformat() if batch.brew_date else None,
        "recipe_name": batch.recipe.name if batch.recipe else None,
        "batch_size": float(batch.batch_size) if batch.batch_size else None,
        "age_days": (datetime.now().date() - batch.brew_date).days if batch.brew_date else 0,
        "brewer": batch.brewer,
        "last_updated": datetime.now().isoformat()
    }
    
    mqtt_service.publish(
        f"batch/{batch.id}/attributes",
        attributes
    )

def publish_batch_discovery(batch):
    """Publish Home Assistant MQTT discovery for batch"""
    config = {
        "name": f"HoppyBrew Batch {batch.batch_number}",
        "unique_id": f"hoppybrew_batch_{batch.id}",
        "state_topic": f"hoppybrew/batch/{batch.id}/state",
        "json_attributes_topic": f"hoppybrew/batch/{batch.id}/attributes",
        "device": {
            "identifiers": [f"hoppybrew_batch_{batch.id}"],
            "name": f"Batch: {batch.batch_name}",
            "model": "HoppyBrew Batch",
            "manufacturer": "HoppyBrew",
            "sw_version": "1.0.0"
        },
        "icon": "mdi:beer",
        "availability_topic": "hoppybrew/status"
    }
    
    mqtt_service.publish_discovery("sensor", f"batch_{batch.id}", config)

def publish_fermentation_reading(batch_id, reading):
    """Publish fermentation reading to MQTT"""
    mqtt_service.publish(
        f"batch/{batch_id}/fermentation/gravity",
        reading.gravity
    )
    
    mqtt_service.publish(
        f"batch/{batch_id}/fermentation/temperature",
        reading.temperature
    )
    
    # Calculate and publish attenuation if we have OG
    if reading.batch.actual_og and reading.gravity:
        attenuation = ((reading.batch.actual_og - reading.gravity) / 
                      (reading.batch.actual_og - 1.000)) * 100
        mqtt_service.publish(
            f"batch/{batch_id}/fermentation/attenuation",
            round(attenuation, 1)
        )

def publish_brewery_summary(db: Session):
    """Publish overall brewery status"""
    active_batches = db.query(Batch).filter(
        Batch.status.in_(['brewing', 'fermenting', 'conditioning'])
    ).count()
    
    brewing_count = db.query(Batch).filter(Batch.status == 'brewing').count()
    fermenting_count = db.query(Batch).filter(Batch.status == 'fermenting').count()
    conditioning_count = db.query(Batch).filter(Batch.status == 'conditioning').count()
    
    mqtt_service.publish("brewery/active_batches", active_batches)
    mqtt_service.publish("brewery/brewing_count", brewing_count)
    mqtt_service.publish("brewery/fermenting_count", fermenting_count)
    mqtt_service.publish("brewery/conditioning_count", conditioning_count)
```

**2. Update Batch Endpoints to Publish**
```python
# services/backend/api/endpoints/batches.py (additions)
from services.mqtt_publishers import (
    publish_batch_state, 
    publish_batch_discovery,
    publish_brewery_summary
)

@router.post("/batches", response_model=BatchSchema)
async def create_batch(batch: BatchCreateSchema, db: Session = Depends(get_db)):
    # ... existing creation logic ...
    
    # Publish to MQTT
    publish_batch_discovery(new_batch)
    publish_batch_state(new_batch)
    publish_brewery_summary(db)
    
    return new_batch

@router.put("/batches/{batch_id}/status")
async def update_batch_status(
    batch_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # Update status
    batch.status = status
    db.commit()
    
    # Publish to MQTT
    publish_batch_state(batch)
    publish_brewery_summary(db)
    
    return {"status": "updated"}
```

**3. Update Fermentation Endpoints**
```python
# services/backend/api/endpoints/fermentation.py (new file)
from services.mqtt_publishers import publish_fermentation_reading

@router.post("/batches/{batch_id}/fermentation/readings")
async def create_fermentation_reading(
    batch_id: int,
    reading: FermentationReadingCreate,
    db: Session = Depends(get_db)
):
    # ... create reading logic ...
    
    # Publish to MQTT
    publish_fermentation_reading(batch_id, new_reading)
    
    return new_reading
```

#### Tasks - Phase 2
- [ ] Create mqtt_publishers.py with publishing functions
- [ ] Update batch creation to publish MQTT
- [ ] Update batch status changes to publish MQTT
- [ ] Update fermentation readings to publish MQTT
- [ ] Add brewery summary publishing
- [ ] Test MQTT messages with mosquitto_sub
- [ ] Verify HA auto-discovery works

---

### Phase 3: Device Integration - iSpindel (Week 2)

#### Backend Changes

**1. Create Device Models**
```python
# services/backend/Database/Models/devices.py (enhance existing)
class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)  # ispindel, tilt, inkbird, etc.
    device_id = Column(String, unique=True, nullable=False)  # unique identifier
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=True)
    
    # Configuration
    config = Column(JSON)  # device-specific config
    
    # Status
    status = Column(String, default="offline")  # online, offline, error
    last_seen = Column(DateTime)
    battery_level = Column(Float)
    signal_strength = Column(Integer)
    
    # Relationships
    batch = relationship("Batch", back_populates="devices")
```

**2. Create iSpindel Data Handler**
```python
# services/backend/api/endpoints/devices.py (additions)

@router.post("/devices/ispindel/data")
async def receive_ispindel_data(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Receive data from iSpindel device
    
    Expected payload:
    {
        "name": "iSpindel001",
        "ID": 123456,
        "token": "optional_auth_token",
        "angle": 25.3,
        "temperature": 20.5,
        "battery": 4.1,
        "gravity": 1.048,
        "interval": 900,
        "RSSI": -65
    }
    """
    
    # Find or create device
    device = db.query(Device).filter(
        Device.device_id == data.get("name")
    ).first()
    
    if not device:
        device = Device(
            name=data.get("name"),
            device_type="ispindel",
            device_id=data.get("name"),
            status="online"
        )
        db.add(device)
    
    # Update device status
    device.last_seen = datetime.now()
    device.battery_level = data.get("battery")
    device.signal_strength = data.get("RSSI")
    device.status = "online"
    
    db.commit()
    
    # If device is assigned to a batch, create fermentation reading
    if device.batch_id:
        reading = FermentationReading(
            batch_id=device.batch_id,
            reading_date=datetime.now(),
            gravity=data.get("gravity"),
            temperature=data.get("temperature"),
            notes=f"Auto-logged from {device.name}"
        )
        db.add(reading)
        db.commit()
        
        # Publish to MQTT
        publish_fermentation_reading(device.batch_id, reading)
        publish_device_data(device, data)
    
    return {"status": "ok"}

def publish_device_data(device, data):
    """Publish device data to MQTT"""
    mqtt_service.publish(
        f"devices/{device.device_id}/status",
        device.status
    )
    
    mqtt_service.publish(
        f"devices/{device.device_id}/battery",
        data.get("battery")
    )
    
    mqtt_service.publish(
        f"devices/{device.device_id}/gravity",
        data.get("gravity")
    )
    
    mqtt_service.publish(
        f"devices/{device.device_id}/temperature",
        data.get("temperature")
    )
    
    mqtt_service.publish(
        f"devices/{device.device_id}/signal",
        data.get("RSSI")
    )
```

**3. Device Management Endpoints**
```python
@router.get("/devices")
async def list_devices(db: Session = Depends(get_db)):
    """List all registered devices"""
    devices = db.query(Device).all()
    return devices

@router.post("/devices")
async def register_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """Register a new device"""
    new_device = Device(**device.dict())
    db.add(new_device)
    db.commit()
    
    # Publish discovery
    publish_device_discovery(new_device)
    
    return new_device

@router.put("/devices/{device_id}/assign")
async def assign_device_to_batch(
    device_id: int,
    batch_id: int,
    db: Session = Depends(get_db)
):
    """Assign device to a batch"""
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device.batch_id = batch_id
    db.commit()
    
    return {"status": "assigned"}
```

#### Frontend Changes

**1. Device Management Page**
```vue
<!-- services/nuxt3-shadcn/pages/devices/index.vue -->
<template>
  <div class="container mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Devices</h1>
      <Button @click="showAddDevice = true">
        <Plus class="mr-2" /> Add Device
      </Button>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <Card v-for="device in devices" :key="device.id">
        <CardHeader>
          <div class="flex justify-between">
            <CardTitle>{{ device.name }}</CardTitle>
            <Badge :variant="device.status === 'online' ? 'success' : 'secondary'">
              {{ device.status }}
            </Badge>
          </div>
          <CardDescription>{{ device.device_type }}</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-sm text-muted-foreground">Battery:</span>
              <span>{{ device.battery_level }}V</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-muted-foreground">Signal:</span>
              <span>{{ device.signal_strength }} dBm</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-muted-foreground">Last Seen:</span>
              <span>{{ formatDate(device.last_seen) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-muted-foreground">Assigned to:</span>
              <span>{{ device.batch ? device.batch.batch_name : 'None' }}</span>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button variant="outline" @click="assignDevice(device)">
            Assign to Batch
          </Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDevices } from '~/composables/useDevices'

const { devices, fetchDevices, assignDeviceToBatch } = useDevices()
const showAddDevice = ref(false)

onMounted(async () => {
  await fetchDevices()
})

const assignDevice = async (device) => {
  // Show batch selection dialog
  // ...
}

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}
</script>
```

**2. Device Composable**
```typescript
// services/nuxt3-shadcn/composables/useDevices.ts
export const useDevices = () => {
  const devices = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  const fetchDevices = async () => {
    loading.value = true
    try {
      const response = await $fetch('/api/devices')
      devices.value = response
    } catch (e) {
      error.value = e
    } finally {
      loading.value = false
    }
  }
  
  const registerDevice = async (deviceData) => {
    const response = await $fetch('/api/devices', {
      method: 'POST',
      body: deviceData
    })
    devices.value.push(response)
    return response
  }
  
  const assignDeviceToBatch = async (deviceId, batchId) => {
    await $fetch(`/api/devices/${deviceId}/assign`, {
      method: 'PUT',
      body: { batch_id: batchId }
    })
    await fetchDevices() // Refresh
  }
  
  return {
    devices,
    loading,
    error,
    fetchDevices,
    registerDevice,
    assignDeviceToBatch
  }
}
```

#### Tasks - Phase 3
- [ ] Enhance Device model with status fields
- [ ] Create iSpindel data webhook endpoint
- [ ] Add device management CRUD endpoints
- [ ] Create device assignment endpoint
- [ ] Add MQTT publishing for device data
- [ ] Create Device Management page (frontend)
- [ ] Create useDevices composable
- [ ] Add device assignment dialog
- [ ] Test iSpindel data flow end-to-end
- [ ] Document iSpindel configuration

---

### Phase 4: WebSocket Real-time Updates (Week 2)

#### Backend Changes

**1. Add WebSocket Support**
```python
# requirements.txt additions
python-socketio==5.10.0
python-engineio==4.8.0

# services/backend/main.py (additions)
import socketio

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*'
)

# Wrap FastAPI app with Socket.IO
app_asgi = socketio.ASGIApp(sio, app)

@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    logger.info(f"Client connected: {sid}")
    
@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {sid}")
    
@sio.event
async def subscribe_batch(sid, data):
    """Subscribe to batch updates"""
    batch_id = data.get('batch_id')
    await sio.enter_room(sid, f"batch_{batch_id}")
    logger.info(f"Client {sid} subscribed to batch {batch_id}")
    
async def emit_batch_update(batch_id, data):
    """Emit batch update to subscribed clients"""
    await sio.emit('batch_update', data, room=f"batch_{batch_id}")
```

**2. Emit on Data Changes**
```python
# services/backend/services/mqtt_publishers.py (additions)
from main import sio

async def publish_batch_state(batch):
    """Publish batch state to MQTT and WebSocket"""
    # ... existing MQTT publish code ...
    
    # Also emit via WebSocket
    await emit_batch_update(batch.id, {
        'batch_id': batch.id,
        'status': batch.status,
        'updated_at': datetime.now().isoformat()
    })
```

#### Frontend Changes

**1. WebSocket Client**
```typescript
// services/nuxt3-shadcn/composables/useWebSocket.ts
import { io } from 'socket.io-client'

export const useWebSocket = () => {
  const socket = ref(null)
  const connected = ref(false)
  
  const connect = () => {
    socket.value = io('http://localhost:8000', {
      transports: ['websocket']
    })
    
    socket.value.on('connect', () => {
      connected.value = true
      console.log('WebSocket connected')
    })
    
    socket.value.on('disconnect', () => {
      connected.value = false
      console.log('WebSocket disconnected')
    })
  }
  
  const subscribeToBatch = (batchId) => {
    if (socket.value && connected.value) {
      socket.value.emit('subscribe_batch', { batch_id: batchId })
    }
  }
  
  const onBatchUpdate = (callback) => {
    if (socket.value) {
      socket.value.on('batch_update', callback)
    }
  }
  
  const disconnect = () => {
    if (socket.value) {
      socket.value.disconnect()
    }
  }
  
  return {
    connected,
    connect,
    subscribeToBatch,
    onBatchUpdate,
    disconnect
  }
}
```

**2. Use in Components**
```vue
<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useWebSocket } from '~/composables/useWebSocket'

const route = useRoute()
const batchId = route.params.id

const { connect, subscribeToBatch, onBatchUpdate, disconnect } = useWebSocket()

onMounted(() => {
  connect()
  subscribeToBatch(batchId)
  
  onBatchUpdate((data) => {
    console.log('Batch updated:', data)
    // Update local state
  })
})

onUnmounted(() => {
  disconnect()
})
</script>
```

#### Tasks - Phase 4
- [ ] Add python-socketio to requirements
- [ ] Implement Socket.IO server in main.py
- [ ] Add WebSocket event handlers
- [ ] Emit batch updates via WebSocket
- [ ] Emit fermentation reading updates via WebSocket
- [ ] Create useWebSocket composable
- [ ] Add WebSocket to batch detail page
- [ ] Add WebSocket to fermentation charts
- [ ] Test real-time updates
- [ ] Add reconnection logic

---

## 📊 Testing Plan

### Unit Tests
- [ ] MQTT service connection/disconnection
- [ ] MQTT publish functionality
- [ ] Discovery payload generation
- [ ] Device data parsing
- [ ] WebSocket event handling

### Integration Tests
- [ ] MQTT broker connectivity
- [ ] HA discovery protocol
- [ ] iSpindel data flow
- [ ] WebSocket real-time updates
- [ ] End-to-end device integration

### Manual Testing
- [ ] Set up Mosquitto MQTT broker
- [ ] Test MQTT connection from HoppyBrew
- [ ] Configure HA to receive sensors
- [ ] Verify auto-discovery works
- [ ] Send test data from iSpindel simulator
- [ ] Verify data appears in HA
- [ ] Test WebSocket updates in browser
- [ ] Test state transitions publish correctly

---

## 📖 Documentation Updates

### New Documentation Needed
- [ ] MQTT broker setup guide (Mosquitto, HiveMQ, etc.)
- [ ] Home Assistant MQTT configuration
- [ ] iSpindel device setup and configuration
- [ ] Tilt device setup (if implemented)
- [ ] WebSocket API documentation
- [ ] Device pairing procedures
- [ ] Troubleshooting guide for MQTT issues
- [ ] Example HA automations using MQTT
- [ ] Example HA dashboard configurations

### Updates to Existing Docs
- [ ] Update HOMEASSISTANT_INTEGRATION.md with MQTT section
- [ ] Add MQTT configuration to README.md
- [ ] Update docker-compose.yml with MQTT settings
- [ ] Add .env.example MQTT variables
- [ ] Update API documentation with device endpoints

---

## 🎯 Success Metrics

### Technical Metrics
- [ ] MQTT messages published within 1 second of state change
- [ ] WebSocket latency < 100ms
- [ ] Device data processing < 500ms
- [ ] 99.9% MQTT connection uptime
- [ ] Zero message loss during normal operation

### User Experience Metrics
- [ ] HA auto-discovery success rate > 95%
- [ ] Device pairing time < 2 minutes
- [ ] Real-time dashboard updates without refresh
- [ ] Fermentation data visible in HA within 1 minute of device update

---

## 🚀 Deployment Checklist

### Infrastructure Requirements
- [ ] MQTT broker running (Mosquitto recommended)
- [ ] MQTT broker accessible from HoppyBrew container
- [ ] WebSocket port (8000) accessible
- [ ] Home Assistant configured for MQTT
- [ ] Devices configured with HoppyBrew endpoint

### Configuration
- [ ] MQTT broker hostname/IP configured
- [ ] MQTT credentials configured (if authentication enabled)
- [ ] MQTT topic prefix configured
- [ ] WebSocket CORS configured for frontend
- [ ] Device webhooks configured

### Post-Deployment
- [ ] Verify MQTT connection in logs
- [ ] Check HA discovers sensors automatically
- [ ] Test device data ingestion
- [ ] Verify WebSocket connections
- [ ] Monitor MQTT message volume and latency

---

**End of Home Assistant Enhancement Plan**
