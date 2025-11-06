# HoppyBrew Backup & Restore Guide

## Overview

This guide covers backup and restore procedures for HoppyBrew, ensuring your brewing data is safe and recoverable. HoppyBrew uses PostgreSQL for production data storage, making backup procedures straightforward.

## What to Backup

### Critical Data
1. **PostgreSQL Database** - All brewing data (recipes, batches, inventory, references)
2. **Environment Configuration** - `.env` file with database credentials
3. **User Uploads** - Any uploaded files (if implemented)

### Optional Data
- Application logs (for troubleshooting)
- Docker volumes (if using custom volumes)

## Backup Procedures

### Method 1: PostgreSQL pg_dump (Recommended)

This method creates a SQL dump of your database that can be restored on any PostgreSQL installation.

#### Create Backup

```bash
# Manual backup
docker exec hoppybrew-db-1 pg_dump -U postgres hoppybrew_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Or using environment variables
export DB_USER=postgres
export DB_NAME=hoppybrew_db
export BACKUP_DIR=./backups

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create timestamped backup
docker exec hoppybrew-db-1 pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/hoppybrew_backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Automated Backups with Cron

Create a backup script:

```bash
#!/bin/bash
# File: backup_hoppybrew.sh

BACKUP_DIR="/path/to/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/hoppybrew_backup_$TIMESTAMP.sql"
CONTAINER_NAME="hoppybrew-db-1"
DB_USER="postgres"
DB_NAME="hoppybrew_db"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup
docker exec $CONTAINER_NAME pg_dump -U $DB_USER $DB_NAME > "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"

# Keep only last 30 days of backups
find "$BACKUP_DIR" -name "hoppybrew_backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: ${BACKUP_FILE}.gz"
```

Make it executable and add to crontab:

```bash
chmod +x backup_hoppybrew.sh

# Add to crontab (daily at 2 AM)
crontab -e
# Add line:
0 2 * * * /path/to/backup_hoppybrew.sh >> /var/log/hoppybrew_backup.log 2>&1
```

### Method 2: Docker Volume Backup

Backup the entire PostgreSQL data volume:

```bash
# Stop the database container (optional, for consistency)
docker-compose stop db

# Create volume backup
docker run --rm \
  -v hoppybrew_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres_volume_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .

# Restart database
docker-compose start db
```

### Method 3: Custom Backup Script (Application-Level)

For more granular control, you can create a backup script:

```bash
#!/bin/bash
# File: full_backup.sh

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 1. Backup database
echo "Backing up database..."
docker exec hoppybrew-db-1 pg_dump -U postgres hoppybrew_db > "$BACKUP_DIR/database.sql"

# 2. Backup environment config
echo "Backing up environment config..."
cp .env "$BACKUP_DIR/.env.backup"

# 3. Backup any custom data files
echo "Backing up data files..."
cp -r data "$BACKUP_DIR/data" 2>/dev/null || true

# 4. Create manifest
echo "Creating backup manifest..."
cat > "$BACKUP_DIR/MANIFEST.txt" << EOF
HoppyBrew Backup
Created: $(date)
Database: hoppybrew_db
PostgreSQL Version: $(docker exec hoppybrew-db-1 psql -U postgres -c 'SELECT version();' -t | head -n1)
Application Version: $(git describe --tags --always 2>/dev/null || echo "unknown")
EOF

# 5. Compress backup
echo "Compressing backup..."
cd backups
tar czf "hoppybrew_full_backup_$(date +%Y%m%d_%H%M%S).tar.gz" "$(basename $BACKUP_DIR)"
cd ..

echo "Backup completed: $BACKUP_DIR"
```

## Restore Procedures

### Restore from pg_dump

```bash
# Method 1: Direct restore to running container
docker exec -i hoppybrew-db-1 psql -U postgres -d hoppybrew_db < backup_20251106_120000.sql

# Method 2: Recreate database and restore
docker exec hoppybrew-db-1 psql -U postgres -c "DROP DATABASE IF EXISTS hoppybrew_db;"
docker exec hoppybrew-db-1 psql -U postgres -c "CREATE DATABASE hoppybrew_db;"
docker exec -i hoppybrew-db-1 psql -U postgres -d hoppybrew_db < backup_20251106_120000.sql
```

### Restore from Compressed Backup

```bash
# Uncompress and restore
gunzip -c backup_20251106_120000.sql.gz | docker exec -i hoppybrew-db-1 psql -U postgres -d hoppybrew_db
```

### Restore from Volume Backup

```bash
# Stop containers
docker-compose down

# Remove old volume
docker volume rm hoppybrew_postgres_data

# Create new volume
docker volume create hoppybrew_postgres_data

# Restore data
docker run --rm \
  -v hoppybrew_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/postgres_volume_20251106_120000.tar.gz -C /data

# Start containers
docker-compose up -d
```

### Full System Restore

```bash
#!/bin/bash
# File: restore.sh

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: ./restore.sh <backup-file.tar.gz>"
  exit 1
fi

# Extract backup
TEMP_DIR=$(mktemp -d)
tar xzf "$BACKUP_FILE" -C "$TEMP_DIR"

# Find the backup directory
BACKUP_DIR=$(find "$TEMP_DIR" -type f -name "MANIFEST.txt" -exec dirname {} \;)

# Stop services
echo "Stopping services..."
docker-compose down

# Restore database
echo "Restoring database..."
docker-compose up -d db
sleep 5
docker exec hoppybrew-db-1 psql -U postgres -c "DROP DATABASE IF EXISTS hoppybrew_db;"
docker exec hoppybrew-db-1 psql -U postgres -c "CREATE DATABASE hoppybrew_db;"
docker exec -i hoppybrew-db-1 psql -U postgres -d hoppybrew_db < "$BACKUP_DIR/database.sql"

# Restore environment
echo "Restoring environment..."
cp "$BACKUP_DIR/.env.backup" .env

# Restore data files
echo "Restoring data files..."
rm -rf data
cp -r "$BACKUP_DIR/data" data 2>/dev/null || true

# Start all services
echo "Starting all services..."
docker-compose up -d

# Cleanup
rm -rf "$TEMP_DIR"

echo "Restore completed!"
```

## Backup Best Practices

### 1. Regular Backups
- **Daily**: Automated database backups via cron
- **Weekly**: Full system backups including volumes
- **Before Updates**: Manual backup before upgrading

### 2. Backup Retention
- Keep daily backups for 7 days
- Keep weekly backups for 4 weeks
- Keep monthly backups for 12 months
- Keep yearly backups indefinitely

### 3. Off-Site Storage
Store backups in multiple locations:
- Local disk (fast recovery)
- Network storage (NAS)
- Cloud storage (S3, Backblaze, etc.)
- External hard drive (offline backup)

### 4. Test Restores
- Test restore procedure monthly
- Verify data integrity
- Document restore time

### 5. Backup Security
```bash
# Encrypt backups (recommended for off-site storage)
gpg --symmetric --cipher-algo AES256 backup_20251106_120000.sql

# Decrypt when needed
gpg --decrypt backup_20251106_120000.sql.gpg > backup_20251106_120000.sql
```

## Backup to Cloud Storage

### AWS S3 Example

```bash
#!/bin/bash
# Backup to S3

BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
S3_BUCKET="s3://my-hoppybrew-backups"

# Create backup
docker exec hoppybrew-db-1 pg_dump -U postgres hoppybrew_db > "$BACKUP_FILE"

# Compress and encrypt
gzip "$BACKUP_FILE"
gpg --symmetric --cipher-algo AES256 "${BACKUP_FILE}.gz"

# Upload to S3
aws s3 cp "${BACKUP_FILE}.gz.gpg" "$S3_BUCKET/"

# Cleanup local files
rm "${BACKUP_FILE}.gz.gpg"
```

### Rclone Example (works with multiple cloud providers)

```bash
#!/bin/bash
# Backup using rclone

BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
REMOTE="mycloud:hoppybrew-backups"

# Create and compress backup
docker exec hoppybrew-db-1 pg_dump -U postgres hoppybrew_db | gzip > "${BACKUP_FILE}.gz"

# Upload to cloud
rclone copy "${BACKUP_FILE}.gz" "$REMOTE"

# Cleanup
rm "${BACKUP_FILE}.gz"
```

## Disaster Recovery Plan

### Recovery Time Objective (RTO)
Target: Restore service within 1 hour

### Recovery Point Objective (RPO)
Target: Maximum 24 hours of data loss (with daily backups)

### Emergency Restore Steps

1. **Identify the Problem**
   - Data corruption
   - Hardware failure
   - Accidental deletion

2. **Stop Services**
   ```bash
   docker-compose down
   ```

3. **Locate Latest Valid Backup**
   ```bash
   ls -lht backups/ | head
   ```

4. **Restore Database**
   ```bash
   docker-compose up -d db
   docker exec -i hoppybrew-db-1 psql -U postgres -d hoppybrew_db < latest_backup.sql
   ```

5. **Verify Restore**
   - Check record counts
   - Verify recent data
   - Test critical operations

6. **Start Application**
   ```bash
   docker-compose up -d
   ```

7. **Document Incident**
   - What happened
   - How it was resolved
   - Lessons learned

## Monitoring & Alerts

### Backup Monitoring Script

```bash
#!/bin/bash
# Check if backup is recent

BACKUP_DIR="/path/to/backups"
MAX_AGE_HOURS=26  # Alert if backup older than 26 hours

LATEST_BACKUP=$(find "$BACKUP_DIR" -name "hoppybrew_backup_*.sql.gz" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2)

if [ -z "$LATEST_BACKUP" ]; then
  echo "ERROR: No backups found!"
  exit 1
fi

BACKUP_AGE_HOURS=$(( ($(date +%s) - $(stat -c %Y "$LATEST_BACKUP")) / 3600 ))

if [ $BACKUP_AGE_HOURS -gt $MAX_AGE_HOURS ]; then
  echo "WARNING: Latest backup is $BACKUP_AGE_HOURS hours old!"
  exit 1
else
  echo "OK: Latest backup is $BACKUP_AGE_HOURS hours old"
  exit 0
fi
```

## Troubleshooting

### Backup Fails - Permission Denied
```bash
# Ensure docker user has write permissions
sudo chown -R $USER:$USER ./backups
```

### Restore Fails - Database Exists
```bash
# Drop database first
docker exec hoppybrew-db-1 psql -U postgres -c "DROP DATABASE hoppybrew_db;"
docker exec hoppybrew-db-1 psql -U postgres -c "CREATE DATABASE hoppybrew_db;"
```

### Backup File Too Large
```bash
# Use compression
docker exec hoppybrew-db-1 pg_dump -U postgres hoppybrew_db | gzip > backup.sql.gz

# Or use custom format (better compression)
docker exec hoppybrew-db-1 pg_dump -U postgres -Fc hoppybrew_db > backup.dump
```

## Additional Resources

- [PostgreSQL Backup Documentation](https://www.postgresql.org/docs/current/backup.html)
- [Docker Volume Backup Best Practices](https://docs.docker.com/storage/volumes/#back-up-restore-or-migrate-data-volumes)
- [Backup Encryption with GPG](https://www.gnupg.org/gph/en/manual/x110.html)

## Support

For backup-related questions or issues:
1. Check the [troubleshooting section](#troubleshooting)
2. Review application logs
3. Open an issue on GitHub
4. Contact support

---

**Remember**: A backup is only as good as your last successful restore test!
