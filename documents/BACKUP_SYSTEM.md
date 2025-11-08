# Backup System Documentation

## Overview

The HoppyBrew Automated Backup System provides comprehensive database backup and restore functionality with automated scheduling and retention management.

## Features

- **Automated Backups**: Schedule regular backups using cron expressions
- **Manual Backups**: Create on-demand backups via API
- **Restore Functionality**: Restore database from any backup
- **Retention Management**: Automatic cleanup of old backups
- **Compression**: All backups are compressed with gzip to save space
- **Metadata Tracking**: Each backup includes metadata (timestamp, size, description)
- **REST API**: Full REST API for backup management

## Configuration

All backup settings are configured via environment variables in `.env`:

```bash
# Enable/disable automated backups
BACKUP_ENABLED=false

# Directory to store backups
BACKUP_DIR=/app/data/backups

# Cron schedule for automated backups (default: 2 AM daily)
# Format: minute hour day month day_of_week
BACKUP_SCHEDULE=0 2 * * *

# Number of days to retain backups
BACKUP_RETENTION_DAYS=30
```

### Schedule Examples

- `0 2 * * *` - Daily at 2 AM
- `0 */6 * * *` - Every 6 hours
- `0 0 * * 0` - Weekly on Sunday at midnight
- `0 3 1 * *` - Monthly on the 1st at 3 AM

## API Endpoints

### Create Backup

Create a manual database backup.

```http
POST /backups
Content-Type: application/json

{
  "description": "Pre-upgrade backup"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Backup created successfully",
  "filename": "hoppybrew_backup_20241108_120000.sql.gz",
  "timestamp": "2024-11-08T12:00:00"
}
```

### List Backups

Get a list of all available backups.

```http
GET /backups
```

**Response:**
```json
[
  {
    "filename": "hoppybrew_backup_20241108_120000.sql.gz",
    "timestamp": "20241108_120000",
    "created_at": "2024-11-08T12:00:00",
    "description": "Pre-upgrade backup",
    "size_bytes": 1048576,
    "database_name": "hoppybrew_db",
    "database_host": "localhost"
  }
]
```

### Get Backup Info

Get detailed information about a specific backup.

```http
GET /backups/{filename}
```

**Response:**
```json
{
  "filename": "hoppybrew_backup_20241108_120000.sql.gz",
  "timestamp": "20241108_120000",
  "created_at": "2024-11-08T12:00:00",
  "description": "Pre-upgrade backup",
  "size_bytes": 1048576,
  "database_name": "hoppybrew_db",
  "database_host": "localhost"
}
```

### Restore Backup

Restore the database from a backup file.

**⚠️ WARNING**: This will overwrite all current data with the backup data!

```http
POST /backups/restore
Content-Type: application/json

{
  "filename": "hoppybrew_backup_20241108_120000.sql.gz"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Database restored successfully",
  "filename": "hoppybrew_backup_20241108_120000.sql.gz",
  "timestamp": "2024-11-08T12:05:00"
}
```

### Delete Backup

Delete a specific backup file.

```http
DELETE /backups/{filename}
```

**Response:**
```json
{
  "status": "success",
  "message": "Backup deleted successfully",
  "filename": "hoppybrew_backup_20241108_120000.sql.gz",
  "timestamp": "2024-11-08T12:10:00"
}
```

### Cleanup Old Backups

Remove backups older than the retention period.

```http
POST /backups/cleanup
```

**Response:**
```json
{
  "deleted_count": 3,
  "deleted_files": [
    "hoppybrew_backup_20241001_120000.sql.gz",
    "hoppybrew_backup_20241002_120000.sql.gz",
    "hoppybrew_backup_20241003_120000.sql.gz"
  ],
  "total_size_freed": 3145728,
  "retention_days": 30,
  "cleanup_date": "2024-11-08T12:00:00"
}
```

## Architecture

### Components

1. **BackupService** (`modules/backup_service.py`)
   - Core backup and restore logic
   - Uses PostgreSQL `pg_dump` and `psql` commands
   - Handles compression and metadata

2. **BackupScheduler** (`modules/backup_scheduler.py`)
   - APScheduler integration
   - Automated backup execution
   - Cleanup job scheduling

3. **Backup API** (`api/endpoints/backups.py`)
   - REST API endpoints
   - Request/response models
   - Error handling

### Backup Process

1. **Create Backup**
   - Execute `pg_dump` to create SQL dump
   - Compress with gzip
   - Create metadata JSON file
   - Remove uncompressed SQL file

2. **Restore Backup**
   - Decompress backup file
   - Execute `psql` to restore database
   - Clean up temporary files

3. **Cleanup**
   - List all backups
   - Calculate retention cutoff date
   - Delete backups older than retention period

## Docker Integration

The backup system is integrated with Docker Compose:

```yaml
services:
  backend:
    volumes:
      - backup_data:/app/data/backups
    # ... other configuration

volumes:
  backup_data:
```

### Backup Storage

- **Container**: `/app/data/backups`
- **Docker Volume**: `backup_data`
- **Local Development**: `./data/backups`

## Usage Examples

### Enable Automated Backups

1. Edit `.env`:
   ```bash
   BACKUP_ENABLED=true
   BACKUP_SCHEDULE=0 2 * * *
   BACKUP_RETENTION_DAYS=30
   ```

2. Restart the backend service:
   ```bash
   docker compose restart backend
   ```

### Manual Backup Before Upgrade

```bash
curl -X POST http://localhost:8000/backups \
  -H "Content-Type: application/json" \
  -d '{"description": "Before v2.0 upgrade"}'
```

### List All Backups

```bash
curl http://localhost:8000/backups
```

### Restore from Backup

```bash
curl -X POST http://localhost:8000/backups/restore \
  -H "Content-Type: application/json" \
  -d '{"filename": "hoppybrew_backup_20241108_120000.sql.gz"}'
```

### Clean Up Old Backups

```bash
curl -X POST http://localhost:8000/backups/cleanup
```

## Security Considerations

1. **Database Credentials**: Stored in environment variables
2. **Backup Access**: No authentication required (add in production!)
3. **File Permissions**: Backups stored with container user permissions
4. **Network Security**: Consider firewall rules for backup endpoints

## Troubleshooting

### Backup Creation Fails

**Error**: `pg_dump failed`

**Solution**: Verify database connectivity and credentials:
```bash
docker compose exec backend env | grep DATABASE
```

### Restore Fails

**Error**: `Database restore failed`

**Solution**: Check database is not in use:
```bash
docker compose stop backend
docker compose up -d backend
```

### Disk Space Issues

**Error**: `No space left on device`

**Solution**: Run cleanup or reduce retention period:
```bash
curl -X POST http://localhost:8000/backups/cleanup
```

### Scheduler Not Running

**Error**: No automated backups

**Solution**: Check scheduler is enabled:
```bash
# In .env
BACKUP_ENABLED=true

# Restart backend
docker compose restart backend

# Check logs
docker compose logs backend | grep -i backup
```

## Testing

Run the backup endpoint tests:

```bash
cd services/backend
pytest tests/test_endpoints/test_backups.py -v
```

## Monitoring

Check backup scheduler status in logs:

```bash
docker compose logs backend | grep -i "backup"
```

Expected log messages:
- `Backup scheduler started`
- `Running scheduled backup`
- `Scheduled backup completed`
- `Running scheduled backup cleanup`

## Best Practices

1. **Regular Backups**: Enable automated backups in production
2. **Test Restores**: Periodically test restore process
3. **Monitor Disk Space**: Keep track of backup directory size
4. **Off-site Copies**: Consider copying backups to external storage
5. **Before Upgrades**: Always create manual backup before major updates
6. **Retention Policy**: Adjust based on your needs and disk space

## Future Enhancements

Potential improvements for future versions:

- [ ] Backup encryption
- [ ] Remote storage support (S3, Azure, etc.)
- [ ] Incremental backups
- [ ] Backup verification
- [ ] Email notifications
- [ ] Backup download via API
- [ ] Multi-database support
- [ ] Authentication/authorization for endpoints
