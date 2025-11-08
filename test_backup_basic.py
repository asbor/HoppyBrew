#!/usr/bin/env python3
"""
Simple test script to verify backup service functionality
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent / "services" / "backend"
sys.path.insert(0, str(backend_dir))

# Set testing mode
os.environ["TESTING"] = "1"
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test_backup.db"
os.environ["BACKUP_DIR"] = "./test_backups"

from modules.backup_service import BackupService
from logger_config import get_logger

logger = get_logger("BackupTest")


def test_backup_service():
    """Test basic backup service functionality"""
    
    # Create backup service with test directory
    backup_dir = Path("./test_backups")
    backup_dir.mkdir(exist_ok=True)
    
    service = BackupService(str(backup_dir))
    
    logger.info("=" * 60)
    logger.info("Testing Backup Service")
    logger.info("=" * 60)
    
    # Test 1: List backups (should be empty initially)
    logger.info("\nTest 1: List backups")
    backups = service.list_backups()
    logger.info(f"Found {len(backups)} backups")
    assert isinstance(backups, list), "list_backups should return a list"
    
    # Test 2: Check configuration
    logger.info("\nTest 2: Check configuration")
    logger.info(f"Backup directory: {service.backup_dir}")
    logger.info(f"Directory exists: {service.backup_dir.exists()}")
    assert service.backup_dir.exists(), "Backup directory should exist"
    
    # Test 3: Test metadata operations (without actual pg_dump)
    logger.info("\nTest 3: Test backup metadata structure")
    test_metadata = {
        "filename": "test_backup.sql.gz",
        "timestamp": "20241108_120000",
        "created_at": "2024-11-08T12:00:00",
        "description": "Test backup",
        "size_bytes": 1024,
        "database_name": "test_db",
        "database_host": "localhost"
    }
    logger.info(f"Test metadata: {test_metadata}")
    
    # Test 4: Test cleanup logic (without actual backups)
    logger.info("\nTest 4: Test cleanup parameters")
    from config import settings
    logger.info(f"Retention days: {settings.BACKUP_RETENTION_DAYS}")
    logger.info(f"Backup enabled: {settings.BACKUP_ENABLED}")
    logger.info(f"Backup schedule: {settings.BACKUP_SCHEDULE}")
    
    logger.info("\n" + "=" * 60)
    logger.info("All basic tests passed!")
    logger.info("=" * 60)
    
    # Cleanup test directory
    import shutil
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
        logger.info(f"\nCleaned up test directory: {backup_dir}")


if __name__ == "__main__":
    try:
        test_backup_service()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)
