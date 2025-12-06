# Debugging Guide: API Connectivity Issues

## Overview

This guide documents common connectivity issues between the HoppyBrew frontend and backend, their root causes, and solutions. Use this guide when experiencing "NetworkError when attempting to fetch resource" or similar connectivity problems.

## Table of Contents

1. [Common Issues](#common-issues)
2. [Diagnostic Steps](#diagnostic-steps)
3. [Solutions](#solutions)
4. [Prevention](#prevention)
5. [Architecture](#architecture)

---

## Common Issues

### 1. NetworkError When Fetching Resources

**Symptoms:**
- Browser console shows: `NetworkError when attempting to fetch resource`
- API calls fail with CORS errors
- Frontend cannot reach backend endpoints

**Root Causes:**
- Hardcoded `http://localhost:8000` URLs in components
- Incorrect `API_BASE_URL` environment variable
- Backend not running or not accessible
- CORS misconfiguration
- Multiple backend instances running on the same port

### 2. CORS Errors

**Symptoms:**
- Browser console shows: `Access to fetch at 'http://...' from origin 'http://...' has been blocked by CORS policy`
- Preflight OPTIONS requests failing

**Root Causes:**
- Backend CORS settings don't include frontend origin
- Backend not responding to OPTIONS requests
- Middleware configuration issues

### 3. Mixed Content Errors

**Symptoms:**
- HTTPS pages trying to load HTTP resources
- Browser blocking requests due to security policies

**Root Causes:**
- Production deployment using HTTPS for frontend but HTTP for backend API URLs

---

## Diagnostic Steps

### Step 1: Verify Backend is Running

#### Docker Environment:
```bash
# Check if backend container is running
docker ps | grep hoppybrew-backend

# Check backend logs
docker logs hoppybrew-backend-1

# Test backend health endpoint from host
curl http://localhost:8000/health

# Test backend health endpoint from within Docker network
docker exec hoppybrew-frontend-1 curl http://hoppybrew-backend-1:8000/health
```

#### Local Development:
```bash
# Check if Uvicorn is running
ps aux | grep uvicorn

# Check for multiple instances (common issue!)
pgrep -f "uvicorn.*main:app" | wc -l

# Test health endpoint
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "detail": "Database, cache, and background workers are healthy."
}
```

### Step 2: Verify Frontend Configuration

#### Check Environment Variables:
```bash
# In Docker
docker exec hoppybrew-frontend-1 printenv | grep API

# Local development
cd services/nuxt3-shadcn
cat .env
```

#### Check Runtime Configuration:
Open browser console and run:
```javascript
// This will log current API configuration
const { logConfig } = useApiConfig()
logConfig()
```

### Step 3: Check Network Connectivity

#### Docker Environment:
```bash
# Test connectivity between containers
docker exec hoppybrew-frontend-1 ping -c 3 hoppybrew-backend-1

# Check DNS resolution
docker exec hoppybrew-frontend-1 nslookup hoppybrew-backend-1

# Verify both containers are on same network
docker network inspect hoppybrew_my-network
```

#### Local Development:
```bash
# Test localhost connectivity
curl -v http://localhost:8000/health
curl -v http://localhost:3000
```

### Step 4: Check for Port Conflicts

```bash
# Check what's running on port 8000
lsof -i :8000

# Check what's running on port 3000
lsof -i :3000

# Kill processes if needed
kill -9 <PID>
```

### Step 5: Verify Browser Can Reach API

1. Open browser to: `http://localhost:3000`
2. Open Developer Tools (F12)
3. Go to Network tab
4. Try to perform an action that calls the API
5. Look for failed requests
6. Check request URL - should NOT be hardcoded `localhost:8000` if in Docker
7. Check response headers for CORS headers

---

## Solutions

### Solution 1: Use Centralized API Configuration

**Always use `useApiConfig()` composable instead of hardcoded URLs:**

❌ **Bad:**
```typescript
const response = await fetch('http://localhost:8000/recipes')
```

✅ **Good:**
```typescript
const { buildUrl } = useApiConfig()
const response = await fetch(buildUrl('/recipes'))
```

### Solution 2: Fix Docker Networking

**For Docker deployments, ensure proper container-to-container communication:**

In `docker-compose.yml`:
```yaml
frontend:
  environment:
    # Use Docker service name, NOT localhost
    - API_BASE_URL=http://hoppybrew-backend-1:8000
```

**Note:** The frontend container makes SSR requests to the backend, so it needs to use the Docker service name. Client-side requests from the browser still use `localhost:8000` because the browser is outside the Docker network.

### Solution 3: Environment-Specific Configuration

Create `.env` file in `services/nuxt3-shadcn/`:

```bash
# For local development (both running outside Docker)
API_BASE_URL=http://localhost:8000

# For Docker development
# API_BASE_URL=http://hoppybrew-backend-1:8000

# For production
# API_BASE_URL=https://api.yourdomain.com
```

### Solution 4: Fix CORS Configuration

Ensure backend `config.py` includes your frontend origin:

```python
# In services/backend/config.py
cors_origins_str = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:3000,http://localhost:5173"
)
```

In `.env` file:
```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://hoppybrew-frontend-1:3000
```

### Solution 5: Kill Multiple Backend Instances

```bash
# Find all Uvicorn processes
pgrep -f "uvicorn.*main:app"

# Kill all instances
pkill -f "uvicorn.*main:app"

# Restart properly
cd services/backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Prevention

### Best Practices

1. **Never hardcode API URLs**
   - Always use `useApiConfig()` or `useApi()` composables
   - Use environment variables for configuration

2. **Use consistent patterns**
   - Prefer `useApiConfig().buildUrl()` for all API calls
   - Use `useApi().get/post/put/delete()` for standard CRUD operations

3. **Validate environment on startup**
   - Check that `API_BASE_URL` is set correctly
   - Log configuration in development mode
   - Add health checks

4. **Test in both environments**
   - Test locally (outside Docker)
   - Test in Docker containers
   - Verify environment variables are correct for each

5. **Document deployment requirements**
   - Document required environment variables
   - Provide example `.env` files
   - Include troubleshooting steps

### Code Review Checklist

When reviewing frontend code, check for:

- [ ] No hardcoded `http://localhost:8000` URLs
- [ ] Uses `useApiConfig()` or `useApi()` composables
- [ ] Proper error handling for network requests
- [ ] Loading states implemented
- [ ] CORS considerations for new endpoints

### Deployment Checklist

Before deploying:

- [ ] Environment variables configured correctly
- [ ] Backend accessible from frontend (test with curl)
- [ ] CORS origins include all required domains
- [ ] Health endpoints responding
- [ ] No multiple backend instances running
- [ ] Logs checked for errors
- [ ] Browser console checked for errors

---

## Architecture

### Local Development (Both Outside Docker)

```
┌─────────────────┐
│   Browser       │
│  localhost:3000 │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐      ┌──────────────┐
│  Nuxt Dev       │─────►│  FastAPI     │
│  localhost:3000 │      │  localhost:  │
│                 │      │  8000        │
└─────────────────┘      └──────────────┘

API_BASE_URL=http://localhost:8000
```

### Docker Development

```
┌─────────────────┐
│   Browser       │
│  localhost:3000 │
└────────┬────────┘
         │ HTTP (to localhost:3000)
         ▼
┌──────────────────────┐
│   Docker Network     │
│                      │
│  ┌───────────────┐   │   ┌────────────────┐
│  │  Frontend     │◄──┼───┤  Backend       │
│  │  :3000        │   │   │  :8000         │
│  └───────────────┘   │   └────────────────┘
└──────────────────────┘

From container: API_BASE_URL=http://hoppybrew-backend-1:8000
From browser: API calls to http://localhost:8000
```

**Important:** In Docker, the frontend container needs to use the backend service name for SSR, but client-side requests from the browser use `localhost` because the browser is outside the Docker network.

### Understanding the Flow

1. **Browser → Frontend Container**
   - Browser accesses `http://localhost:3000`
   - Port 3000 is mapped from container to host

2. **Frontend SSR → Backend Container**
   - Server-side rendering needs backend data
   - Uses `http://hoppybrew-backend-1:8000` (internal Docker network)

3. **Browser → Backend**
   - Client-side JavaScript API calls
   - Uses `http://localhost:8000` (port mapped from container to host)
   - Must pass through CORS since different origin

---

## Quick Reference

### Check Health
```bash
# Backend
curl http://localhost:8000/health

# Backend from Docker container
docker exec hoppybrew-frontend-1 curl http://hoppybrew-backend-1:8000/health
```

### View Logs
```bash
# Backend logs
docker logs hoppybrew-backend-1 -f

# Frontend logs
docker logs hoppybrew-frontend-1 -f
```

### Restart Services
```bash
# Restart everything
docker-compose down && docker-compose up -d

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

### Clean Restart
```bash
# Stop all containers
docker-compose down

# Remove containers, networks, volumes
docker-compose down -v

# Rebuild and start
docker-compose up -d --build
```

---

## Getting Help

If you're still experiencing issues after following this guide:

1. Collect diagnostic information:
   ```bash
   # Save this output
   docker ps
   docker logs hoppybrew-backend-1
   docker logs hoppybrew-frontend-1
   curl -v http://localhost:8000/health
   ```

2. Check browser console for errors (F12)

3. Check Network tab in browser DevTools

4. Open an issue on GitHub with:
   - Description of the problem
   - Steps to reproduce
   - Diagnostic output
   - Browser and OS information
   - Docker version (if using Docker)

---

## Summary

**The most common issue is hardcoded `http://localhost:8000` URLs in components.**

**Solution:**
1. Use `useApiConfig().buildUrl()` for all API calls
2. Configure `API_BASE_URL` correctly for your environment
3. Test in both local and Docker environments
4. Follow the diagnostic steps when issues occur

**Remember:** Configuration is environment-specific. What works locally may not work in Docker, and vice versa.
