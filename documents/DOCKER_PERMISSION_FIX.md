# Docker Permission Fix Documentation

## Problem
The HoppyBrew Nuxt3 frontend container was experiencing permission denied errors when trying to access build files:
```
ERROR  EACCES: permission denied, unlink '/app/.nuxt/app.config.mjs'
```

## Root Cause
The container was running as root (UID 0) while the mounted volume directory was owned by the host user (UID 1000). This mismatch caused permission conflicts when the container tried to create or modify files in the `.nuxt` build directory.

## Solution
Implemented proper user management in the Docker container to match host user permissions:

### 1. Dockerfile Changes
- Added `HOST_UID` and `HOST_GID` build arguments with defaults (1000:1000)
- Implemented graceful user/group creation that handles pre-existing IDs
- Created dedicated `appuser` matching host permissions
- Pre-created `.nuxt` directory with correct ownership
- Run container processes as non-root user

### 2. Docker Compose Changes
- Pass `HOST_UID` and `HOST_GID` as build arguments from environment
- Added anonymous volume for `/app/node_modules` to prevent permission conflicts
- Explicit `yarn install` before starting dev server

## Usage

### Default (UID/GID 1000)
```bash
docker compose up frontend
```

### Custom UID/GID
```bash
export HOST_UID=$(id -u)
export HOST_GID=$(id -g)
docker compose up frontend
```

## Benefits
- ✅ No permission errors when accessing mounted volumes
- ✅ Works across different host environments
- ✅ Matches best practices for Docker user management
- ✅ Enables proper hot reloading in development
- ✅ Files created in container have correct host ownership

## Technical Details

### User Creation Logic
```dockerfile
RUN if ! getent group ${HOST_GID} > /dev/null 2>&1; then \
      addgroup -g ${HOST_GID} appuser; \
    fi && \
    if ! getent passwd ${HOST_UID} > /dev/null 2>&1; then \
      adduser -u ${HOST_UID} -G $(getent group ${HOST_GID} | cut -d: -f1) -s /bin/sh -D appuser; \
    fi
```

This checks if the GID/UID already exist before attempting to create them, preventing build failures on systems where these IDs are already assigned.

### Directory Ownership
```dockerfile
RUN mkdir -p /app/.nuxt && \
    chown -R ${HOST_UID}:${HOST_GID} /app
```

Pre-creates the build directory and ensures all files in `/app` are owned by the correct user.

## Testing
To verify the fix:
1. Build the container: `docker compose build frontend`
2. Start the container: `docker compose up frontend -d`
3. Check logs: `docker compose logs frontend`
4. Verify no permission errors appear in logs
5. Check file ownership: `docker compose exec frontend ls -la /app/.nuxt`

## Notes
- The solution uses Alpine Linux user management commands (`addgroup`, `adduser`)
- Anonymous volumes prevent node_modules permission issues
- Development dependencies are installed at runtime for flexibility
