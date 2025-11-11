# services/backend/modules/device_poller.py

"""
Background task for polling device data.

This module provides automatic polling for devices that don't push data directly.
Currently supports:
- Tilt Cloud API polling
- Future: other cloud-based device APIs
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional
import httpx
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models

logger = logging.getLogger(__name__)


class DevicePoller:
    """Background poller for device data"""
    
    def __init__(self, poll_interval: int = 900):  # 15 minutes default
        """
        Initialize device poller.
        
        Args:
            poll_interval: Seconds between polls (default 900 = 15 minutes)
        """
        self.poll_interval = poll_interval
        self.running = False
        self.task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the polling task"""
        if self.running:
            logger.warning("Device poller already running")
            return
        
        self.running = True
        self.task = asyncio.create_task(self._poll_loop())
        logger.info(f"Device poller started with {self.poll_interval}s interval")
    
    async def stop(self):
        """Stop the polling task"""
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("Device poller stopped")
    
    async def _poll_loop(self):
        """Main polling loop"""
        while self.running:
            try:
                await self._poll_devices()
            except Exception as e:
                logger.error(f"Error in device polling loop: {e}")
            
            # Wait for next poll interval
            await asyncio.sleep(self.poll_interval)
    
    async def _poll_devices(self):
        """Poll all active devices"""
        # Get database session
        db = next(get_db())
        
        try:
            # Get all active devices with batch associations
            devices = db.query(models.Device).filter(
                models.Device.is_active == True,
                models.Device.batch_id.isnot(None)
            ).all()
            
            logger.info(f"Polling {len(devices)} active devices")
            
            for device in devices:
                try:
                    if device.device_type == "tilt" and device.configuration:
                        await self._poll_tilt_cloud(device, db)
                    # Add other device types here as needed
                except Exception as e:
                    logger.error(f"Error polling device {device.name}: {e}")
            
            db.commit()
        
        except Exception as e:
            logger.error(f"Error in device poll: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def _poll_tilt_cloud(self, device: models.Device, db: Session):
        """
        Poll Tilt Cloud API for data.
        
        Requires device configuration with:
        - cloud_url: URL to Tilt Cloud API
        - hydrometer_id: Tilt hydrometer ID
        """
        config = device.configuration or {}
        cloud_url = config.get("cloud_url")
        hydrometer_id = config.get("hydrometer_id")
        
        if not cloud_url or not hydrometer_id:
            logger.debug(f"Tilt device {device.name} missing cloud configuration")
            return
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {}
                if device.api_token:
                    headers["Authorization"] = f"Bearer {device.api_token}"
                
                response = await client.get(
                    f"{cloud_url}/api/hydrometer/{hydrometer_id}/latest",
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    logger.warning(f"Tilt Cloud API returned {response.status_code} for {device.name}")
                    return
                
                data = response.json()
                
                # Extract data
                temperature_f = data.get("Temp")
                temperature_c = (temperature_f - 32) * 5/9 if temperature_f else None
                gravity = data.get("SG")
                timestamp_str = data.get("Timepoint")
                
                # Parse timestamp
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) if timestamp_str else datetime.now()
                
                # Check if we already have this reading (avoid duplicates)
                existing = db.query(models.FermentationReadings).filter(
                    models.FermentationReadings.batch_id == device.batch_id,
                    models.FermentationReadings.device_id == device.id,
                    models.FermentationReadings.timestamp == timestamp
                ).first()
                
                if existing:
                    logger.debug(f"Reading from {timestamp} already exists for {device.name}")
                    return
                
                # Create new reading
                reading = models.FermentationReadings(
                    batch_id=device.batch_id,
                    device_id=device.id,
                    timestamp=timestamp,
                    gravity=gravity,
                    temperature=temperature_c,
                    source="tilt",
                    notes=f"Tilt {data.get('Color', 'Unknown')} auto-poll"
                )
                
                db.add(reading)
                device.last_reading_at = datetime.now()
                
                logger.info(f"Polled reading from {device.name}: SG={gravity}, Temp={temperature_c}°C")
        
        except httpx.TimeoutException:
            logger.warning(f"Timeout polling Tilt Cloud for {device.name}")
        except Exception as e:
            logger.error(f"Error polling Tilt Cloud for {device.name}: {e}")


# Global poller instance
_poller: Optional[DevicePoller] = None


def get_poller() -> DevicePoller:
    """Get or create the global device poller instance"""
    global _poller
    if _poller is None:
        _poller = DevicePoller()
    return _poller


async def start_device_poller():
    """Start the device polling background task"""
    poller = get_poller()
    await poller.start()


async def stop_device_poller():
    """Stop the device polling background task"""
    poller = get_poller()
    await poller.stop()
