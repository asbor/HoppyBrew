"""
Backup Service Module for HoppyBrew
Handles database backup and restore operations with retention management.
"""

import os
import subprocess
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import json
from logger_config import get_logger
from config import settings

logger = get_logger("BackupService")


class BackupService:
    """Service for managing database backups and restore operations"""

    def __init__(self, backup_dir: Optional[str] = None):
        """
        Initialize the backup service
        
        Args:
            backup_dir: Directory to store backups. If None, uses environment config or default.
        """
        if backup_dir:
            self.backup_dir = Path(backup_dir)
        else:
            # Use /app/data/backups in container, ./data/backups locally
            default_dir = os.getenv("BACKUP_DIR", "/app/data/backups")
            self.backup_dir = Path(default_dir)
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Backup directory: {self.backup_dir}")

    def create_backup(self, description: str = "") -> Dict[str, str]:
        """
        Create a database backup
        
        Args:
            description: Optional description for the backup
            
        Returns:
            Dictionary with backup metadata
            
        Raises:
            RuntimeError: If backup creation fails
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hoppybrew_backup_{timestamp}.sql"
        filepath = self.backup_dir / filename
        compressed_filepath = self.backup_dir / f"{filename}.gz"
        
        logger.info(f"Creating backup: {filename}")
        
        try:
            # Run pg_dump to create backup
            env = os.environ.copy()
            env["PGPASSWORD"] = settings.DATABASE_PASSWORD
            
            # Build pg_dump command
            cmd = [
                "pg_dump",
                "-h", settings.DATABASE_HOST,
                "-p", str(settings.DATABASE_PORT),
                "-U", settings.DATABASE_USER,
                "-d", settings.DATABASE_NAME,
                "-F", "p",  # Plain text format
                "-f", str(filepath),
                "--no-owner",  # Don't include ownership commands
                "--no-acl",    # Don't include ACL commands
            ]
            
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                error_msg = f"pg_dump failed: {result.stderr}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            # Compress the backup file
            logger.info(f"Compressing backup: {compressed_filepath}")
            with open(filepath, 'rb') as f_in:
                with gzip.open(compressed_filepath, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove uncompressed file
            filepath.unlink()
            
            # Get file size
            file_size = compressed_filepath.stat().st_size
            
            # Create metadata file
            metadata = {
                "filename": compressed_filepath.name,
                "timestamp": timestamp,
                "created_at": datetime.now().isoformat(),
                "description": description,
                "size_bytes": file_size,
                "database_name": settings.DATABASE_NAME,
                "database_host": settings.DATABASE_HOST,
            }
            
            metadata_filepath = self.backup_dir / f"{filename}.json"
            with open(metadata_filepath, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Backup created successfully: {compressed_filepath.name} ({file_size} bytes)")
            
            return metadata
            
        except subprocess.TimeoutExpired:
            error_msg = "Backup creation timed out after 5 minutes"
            logger.error(error_msg)
            if filepath.exists():
                filepath.unlink()
            raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"Failed to create backup: {str(e)}"
            logger.error(error_msg)
            # Cleanup on failure
            if filepath.exists():
                filepath.unlink()
            if compressed_filepath.exists():
                compressed_filepath.unlink()
            raise RuntimeError(error_msg)

    def list_backups(self) -> List[Dict[str, str]]:
        """
        List all available backups
        
        Returns:
            List of backup metadata dictionaries
        """
        backups = []
        
        # Find all .json metadata files
        for metadata_file in self.backup_dir.glob("*.json"):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    
                # Verify the backup file exists
                backup_file = self.backup_dir / metadata["filename"]
                if backup_file.exists():
                    # Add file path for restore operations
                    metadata["filepath"] = str(backup_file)
                    backups.append(metadata)
                else:
                    logger.warning(f"Backup file missing: {backup_file}")
            except Exception as e:
                logger.error(f"Error reading metadata {metadata_file}: {e}")
        
        # Sort by timestamp, newest first
        backups.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return backups

    def restore_backup(self, filename: str) -> Dict[str, str]:
        """
        Restore database from a backup file
        
        Args:
            filename: Name of the backup file to restore
            
        Returns:
            Dictionary with restore operation result
            
        Raises:
            FileNotFoundError: If backup file doesn't exist
            RuntimeError: If restore fails
        """
        compressed_filepath = self.backup_dir / filename
        
        if not compressed_filepath.exists():
            raise FileNotFoundError(f"Backup file not found: {filename}")
        
        # Decompress the backup file
        sql_filepath = self.backup_dir / filename.replace('.gz', '')
        
        logger.info(f"Restoring backup: {filename}")
        
        try:
            # Decompress the backup
            logger.info(f"Decompressing backup: {compressed_filepath}")
            with gzip.open(compressed_filepath, 'rb') as f_in:
                with open(sql_filepath, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Run psql to restore backup
            env = os.environ.copy()
            env["PGPASSWORD"] = settings.DATABASE_PASSWORD
            
            cmd = [
                "psql",
                "-h", settings.DATABASE_HOST,
                "-p", str(settings.DATABASE_PORT),
                "-U", settings.DATABASE_USER,
                "-d", settings.DATABASE_NAME,
                "-f", str(sql_filepath),
            ]
            
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            # Cleanup decompressed file
            sql_filepath.unlink()
            
            if result.returncode != 0:
                error_msg = f"Database restore failed: {result.stderr}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            logger.info(f"Backup restored successfully: {filename}")
            
            return {
                "status": "success",
                "filename": filename,
                "restored_at": datetime.now().isoformat(),
                "message": "Database restored successfully"
            }
            
        except subprocess.TimeoutExpired:
            error_msg = "Restore operation timed out after 10 minutes"
            logger.error(error_msg)
            if sql_filepath.exists():
                sql_filepath.unlink()
            raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"Failed to restore backup: {str(e)}"
            logger.error(error_msg)
            if sql_filepath.exists():
                sql_filepath.unlink()
            raise RuntimeError(error_msg)

    def delete_backup(self, filename: str) -> Dict[str, str]:
        """
        Delete a specific backup file and its metadata
        
        Args:
            filename: Name of the backup file to delete
            
        Returns:
            Dictionary with deletion result
            
        Raises:
            FileNotFoundError: If backup file doesn't exist
        """
        compressed_filepath = self.backup_dir / filename
        
        if not compressed_filepath.exists():
            raise FileNotFoundError(f"Backup file not found: {filename}")
        
        # Also remove metadata file if it exists
        metadata_filename = filename.replace('.gz', '.json')
        metadata_filepath = self.backup_dir / metadata_filename
        
        try:
            compressed_filepath.unlink()
            logger.info(f"Deleted backup: {filename}")
            
            if metadata_filepath.exists():
                metadata_filepath.unlink()
                logger.info(f"Deleted metadata: {metadata_filename}")
            
            return {
                "status": "success",
                "filename": filename,
                "deleted_at": datetime.now().isoformat(),
                "message": "Backup deleted successfully"
            }
        except Exception as e:
            error_msg = f"Failed to delete backup: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def cleanup_old_backups(self, retention_days: Optional[int] = None) -> Dict[str, any]:
        """
        Remove backups older than retention period
        
        Args:
            retention_days: Number of days to keep backups. If None, uses config value.
            
        Returns:
            Dictionary with cleanup statistics
        """
        if retention_days is None:
            retention_days = settings.BACKUP_RETENTION_DAYS
        
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        logger.info(f"Cleaning up backups older than {retention_days} days (before {cutoff_date.isoformat()})")
        
        deleted_count = 0
        deleted_files = []
        total_size_freed = 0
        
        backups = self.list_backups()
        
        for backup in backups:
            try:
                created_at = datetime.fromisoformat(backup["created_at"])
                
                if created_at < cutoff_date:
                    filename = backup["filename"]
                    filepath = Path(backup["filepath"])
                    
                    # Get file size before deletion
                    file_size = filepath.stat().st_size
                    
                    # Delete the backup
                    self.delete_backup(filename)
                    
                    deleted_count += 1
                    deleted_files.append(filename)
                    total_size_freed += file_size
                    
            except Exception as e:
                logger.error(f"Error during cleanup of {backup.get('filename')}: {e}")
        
        logger.info(f"Cleanup complete: {deleted_count} backups deleted, {total_size_freed} bytes freed")
        
        return {
            "deleted_count": deleted_count,
            "deleted_files": deleted_files,
            "total_size_freed": total_size_freed,
            "retention_days": retention_days,
            "cleanup_date": datetime.now().isoformat()
        }

    def get_backup_info(self, filename: str) -> Dict[str, str]:
        """
        Get detailed information about a specific backup
        
        Args:
            filename: Name of the backup file
            
        Returns:
            Dictionary with backup metadata
            
        Raises:
            FileNotFoundError: If backup or metadata file doesn't exist
        """
        compressed_filepath = self.backup_dir / filename
        
        if not compressed_filepath.exists():
            raise FileNotFoundError(f"Backup file not found: {filename}")
        
        metadata_filename = filename.replace('.gz', '.json')
        metadata_filepath = self.backup_dir / metadata_filename
        
        if metadata_filepath.exists():
            with open(metadata_filepath, 'r') as f:
                return json.load(f)
        else:
            # Return basic info if metadata is missing
            return {
                "filename": filename,
                "size_bytes": compressed_filepath.stat().st_size,
                "message": "Metadata file not found"
            }
