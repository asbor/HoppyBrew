# services/backend/modules/device_scheduler.py

"""
Background task scheduler for automatic device data import.

This module handles periodic polling of temperature controller devices
that support pull-based data retrieval (as opposed to webhook-based push).
For webhook-based devices (Tilt, iSpindel), the scheduler is not needed
as they push data directly to the webhook endpoints.

The scheduler can be extended to support additional device types that
require polling, such as Bluetooth devices or cloud API integrations.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
import Database.Models as models
import logging

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None


def get_scheduler():
    """Get or create the global scheduler instance"""
    global scheduler
    if scheduler is None:
        scheduler = AsyncIOScheduler()
    return scheduler


async def check_devices_for_import():
    """
    Check all active devices and determine if they need data import.
    
    This function is called periodically (every 5 minutes) to check
    if any devices need data polling. Devices with auto_import_enabled
    and a configured import_interval_seconds will be checked.
    
    For webhook-based devices (Tilt, iSpindel), this is mainly for
    monitoring purposes and alerting if data hasn't been received.
    """
    db: Session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        
        # Get all active devices with auto-import enabled
        devices = db.query(models.Device).filter(
            models.Device.is_active == True,
            models.Device.auto_import_enabled == True,
            models.Device.manual_override == False,
            models.Device.batch_id.isnot(None)
        ).all()
        
        logger.info(f"Checking {len(devices)} active devices for import")
        
        for device in devices:
            # Check if it's time to import based on interval
            if device.last_import_at is None:
                time_since_import = timedelta.max
            else:
                time_since_import = now - device.last_import_at
            
            import_interval = timedelta(seconds=device.import_interval_seconds)
            
            if time_since_import >= import_interval:
                # For webhook-based devices, log a warning if data hasn't been received
                if device.device_type.lower() in ['tilt', 'ispindel']:
                    logger.warning(
                        f"Device {device.id} ({device.name}) hasn't received data for "
                        f"{time_since_import.total_seconds():.0f} seconds. Expected interval: "
                        f"{device.import_interval_seconds} seconds"
                    )
                    
                    # Check if there's an alert configuration for missing data
                    if device.alert_config and device.alert_config.get('missing_data_alert'):
                        logger.error(
                            f"ALERT: Device {device.id} ({device.name}) - No data received "
                            f"for {time_since_import.total_seconds():.0f} seconds!"
                        )
                else:
                    # For pull-based devices (future implementation), trigger import here
                    logger.info(
                        f"Device {device.id} ({device.name}) type {device.device_type} "
                        f"would trigger pull-based import here"
                    )
        
    except Exception as e:
        logger.error(f"Error in device import check: {e}", exc_info=True)
    finally:
        db.close()


def start_scheduler():
    """
    Start the background scheduler for device data import.
    
    This function should be called when the application starts.
    It sets up a periodic task that runs every 5 minutes to check
    if devices need data import.
    """
    global scheduler
    scheduler = get_scheduler()
    
    # Add the device check job to run every 5 minutes
    scheduler.add_job(
        check_devices_for_import,
        trigger=IntervalTrigger(minutes=5),
        id='device_import_check',
        name='Check devices for data import',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Device scheduler started - checking devices every 5 minutes")


def stop_scheduler():
    """
    Stop the background scheduler.
    
    This function should be called when the application shuts down
    to ensure graceful cleanup of background tasks.
    """
    global scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown()
        logger.info("Device scheduler stopped")


def get_scheduler_status():
    """
    Get the current status of the scheduler.
    
    Returns information about scheduled jobs and their next run times.
    """
    global scheduler
    if not scheduler:
        return {"status": "not_initialized"}
    
    if not scheduler.running:
        return {"status": "stopped"}
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
        })
    
    return {
        "status": "running",
        "jobs": jobs
    }
