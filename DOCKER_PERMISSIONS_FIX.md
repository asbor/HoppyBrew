# Docker Permission Issues - Resolution Guide

## Problem Description

When running the HoppyBrew application with Docker Compose, users encountered permission errors like:

```
ERROR  EACCES: permission denied, unlink '/app/.nuxt/app.config.mjs'
```

This occurred because:
1. Docker containers run with root user by default
2. Volume mounts map host directories to container directories
3. Files created inside the container are owned by the container's user (often root)
4. When the container tries to modify files in the mounted volume, permission conflicts occur

## Solution Overview

We've implemented a comprehensive fix that:
1. Creates non-root users in both frontend and backend containers
2. Uses configurable UID/GID to match the host user
3. Adds proper .dockerignore files to prevent copying unnecessary files
4. Uses anonymous volumes for directories that should not be shared with the host

## Changes Made

### 1. Frontend Dockerfile (`services/nuxt3-shadcn/Dockerfile`)
- Added `USER_UID` and `USER_GID` build arguments (default: 1000)
- Created non-root user `appuser` with the specified UID/GID
- Set proper ownership of all copied files
- Switched to non-root user before installing dependencies

### 2. Backend Dockerfile (`services/backend/Dockerfile`)
- Added `USER_UID` and `USER_GID` build arguments (default: 1000)
- Updated user creation to use the specified UID/GID
- Maintained existing non-root user approach

### 3. Docker Compose Configuration (`docker-compose.yml`)
- Added build arguments to pass HOST_UID and HOST_GID to both services
- Added anonymous volumes for `node_modules` and `.nuxt` directories
- These volumes prevent permission conflicts for auto-generated files

### 4. .dockerignore Files
- **Frontend** (`services/nuxt3-shadcn/.dockerignore`): Excludes node_modules, .nuxt, build outputs
- **Backend** (`services/backend/.dockerignore`): Excludes Python cache, virtual environments

### 5. Documentation Updates
- Updated README.md with clear instructions
- Created helper script for easier usage

## How to Use

### Method 1: Using the Helper Script (Recommended)

```bash
# Make sure the script is executable
chmod +x docker-compose-helper.sh

# Start the services
./docker-compose-helper.sh up

# Or with any docker-compose command
./docker-compose-helper.sh up -d
./docker-compose-helper.sh down
./docker-compose-helper.sh logs -f
```

### Method 2: Manual Environment Variables

```bash
# Export your user ID and group ID
export HOST_UID=$(id -u)
export HOST_GID=$(id -g)

# Run docker-compose
docker compose up
```

### Method 3: One-liner

```bash
HOST_UID=$(id -u) HOST_GID=$(id -g) docker compose up
```

## Technical Details

### Why This Works

1. **UID/GID Mapping**: The container's user has the same UID/GID as your host user
2. **File Ownership**: Files created in mounted volumes have correct ownership
3. **Anonymous Volumes**: Directories like `node_modules` and `.nuxt` are kept separate from the host
4. **Non-Root Security**: Running as non-root user is a security best practice

### Volume Configuration

The frontend service uses three types of volumes:

```yaml
volumes:
  - ./services/nuxt3-shadcn:/app        # Named bind mount (host <-> container)
  - /app/node_modules                    # Anonymous volume (container only)
  - /app/.nuxt                           # Anonymous volume (container only)
```

This ensures:
- Source code is shared between host and container
- Dependencies and build artifacts stay in the container
- No permission conflicts

## Troubleshooting

### Issue: Still getting permission errors

**Solution**: Make sure you're passing the UID/GID when starting the containers:
```bash
export HOST_UID=$(id -u) && export HOST_GID=$(id -g) && docker compose up --build
```

### Issue: Need to rebuild after changes

**Solution**: Force a rebuild with:
```bash
docker compose build --no-cache
export HOST_UID=$(id -u) && export HOST_GID=$(id -g) && docker compose up
```

### Issue: Existing files have wrong ownership

**Solution**: Fix ownership of existing files:
```bash
# On the host
sudo chown -R $(id -u):$(id -g) services/nuxt3-shadcn/node_modules
sudo chown -R $(id -u):$(id -g) services/nuxt3-shadcn/.nuxt
```

### Issue: Different UID on different machines

**Solution**: Always set HOST_UID and HOST_GID when building/running. The defaults (1000) work for most Linux systems, but macOS and some Linux systems may use different UIDs.

## Best Practices

1. **Always use the helper script** or set environment variables
2. **Clean build** after pulling changes: `docker compose down && docker compose build --no-cache`
3. **Check your UID**: Run `id -u` to see your user ID (should be passed to Docker)
4. **Don't commit .env files** with UID/GID values (they're host-specific)

## References

- [Docker User Namespace](https://docs.docker.com/engine/security/userns-remap/)
- [Docker Compose Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [Best Practices for Docker Volumes](https://docs.docker.com/storage/volumes/)
