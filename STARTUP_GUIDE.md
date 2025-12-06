# HoppyBrew Startup & Debugging Guide

**Last Updated:** 2025-11-11  
**Purpose:** One-stop guide to start the application and debug network issues

---

## 🚀 Quick Start (Local Development)

### Prerequisites Check
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check Python environment
python --version  # Should be 3.13+

# Check Node.js
node --version    # Should be 18+
npm --version
```

### Start Services (3 steps)

#### 1. Start Database
```bash
# If PostgreSQL is not running:
sudo systemctl start postgresql

# Verify:
psql -U postgres -d hoppybrew -c "SELECT 1;"
```

#### 2. Start Backend (FastAPI)
```bash
# Set this once (adjust if you cloned somewhere else)
REPO_ROOT="${REPO_ROOT:-/home/asbo/repo/MyHomeLab/MyProjects/HoppyBrew}"
# Alternatively: REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

cd "${REPO_ROOT}/services/backend"

# Method 1: Using uvicorn directly (RECOMMENDED)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
echo $! > /tmp/backend.pid

# Method 2: Using helper script
"${REPO_ROOT}/start_backend.sh" > /tmp/backend.log 2>&1 &
echo $! > /tmp/backend.pid

# Verify backend is running:
curl -s http://localhost:8000/health
# Expected: {"status":"ok","detail":"Database, cache, and background workers are healthy."}
```

#### 3. Start Frontend (Nuxt)
```bash
cd "${REPO_ROOT:-/home/asbo/repo/MyHomeLab/MyProjects/HoppyBrew}/services/nuxt3-shadcn"

# Start with explicit host binding (CRITICAL for IPv4 support)
npm run dev -- --host 0.0.0.0 > /tmp/nuxt.log 2>&1 &
echo $! > /tmp/nuxt.pid

# (Alternative) helper script:
#   "${REPO_ROOT}/start_frontend.sh" > /tmp/nuxt.log 2>&1 &
#   echo $! > /tmp/nuxt.pid

# Verify frontend is running:
curl -4 -I http://localhost:3000
# Expected: HTTP/1.1 200 OK
```

### Verification Checklist
- [ ] Backend: `curl http://localhost:8000/health` returns `{"status":"ok",...}`
- [ ] Frontend: `curl -4 http://localhost:3000` returns `HTTP/1.1 200 OK`
- [ ] IPv4 binding: `ss -tlnp | grep :3000` shows `0.0.0.0:3000` (NOT `[::1]:3000`)
- [ ] IPv4 binding: `ss -tlnp | grep :8000` shows `0.0.0.0:8000`
- [ ] Browser: Open http://localhost:3000 - Dashboard loads without network errors
- [ ] API connectivity: Open http://localhost:3000/debug-api and confirm ✅ on Health/Recipes/Batches

---

## 🔍 Debugging Network Errors

### "NetworkError when attempting to fetch resource"

This means the **frontend cannot reach the backend**. Follow this debugging sequence:

#### Step 1: Check if Backend is Running
```bash
# Check process
ps aux | grep -E "uvicorn|python.*main.py" | grep -v grep

# If nothing shows up, backend is NOT running
# → Go to "Start Backend" section above
```

#### Step 2: Verify Backend Health
```bash
curl -s http://localhost:8000/health

# Expected output:
# {"status":"ok","detail":"Database, cache, and background workers are healthy."}

# If connection refused (exit code 7):
# → Backend is not running - start it!

# If database error:
# → Check PostgreSQL is running: sudo systemctl start postgresql
```

#### Step 3: Check Frontend API Configuration
```bash
# Check what API URL the frontend is using
cd "${REPO_ROOT:-/home/asbo/repo/MyHomeLab/MyProjects/HoppyBrew}/services/nuxt3-shadcn"
grep -r "API_BASE_URL" .env* 2>/dev/null || echo "No .env file"

# Frontend should use: http://localhost:8000
# Check nuxt.config.ts:
grep "API_URL" nuxt.config.ts
```

#### Step 4: Test API Endpoints Manually
```bash
# Test recipes endpoint
curl -s http://localhost:8000/recipes | jq '.[:2]'

# Test batches endpoint
curl -s http://localhost:8000/batches | jq '.[:2]'

# Test inventory endpoints
curl -s http://localhost:8000/hops | jq '.[:2]'
curl -s http://localhost:8000/fermentables | jq '.[:2]'

# If any fail with connection refused:
# → Backend is not running or not listening on correct port
```

#### Step 5: Check Browser Console
Open Developer Tools (F12) and check Console tab for:
- Fetch errors with specific endpoints
- CORS errors (red flag: backend not running)
- Network tab shows failed requests (status 0 or "Failed to fetch")

#### Step 6: Use the API Debug Page
- Navigate to `http://localhost:3000/debug-api`
- Health, recipes, and batches checks run automatically
- If any box is red, confirm the backend is running on port 8000

---

## 🛠️ Common Issues & Solutions

### Issue: Frontend only on IPv6 (can't connect from browser)

**Symptom:** `ss -tlnp | grep :3000` shows `[::1]:3000` instead of `0.0.0.0:3000`

**Solution:**
```bash
# Kill existing Nuxt process
pkill -f "node.*nuxt"

# Restart with explicit host binding
cd "${REPO_ROOT:-/home/asbo/repo/MyHomeLab/MyProjects/HoppyBrew}/services/nuxt3-shadcn"
npm run dev -- --host 0.0.0.0 > /tmp/nuxt.log 2>&1 &

# Verify:
ss -tlnp | grep :3000  # Should show 0.0.0.0:3000
curl -4 -I http://localhost:3000  # Should return HTTP 200
```

### Issue: Backend exits immediately after start

**Symptom:** Process starts but `ps aux | grep uvicorn` shows nothing

**Common Causes:**
1. Database connection failure (.env misconfiguration)
2. Port 8000 already in use
3. Python import errors

**Debug:**
```bash
# Check logs
tail -50 /tmp/backend.log

# Common fixes:
# 1. Fix .env database settings
cat services/backend/.env
# Should have: DATABASE_HOST="localhost" (NOT "hoppybrew-db-1")

# 2. Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# 3. Test imports
cd services/backend
python -c "from main import app; print('OK')"
```

### Issue: "Invalid status 'brew_day'" error

**Status:** ✅ FIXED (2025-11-11)

**Background:** Frontend used `brew_day` status but backend enum only accepts:
- `planning`, `brewing`, `fermenting`, `conditioning`, `packaging`, `complete`, `archived`

**Fix Applied:**
- Replaced all `brew_day` references with `brewing` across 5 frontend files
- Migration script created to fix database records
- See commit `f268efa` for details

**Remaining Status Mismatches:** (documented in ISSUE-006)
- Frontend uses: `primary_fermentation`, `secondary_fermentation`, `packaged`, `completed`
- Backend expects: `fermenting`, `fermenting`, `packaging`, `complete`
- TODO: Implement status mapping in `useBatches` composable

### Issue: Database connection refused

**Symptom:** Backend logs show "Connection refused" or "could not connect to server"

**Solution:**
```bash
# 1. Check PostgreSQL status
sudo systemctl status postgresql

# If not running:
sudo systemctl start postgresql

# 2. Verify database exists
psql -U postgres -l | grep hoppybrew

# If missing, create it:
psql -U postgres -c "CREATE DATABASE hoppybrew;"

# 3. Test connection
psql -U postgres -d hoppybrew -c "SELECT version();"
```

---

## 📊 Service Status Commands

### Check Everything at Once
```bash
# Quick status check script
echo "=== PostgreSQL ===" && sudo systemctl status postgresql --no-pager -l | head -3
echo -e "\n=== Backend (port 8000) ===" && ss -tlnp | grep :8000 || echo "Not listening"
echo -e "\n=== Backend Health ===" && curl -s http://localhost:8000/health || echo "Not responding"
echo -e "\n=== Frontend (port 3000) ===" && ss -tlnp | grep :3000 || echo "Not listening"
echo -e "\n=== Frontend IPv4 ===" && curl -4 -I http://localhost:3000 2>&1 | head -1 || echo "Failed"
```

### Stop All Services
```bash
# Stop frontend
pkill -f "node.*nuxt"

# Stop backend
pkill -f "uvicorn"

# Stop PostgreSQL (optional - usually keep running)
sudo systemctl stop postgresql
```

---

## 🔧 Environment Configuration

### Backend `.env` (services/backend/.env)
```bash
# Database (LOCAL DEVELOPMENT)
DATABASE_HOST="localhost"          # NOT "hoppybrew-db-1" for local dev
DATABASE_PORT=5432
DATABASE_NAME="hoppybrew"
DATABASE_USER="postgres"
DATABASE_PASSWORD="your_password"

# API
API_HOST="0.0.0.0"
API_PORT=8000

# Development
DEBUG=True
LOG_LEVEL="DEBUG"
```

### Frontend `nuxt.config.ts`
```typescript
runtimeConfig: {
  API_URL: process.env.API_BASE_URL || "http://localhost:8000",
  public: {
    API_URL: process.env.API_BASE_URL || "http://localhost:8000",
  }
}
```

---

## 🐛 Debugging Tools

### Network Inspection
```bash
# Check what's listening on ports
ss -tlnp | grep -E ":(3000|8000)"

# Test IPv4 vs IPv6
curl -4 http://localhost:3000  # Force IPv4
curl -6 http://localhost:3000  # Force IPv6

# Detailed connection test
curl -v http://localhost:8000/health 2>&1 | grep -E "Connected|HTTP"
```

### Process Inspection
```bash
# Find Nuxt processes
ps aux | grep -E "node.*nuxt|npm.*dev" | grep -v grep

# Find backend processes
ps aux | grep -E "uvicorn|python.*main" | grep -v grep

# Check process tree
pstree -p | grep -E "node|python|uvicorn"
```

### Log Monitoring
```bash
# Backend logs (if using redirected output)
tail -f /tmp/backend.log

# Frontend logs (if using redirected output)
tail -f /tmp/nuxt.log

# Follow both simultaneously
tail -f /tmp/backend.log /tmp/nuxt.log
```

---

## 📝 Development Workflow

### Typical Day Start
1. `sudo systemctl start postgresql` (if not running)
2. Start backend in one terminal: `cd services/backend && python -m uvicorn main:app --reload --host 0.0.0.0`
3. Start frontend in another terminal: `cd services/nuxt3-shadcn && npm run dev -- --host 0.0.0.0`
4. Open http://localhost:3000
5. Keep terminals visible to monitor logs

### After Git Pull
1. **Backend:** `cd services/backend && pip install -r requirements.txt`
2. **Frontend:** `cd services/nuxt3-shadcn && npm install`
3. **Database:** Check for migration scripts in `services/backend/` (e.g., `fix_batch_statuses.py`)
4. **Restart services** to pick up changes

### Before Committing
1. Check for uncommitted changes: `git status`
2. Run backend tests: `cd services/backend && pytest`
3. Run frontend tests: `cd services/nuxt3-shadcn && npm run test:unit`
4. Verify app still works: Test dashboard, recipes, batches pages

---

## 🎯 Emergency Recovery

If nothing works and you're stuck in a loop:

```bash
# 1. STOP EVERYTHING
pkill -f "node.*nuxt"
pkill -f "uvicorn"

# 2. VERIFY CLEAN STATE
ps aux | grep -E "node|uvicorn|python.*main" | grep -v grep
# Should show nothing related to app

# 3. VERIFY PORTS ARE FREE
ss -tlnp | grep -E ":(3000|8000)"
# Should show nothing

# 4. VERIFY DATABASE
sudo systemctl status postgresql
psql -U postgres -d hoppybrew -c "SELECT COUNT(*) FROM recipes;"

# 5. RESTART FROM SCRATCH
cd "${REPO_ROOT:-/home/asbo/repo/MyHomeLab/MyProjects/HoppyBrew}"

# Backend
cd services/backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
sleep 3
curl http://localhost:8000/health  # Must succeed before continuing

# Frontend
cd ../nuxt3-shadcn
npm run dev -- --host 0.0.0.0 &
sleep 5
curl -4 -I http://localhost:3000  # Must succeed

# 6. OPEN BROWSER
# http://localhost:3000
```

---

## 📚 Related Documentation

- **API Documentation:** http://localhost:8000/docs (when backend is running)
- **Issue Tracker:** `documents/issues/` - Known issues and fixes
- **Database Schema:** `services/backend/Database/Schemas/`
- **Frontend Composables:** `services/nuxt3-shadcn/composables/` - API integration

---

## 🔗 Quick Reference

| Service | URL | Check Command | Log File |
|---------|-----|---------------|----------|
| Backend API | http://localhost:8000 | `curl http://localhost:8000/health` | `/tmp/backend.log` |
| Frontend | http://localhost:3000 | `curl -4 -I http://localhost:3000` | `/tmp/nuxt.log` |
| API Docs | http://localhost:8000/docs | Open in browser | N/A |
| PostgreSQL | localhost:5432 | `sudo systemctl status postgresql` | `/var/log/postgresql/` |

---

**Remember:** The most common issue is **backend not running**. Always check `curl http://localhost:8000/health` first!
