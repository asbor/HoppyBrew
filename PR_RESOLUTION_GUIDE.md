# Manual PR Resolution Guide

Since OAuth token lacks workflow scope, use GitHub web interface

## Current Status (as of 2025-11-11)

### 📊 Open PRs: 13 Total

**Category Breakdown:**
- ⏸️ Work-in-Progress: 2 PRs
- ✅ Safe to Merge: 7 PRs  
- ⚠️ Needs Review: 4 PRs
- ❌ Invalid: 1 PR

---

## Immediate Action Required

### ❌ PR #418 - CLOSE THIS PR (Invalid Python Version)
```
URL: https://github.com/asbor/HoppyBrew/pull/418
Title: bump python from 3.12-slim to 3.14-slim
Issue: Python 3.14 does not exist!
Action: Close with comment explaining Python 3.14 doesn't exist
```

---

## Safe to Merge (7 PRs) - No Breaking Changes

### 1. ✅ PR #406 - python-jose security update
```
URL: https://github.com/asbor/HoppyBrew/pull/406
Priority: HIGH (security fixes for CVE-2024-33664 and CVE-2024-33663)
Action: Squash and merge immediately
```

### 2. ✅ PR #405 - sqlalchemy-utils
```
URL: https://github.com/asbor/HoppyBrew/pull/405
Action: Squash and merge
```

### 3. ✅ PR #403 - beautifulsoup4
```
URL: https://github.com/asbor/HoppyBrew/pull/403  
Action: Squash and merge
```

### 4. ✅ PR #401 - selenium
```
URL: https://github.com/asbor/HoppyBrew/pull/401
Action: Squash and merge
```

### 5. ✅ PR #404 - tailwind-merge
```
URL: https://github.com/asbor/HoppyBrew/pull/404
Action: Squash and merge
```

### 6. ✅ PR #397 - lucide-vue-next
```
URL: https://github.com/asbor/HoppyBrew/pull/397
Action: Squash and merge
```

---

## Review Before Merge (4 PRs) - Potential Breaking Changes

### 7. ⚠️ PR #402 - FastAPI (0.111 → 0.121)
```
URL: https://github.com/asbor/HoppyBrew/pull/402
Risk: Medium - New dependency scope features
Action: Test dependencies with yield, then merge
```

### 8. ⚠️ PR #400 - jsdom (24 → 27) **MAJOR VERSION**
```
URL: https://github.com/asbor/HoppyBrew/pull/400
Risk: High - Requires Node.js 20.19+, breaking changes
Action: Verify Node version, test thoroughly
```

### 9. ⚠️ PR #399 - eslint-config-prettier (9 → 10) **MAJOR VERSION**
```
URL: https://github.com/asbor/HoppyBrew/pull/399
Risk: Medium - Major version bump
Action: Test linting configuration
```

### 10. ⚠️ PR #398 - uuid (9 → 13) **MAJOR VERSION**
```
URL: https://github.com/asbor/HoppyBrew/pull/398
Risk: High - ESM only, drops CommonJS, drops Node 16
Action: Test all uuid imports, verify ESM usage
```

---

## Monitor (2 PRs) - Work in Progress

### 11. ⏸️ PR #421 - Fix issues in multiple PRs
```
URL: https://github.com/asbor/HoppyBrew/pull/421
Status: Draft/WIP
Action: Wait for ready for review
```

### 12. ⏸️ PR #420 - Temperature controller integration  
```
URL: https://github.com/asbor/HoppyBrew/pull/420
Status: Draft/WIP
Action: Wait for ready for review
```

---

## Quick Merge Script for Safe PRs

```bash
# Navigate to each PR and click "Squash and merge" in this order:
# 1. PR #406 (security fixes - highest priority!)
# 2. PR #405
# 3. PR #403  
# 4. PR #401
# 5. PR #404
# 6. PR #397
```

---

## Detailed Analysis

See `PR_RESOLUTION_ANALYSIS.md` for:
- Complete dependency changelog analysis
- Breaking changes documentation
- Risk assessment details
- Testing recommendations
- Merge order strategy

---

## Alternative: Re-authenticate with workflow scope
```bash
gh auth login --scopes 'repo,workflow' --web
```

## Notes
- 📊 Current token scopes: repo (missing: workflow)
- 📝 See PR_RESOLUTION_ANALYSIS.md for comprehensive details
- 🔄 Updated: 2025-11-11