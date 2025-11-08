"""
Backup Scheduler Module for HoppyBrew
Handles automated backup scheduling based on configuration
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from modules.backup_service import BackupService
from logger_config import get_logger
from config import settings

logger = get_logger("BackupScheduler")


class BackupScheduler:
    """Manages automated backup scheduling"""

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.backup_service = BackupService()
        self._is_running = False

    def start(self):
        """Start the backup scheduler if enabled in configuration"""
        if not settings.BACKUP_ENABLED:
            logger.info("Automated backups are disabled (BACKUP_ENABLED=false)")
            return

        if self._is_running:
            logger.warning("Backup scheduler is already running")
            return

        try:
            # Parse cron schedule from settings
            cron_parts = settings.BACKUP_SCHEDULE.split()
            if len(cron_parts) != 5:
                logger.error(
                    f"Invalid cron schedule format: {settings.BACKUP_SCHEDULE}. "
                    "Expected format: 'minute hour day month day_of_week'"
                )
                return

            minute, hour, day, month, day_of_week = cron_parts

            # Create cron trigger
            trigger = CronTrigger(
                minute=minute,
                hour=hour,
                day=day,
                month=month,
                day_of_week=day_of_week
            )

            # Add the backup job
            self.scheduler.add_job(
                func=self._run_backup,
                trigger=trigger,
                id="automated_backup",
                name="Automated Database Backup",
                replace_existing=True
            )

            # Add cleanup job - run daily at 3 AM
            self.scheduler.add_job(
                func=self._run_cleanup,
                trigger=CronTrigger(hour=3, minute=0),
                id="backup_cleanup",
                name="Backup Cleanup",
                replace_existing=True
            )

            self.scheduler.start()
            self._is_running = True

            logger.info(
                f"Backup scheduler started. Schedule: {settings.BACKUP_SCHEDULE}, "
                f"Retention: {settings.BACKUP_RETENTION_DAYS} days"
            )

        except Exception as e:
            logger.error(f"Failed to start backup scheduler: {str(e)}")

    def stop(self):
        """Stop the backup scheduler"""
        if not self._is_running:
            return

        try:
            self.scheduler.shutdown(wait=False)
            self._is_running = False
            logger.info("Backup scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping backup scheduler: {str(e)}")

    def _run_backup(self):
        """Execute scheduled backup"""
        try:
            logger.info("Running scheduled backup")
            metadata = self.backup_service.create_backup(
                description="Scheduled backup"
            )
            logger.info(
                f"Scheduled backup completed: {metadata['filename']} "
                f"({metadata['size_bytes']} bytes)"
            )
        except Exception as e:
            logger.error(f"Scheduled backup failed: {str(e)}")

    def _run_cleanup(self):
        """Execute scheduled cleanup"""
        try:
            logger.info("Running scheduled backup cleanup")
            result = self.backup_service.cleanup_old_backups()
            logger.info(
                f"Cleanup completed: {result['deleted_count']} backups deleted, "
                f"{result['total_size_freed']} bytes freed"
            )
        except Exception as e:
            logger.error(f"Scheduled cleanup failed: {str(e)}")

    @property
    def is_running(self) -> bool:
        """Check if scheduler is running"""
        return self._is_running


# Global scheduler instance
backup_scheduler = BackupScheduler()
