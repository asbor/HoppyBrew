# Docker Agent - HoppyBrew Project

## Role & Responsibilities

The Docker Agent is responsible for:
- Container orchestration and management
- Docker and Docker Compose configuration
- Troubleshooting containerization issues
- Network configuration and port management
- Volume management and data persistence
- Image building and optimization
- Multi-container application deployment

## Current Environment

### System Information
- **OS**: Fedora Linux
- **Docker Version**: 28.5.1, build 2.fc42
- **Docker Compose Version**: 2.40.0
- **Firewall**: firewalld (running, nftables backend)

### Known Issues

#### Issue #1: Docker Daemon Fails to Start
**Status**: ACTIVE
**Priority**: HIGH
**Error**: `failed to register "bridge" driver: failed to create NAT chain DOCKER: COMMAND_FAILED: INVALID_IPV: 'ipv4' is not a valid backend or is unavailable`

**Root Cause**: 
- Fedora uses nftables by default
- Docker needs iptables compatibility
- Missing kernel modules or firewall configuration

**Attempted Solutions**:
1. ✅ Verified iptables-nft is installed
2. ✅ Added docker0 to firewalld trusted zone
3. ✅ Created `/etc/docker/daemon.json` with iptables enabled
4. ⏳ Need to load kernel modules or configure nftables properly

**Next Steps**:
1. Check if kernel modules are loaded: `lsmod | grep ip_tables`
2. Load required modules if missing:
   ```bash
   sudo modprobe ip_tables
   sudo modprobe iptable_nat
   sudo modprobe iptable_filter
   ```
3. Alternative: Configure Docker to use nftables directly
4. Alternative: Temporarily disable firewalld for testing
5. Check SELinux status and permissions

## Project Configuration

### Docker Compose Setup
**File**: `docker-compose.yml`

**Services**:
1. **backend** (hoppybrew-backend-1)
   - Build: `./services/backend`
   - Port: 8000:8000
   - Command: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
   - Depends on: db
   - Env file: `.env`

2. **db** (hoppybrew-db-1)
   - Image: postgres:latest
   - Port: 5432:5432
   - Environment:
     - POSTGRES_USER=postgres
     - POSTGRES_PASSWORD=postgres
     - POSTGRES_DB=hoppybrew_db
   - Volume: postgres_data

3. **frontend** (hoppybrew-frontend-1)
   - Build: `./services/nuxt3-shadcn`
   - Port: 3000:3000
   - Command: `yarn && yarn dev`

**Network**: my-network (bridge driver)

### Environment Configuration
**File**: `.env` (root directory)

```properties
TESTING=1
DATABASE_HOST="hoppybrew-db-1"
DATABASE_PORT="5432"
DATABASE_NAME="hoppybrew_db"
DATABASE_USER="postgres"
DATABASE_PASSWORD="postgres"
```

### Docker Daemon Configuration
**File**: `/etc/docker/daemon.json`

```json
{
  "iptables": true
}
```

## Common Tasks

### Start All Services
```bash
docker-compose up -d
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f db
docker-compose logs -f frontend
```

### Stop All Services
```bash
docker-compose down
```

### Rebuild Services
```bash
# Rebuild all
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
```

### Check Service Status
```bash
docker-compose ps
```

### Access Container Shell
```bash
# Backend
docker exec -it hoppybrew-backend-1 /bin/bash

# Database
docker exec -it hoppybrew-db-1 psql -U postgres -d hoppybrew_db

# Frontend
docker exec -it hoppybrew-frontend-1 /bin/sh
```

### Clean Up
```bash
# Remove containers, networks, and volumes
docker-compose down -v

# Remove all unused containers, networks, images
docker system prune -a
```

## Troubleshooting Guide

### Docker Daemon Won't Start

**Check Status**:
```bash
sudo systemctl status docker
sudo journalctl -xeu docker.service --no-pager | tail -50
```

**Common Solutions**:
1. Check firewall configuration
2. Verify kernel modules are loaded
3. Check SELinux context
4. Review `/etc/docker/daemon.json`
5. Check for port conflicts

### Container Won't Start

**Debug Steps**:
```bash
# Check logs
docker logs <container_name>

# Inspect container
docker inspect <container_name>

# Check resource usage
docker stats

# Verify network
docker network ls
docker network inspect my-network
```

### Database Connection Issues

**Verify**:
```bash
# Check if database is running
docker-compose ps db

# Test connection from host
docker exec hoppybrew-db-1 psql -U postgres -d hoppybrew_db -c "SELECT version();"

# Check database logs
docker-compose logs db
```

### Port Already in Use

**Find Process**:
```bash
sudo lsof -i :8000  # Backend
sudo lsof -i :3000  # Frontend
sudo lsof -i :5432  # Database
```

**Solutions**:
1. Stop conflicting process
2. Change port mapping in docker-compose.yml
3. Update .env file with new ports

### Volume Permission Issues

**Check Permissions**:
```bash
ls -la services/backend
ls -la services/nuxt3-shadcn
```

**Fix Permissions**:
```bash
# Fix ownership
sudo chown -R $USER:$USER services/

# Fix SELinux context (if enabled)
sudo chcon -R -t container_file_t services/
```

## Integration Points

### With Backend Agent
- Ensure backend Dockerfile is optimized
- Coordinate environment variables
- Manage database migrations in containers

### With Frontend Agent
- Ensure frontend Dockerfile builds correctly
- Coordinate API endpoint configuration
- Manage static asset serving

### With Database Agent
- Coordinate database initialization
- Manage volume persistence
- Handle backup and restore procedures

### With CI/CD Agent
- Provide Docker build scripts
- Configure multi-stage builds
- Optimize image sizes for deployment

## Best Practices

1. **Image Optimization**
   - Use multi-stage builds
   - Minimize layer count
   - Use .dockerignore files
   - Keep images small and focused

2. **Security**
   - Don't run as root in containers
   - Use specific image versions (not `latest`)
   - Scan images for vulnerabilities
   - Keep secrets out of images

3. **Development Workflow**
   - Use volume mounts for live reload
   - Separate dev and prod configurations
   - Use docker-compose for local development

4. **Networking**
   - Use Docker networks for isolation
   - Expose only necessary ports
   - Use environment variables for hosts

5. **Data Persistence**
   - Use named volumes for databases
   - Back up volumes regularly
   - Document volume mount points

## Quick Reference

### Useful Commands
```bash
# System info
docker info
docker version
docker-compose version

# Clean up everything
docker system prune -a --volumes

# View resource usage
docker stats

# Export/Import volumes
docker run --rm -v postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
docker run --rm -v postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /data

# Network debugging
docker network inspect my-network
docker exec <container> ping <other_container>
```

## Status Tracking

### Current Priority
1. ✅ CRITICAL: Fix Docker daemon startup issue
2. ⏳ Start all services successfully
3. ⏳ Verify backend API is accessible
4. ⏳ Verify frontend is accessible
5. ⏳ Test database connectivity
6. ⏳ Validate full application stack

### Metrics to Monitor
- [ ] Docker daemon running successfully
- [ ] All 3 containers running
- [ ] Backend responding on http://localhost:8000
- [ ] Frontend responding on http://localhost:3000
- [ ] Database accepting connections
- [ ] No error logs in any container

---

**Last Updated**: 2025-11-05
**Status**: Docker daemon troubleshooting in progress
**Next Action**: Resolve nftables/iptables compatibility issue
