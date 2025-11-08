"""
Tests for backup API endpoints
"""

import pytest
import os
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from fastapi import status


@pytest.fixture
def backup_dir(tmp_path):
    """Create a temporary backup directory for testing"""
    backup_path = tmp_path / "backups"
    backup_path.mkdir()
    return str(backup_path)


@pytest.fixture
def mock_backup_service(backup_dir):
    """Mock backup service for testing"""
    with patch("api.endpoints.backups.BackupService") as mock:
        service_instance = MagicMock()
        mock.return_value = service_instance
        
        # Setup default return values
        service_instance.create_backup.return_value = {
            "filename": "hoppybrew_backup_20241108_120000.sql.gz",
            "timestamp": "20241108_120000",
            "created_at": "2024-11-08T12:00:00",
            "description": "Test backup",
            "size_bytes": 1024,
            "database_name": "hoppybrew_db",
            "database_host": "localhost"
        }
        
        service_instance.list_backups.return_value = [
            {
                "filename": "hoppybrew_backup_20241108_120000.sql.gz",
                "timestamp": "20241108_120000",
                "created_at": "2024-11-08T12:00:00",
                "description": "Test backup",
                "size_bytes": 1024,
                "database_name": "hoppybrew_db",
                "database_host": "localhost",
                "filepath": f"{backup_dir}/hoppybrew_backup_20241108_120000.sql.gz"
            }
        ]
        
        service_instance.restore_backup.return_value = {
            "status": "success",
            "filename": "hoppybrew_backup_20241108_120000.sql.gz",
            "restored_at": "2024-11-08T12:05:00",
            "message": "Database restored successfully"
        }
        
        service_instance.delete_backup.return_value = {
            "status": "success",
            "filename": "hoppybrew_backup_20241108_120000.sql.gz",
            "deleted_at": "2024-11-08T12:10:00",
            "message": "Backup deleted successfully"
        }
        
        service_instance.cleanup_old_backups.return_value = {
            "deleted_count": 2,
            "deleted_files": [
                "hoppybrew_backup_20241001_120000.sql.gz",
                "hoppybrew_backup_20241002_120000.sql.gz"
            ],
            "total_size_freed": 2048,
            "retention_days": 30,
            "cleanup_date": "2024-11-08T12:00:00"
        }
        
        service_instance.get_backup_info.return_value = {
            "filename": "hoppybrew_backup_20241108_120000.sql.gz",
            "timestamp": "20241108_120000",
            "created_at": "2024-11-08T12:00:00",
            "description": "Test backup",
            "size_bytes": 1024,
            "database_name": "hoppybrew_db",
            "database_host": "localhost"
        }
        
        yield service_instance


def test_create_backup(client, mock_backup_service):
    """Test creating a new backup"""
    response = client.post(
        "/backups",
        json={"description": "Test backup"}
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    
    assert data["status"] == "success"
    assert data["message"] == "Backup created successfully"
    assert "filename" in data
    assert "timestamp" in data
    
    # Verify backup service was called
    mock_backup_service.create_backup.assert_called_once_with(description="Test backup")


def test_create_backup_without_description(client, mock_backup_service):
    """Test creating a backup without description"""
    response = client.post("/backups", json={})
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    
    assert data["status"] == "success"
    mock_backup_service.create_backup.assert_called_once_with(description="")


def test_create_backup_failure(client, mock_backup_service):
    """Test backup creation failure"""
    mock_backup_service.create_backup.side_effect = RuntimeError("Backup failed")
    
    response = client.post("/backups", json={"description": "Test"})
    
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Failed to create backup" in response.json()["detail"]


def test_list_backups(client, mock_backup_service):
    """Test listing all backups"""
    response = client.get("/backups")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["filename"] == "hoppybrew_backup_20241108_120000.sql.gz"
    assert "filepath" not in data[0]  # Should be removed from response


def test_get_backup_info(client, mock_backup_service):
    """Test getting backup information"""
    filename = "hoppybrew_backup_20241108_120000.sql.gz"
    response = client.get(f"/backups/{filename}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["filename"] == filename
    assert data["size_bytes"] == 1024
    
    mock_backup_service.get_backup_info.assert_called_once_with(filename)


def test_get_backup_info_not_found(client, mock_backup_service):
    """Test getting info for non-existent backup"""
    mock_backup_service.get_backup_info.side_effect = FileNotFoundError()
    
    response = client.get("/backups/nonexistent.sql.gz")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_restore_backup(client, mock_backup_service):
    """Test restoring from backup"""
    filename = "hoppybrew_backup_20241108_120000.sql.gz"
    response = client.post(
        "/backups/restore",
        json={"filename": filename}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["status"] == "success"
    assert data["message"] == "Database restored successfully"
    assert data["filename"] == filename
    
    mock_backup_service.restore_backup.assert_called_once_with(filename)


def test_restore_backup_not_found(client, mock_backup_service):
    """Test restoring from non-existent backup"""
    mock_backup_service.restore_backup.side_effect = FileNotFoundError()
    
    response = client.post(
        "/backups/restore",
        json={"filename": "nonexistent.sql.gz"}
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_restore_backup_failure(client, mock_backup_service):
    """Test backup restore failure"""
    mock_backup_service.restore_backup.side_effect = RuntimeError("Restore failed")
    
    response = client.post(
        "/backups/restore",
        json={"filename": "test.sql.gz"}
    )
    
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Failed to restore backup" in response.json()["detail"]


def test_delete_backup(client, mock_backup_service):
    """Test deleting a backup"""
    filename = "hoppybrew_backup_20241108_120000.sql.gz"
    response = client.delete(f"/backups/{filename}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["status"] == "success"
    assert data["message"] == "Backup deleted successfully"
    assert data["filename"] == filename
    
    mock_backup_service.delete_backup.assert_called_once_with(filename)


def test_delete_backup_not_found(client, mock_backup_service):
    """Test deleting non-existent backup"""
    mock_backup_service.delete_backup.side_effect = FileNotFoundError()
    
    response = client.delete("/backups/nonexistent.sql.gz")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_cleanup_old_backups(client, mock_backup_service):
    """Test cleaning up old backups"""
    response = client.post("/backups/cleanup")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["deleted_count"] == 2
    assert len(data["deleted_files"]) == 2
    assert data["total_size_freed"] == 2048
    assert data["retention_days"] == 30
    
    mock_backup_service.cleanup_old_backups.assert_called_once()


def test_cleanup_failure(client, mock_backup_service):
    """Test cleanup operation failure"""
    mock_backup_service.cleanup_old_backups.side_effect = RuntimeError("Cleanup failed")
    
    response = client.post("/backups/cleanup")
    
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Failed to cleanup backups" in response.json()["detail"]
