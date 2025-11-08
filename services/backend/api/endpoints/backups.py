"""
Backup API Endpoints for HoppyBrew
Provides REST API for database backup and restore operations
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from modules.backup_service import BackupService
from logger_config import get_logger

logger = get_logger("BackupAPI")

router = APIRouter(prefix="/backups")


# Pydantic models for request/response
class BackupCreateRequest(BaseModel):
    """Request model for creating a backup"""
    description: Optional[str] = Field(
        default="",
        description="Optional description for the backup"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "description": "Pre-upgrade backup"
                }
            ]
        }
    }


class BackupInfo(BaseModel):
    """Response model for backup information"""
    filename: str
    timestamp: str
    created_at: str
    description: str
    size_bytes: int
    database_name: str
    database_host: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "filename": "hoppybrew_backup_20241108_120000.sql.gz",
                    "timestamp": "20241108_120000",
                    "created_at": "2024-11-08T12:00:00",
                    "description": "Scheduled backup",
                    "size_bytes": 1024576,
                    "database_name": "hoppybrew_db",
                    "database_host": "localhost"
                }
            ]
        }
    }


class BackupRestoreRequest(BaseModel):
    """Request model for restoring a backup"""
    filename: str = Field(
        description="Name of the backup file to restore"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "filename": "hoppybrew_backup_20241108_120000.sql.gz"
                }
            ]
        }
    }


class BackupOperationResponse(BaseModel):
    """Response model for backup operations"""
    status: str
    message: str
    filename: Optional[str] = None
    timestamp: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "message": "Backup created successfully",
                    "filename": "hoppybrew_backup_20241108_120000.sql.gz",
                    "timestamp": "2024-11-08T12:00:00"
                }
            ]
        }
    }


class CleanupResponse(BaseModel):
    """Response model for cleanup operation"""
    deleted_count: int
    deleted_files: List[str]
    total_size_freed: int
    retention_days: int
    cleanup_date: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "deleted_count": 3,
                    "deleted_files": [
                        "hoppybrew_backup_20241001_120000.sql.gz",
                        "hoppybrew_backup_20241002_120000.sql.gz"
                    ],
                    "total_size_freed": 3145728,
                    "retention_days": 30,
                    "cleanup_date": "2024-11-08T12:00:00"
                }
            ]
        }
    }


# Initialize backup service
backup_service = BackupService()


@router.post(
    "",
    response_model=BackupOperationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new database backup",
    description="Creates a compressed backup of the HoppyBrew database"
)
async def create_backup(request: BackupCreateRequest):
    """
    Create a new database backup.
    
    This endpoint creates a compressed backup of the entire database,
    including all recipes, batches, inventory, and settings.
    
    - **description**: Optional description to help identify the backup later
    """
    try:
        logger.info(f"Creating backup with description: {request.description}")
        metadata = backup_service.create_backup(description=request.description)
        
        return BackupOperationResponse(
            status="success",
            message="Backup created successfully",
            filename=metadata["filename"],
            timestamp=metadata["created_at"]
        )
    except Exception as e:
        logger.error(f"Failed to create backup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create backup: {str(e)}"
        )


@router.get(
    "",
    response_model=List[BackupInfo],
    summary="List all available backups",
    description="Returns a list of all available database backups, sorted by date (newest first)"
)
async def list_backups():
    """
    Get a list of all available backups.
    
    Returns metadata for each backup including:
    - Filename
    - Creation timestamp
    - Description
    - File size
    - Database information
    """
    try:
        backups = backup_service.list_backups()
        
        # Remove filepath from response (internal only)
        for backup in backups:
            backup.pop("filepath", None)
        
        return backups
    except Exception as e:
        logger.error(f"Failed to list backups: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list backups: {str(e)}"
        )


@router.get(
    "/{filename}",
    response_model=BackupInfo,
    summary="Get backup information",
    description="Returns detailed information about a specific backup"
)
async def get_backup_info(filename: str):
    """
    Get detailed information about a specific backup.
    
    - **filename**: Name of the backup file
    """
    try:
        info = backup_service.get_backup_info(filename)
        return info
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Backup not found: {filename}"
        )
    except Exception as e:
        logger.error(f"Failed to get backup info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get backup info: {str(e)}"
        )


@router.post(
    "/restore",
    response_model=BackupOperationResponse,
    summary="Restore database from backup",
    description="Restores the database from a backup file. WARNING: This will overwrite current data!"
)
async def restore_backup(request: BackupRestoreRequest):
    """
    Restore the database from a backup.
    
    **WARNING**: This operation will restore the database to the state captured
    in the backup file. Any changes made after the backup was created will be lost.
    
    - **filename**: Name of the backup file to restore from
    """
    try:
        logger.info(f"Restoring backup: {request.filename}")
        result = backup_service.restore_backup(request.filename)
        
        return BackupOperationResponse(
            status=result["status"],
            message=result["message"],
            filename=result["filename"],
            timestamp=result["restored_at"]
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Backup not found: {request.filename}"
        )
    except Exception as e:
        logger.error(f"Failed to restore backup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to restore backup: {str(e)}"
        )


@router.delete(
    "/{filename}",
    response_model=BackupOperationResponse,
    summary="Delete a backup",
    description="Permanently deletes a backup file and its metadata"
)
async def delete_backup(filename: str):
    """
    Delete a specific backup file.
    
    This permanently removes the backup file and its associated metadata.
    This operation cannot be undone.
    
    - **filename**: Name of the backup file to delete
    """
    try:
        logger.info(f"Deleting backup: {filename}")
        result = backup_service.delete_backup(filename)
        
        return BackupOperationResponse(
            status=result["status"],
            message=result["message"],
            filename=filename,
            timestamp=result["deleted_at"]
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Backup not found: {filename}"
        )
    except Exception as e:
        logger.error(f"Failed to delete backup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete backup: {str(e)}"
        )


@router.post(
    "/cleanup",
    response_model=CleanupResponse,
    summary="Clean up old backups",
    description="Removes backups older than the retention period"
)
async def cleanup_old_backups():
    """
    Clean up old backups based on retention policy.
    
    This removes all backups that are older than the configured retention period
    (default: 30 days). The retention period can be configured via the
    BACKUP_RETENTION_DAYS environment variable.
    """
    try:
        logger.info("Running backup cleanup")
        result = backup_service.cleanup_old_backups()
        return result
    except Exception as e:
        logger.error(f"Failed to cleanup backups: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cleanup backups: {str(e)}"
        )
