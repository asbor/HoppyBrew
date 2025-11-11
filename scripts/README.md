# HoppyBrew Utility Scripts

This directory contains utility scripts for managing and maintaining the HoppyBrew application.

## Available Scripts

### 🔍 find_hardcoded_urls.sh

**Purpose:** Scans the frontend codebase for hardcoded `http://localhost:8000` URLs that should be migrated to use `useApiConfig()`.

**Usage:**
```bash
./scripts/find_hardcoded_urls.sh
```

**Output:**
- Lists all files containing hardcoded URLs
- Shows the number of occurrences in each file
- Provides replacement guidance
- Excludes test files and configuration files (which legitimately contain localhost URLs)

**When to use:**
- Before starting migration work to see current state
- After making changes to verify fixes
- As part of code review process
- When troubleshooting connectivity issues

**Example Output:**
```
🔍 Scanning for hardcoded API URLs in frontend code...

Files with hardcoded 'http://localhost:8000':

❌ services/nuxt3-shadcn/pages/batches/newBatch.vue (2 occurrence(s))
   86:        const response = await fetch('http://localhost:8000/recipes', {
   106:        const response = await fetch('http://localhost:8000/batches', {

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
Total hardcoded URLs found: 34

⚠️  Action Required:
   Replace these hardcoded URLs with useApiConfig()
```

---

### ✅ validate_fixes.sh

**Purpose:** Validates that the API connectivity infrastructure fixes are correctly implemented.

**Usage:**
```bash
./scripts/validate_fixes.sh
```

**Checks:**
1. Docker Compose configuration uses service names
2. useApiConfig composable exists
3. Documentation files are present
4. Remaining hardcoded URLs (informational)
5. Migrated files use useApiConfig correctly
6. Environment configuration is documented

**When to use:**
- After making infrastructure changes
- Before committing changes
- As part of CI/CD pipeline
- When setting up development environment
- To verify deployment readiness

**Example Output:**
```
╔════════════════════════════════════════════════════════════╗
║       HoppyBrew API Connectivity Validation Script        ║
╚════════════════════════════════════════════════════════════╝

[1/6] Checking Docker Compose Configuration...
✅ Docker Compose configured correctly

[2/6] Checking useApiConfig composable...
✅ useApiConfig composable exists

...

✅ Validation Complete!
```

---

## Quick Reference

### Check Current Status
```bash
# Scan for hardcoded URLs
./scripts/find_hardcoded_urls.sh

# Validate infrastructure
./scripts/validate_fixes.sh
```

### Development Workflow

1. **Before making changes:**
   ```bash
   ./scripts/validate_fixes.sh  # Ensure starting point is correct
   ./scripts/find_hardcoded_urls.sh  # See what needs to be fixed
   ```

2. **While making changes:**
   - Follow patterns in MIGRATION_GUIDE.md
   - Test each file after migration

3. **After making changes:**
   ```bash
   ./scripts/find_hardcoded_urls.sh  # Verify fixes
   ./scripts/validate_fixes.sh  # Ensure no regressions
   ```

4. **Before committing:**
   ```bash
   ./scripts/validate_fixes.sh
   git add .
   git commit -m "Fix hardcoded URLs in [component name]"
   ```

---

## Related Documentation

- **[CONNECTIVITY_SUMMARY.md](../CONNECTIVITY_SUMMARY.md)** - Overview of connectivity fixes
- **[DEBUGGING_GUIDE.md](../DEBUGGING_GUIDE.md)** - Troubleshooting connectivity issues
- **[API_BEST_PRACTICES.md](../API_BEST_PRACTICES.md)** - How to write API-calling code
- **[MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md)** - Step-by-step migration guide

---

## Script Maintenance

### Adding New Scripts

When adding new utility scripts:

1. Make script executable:
   ```bash
   chmod +x scripts/your_script.sh
   ```

2. Add documentation to this README

3. Follow naming conventions:
   - Use snake_case
   - Use `.sh` extension
   - Use descriptive names

4. Include:
   - Shebang: `#!/bin/bash`
   - Error handling: `set -e`
   - Usage help
   - Clear output messages

### Script Template

```bash
#!/bin/bash

# Brief description of what the script does

set -e

cd "$(dirname "$0")/.."

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Script Title${NC}"
echo ""

# Your script logic here

echo -e "${GREEN}✅ Complete!${NC}"
```

---

## Troubleshooting

### Script Not Executable

**Error:** `Permission denied`

**Solution:**
```bash
chmod +x scripts/script_name.sh
```

### Script Not Found

**Error:** `No such file or directory`

**Solution:** Run from repository root:
```bash
cd /path/to/HoppyBrew
./scripts/script_name.sh
```

### Colors Not Showing

**Issue:** ANSI color codes not rendering

**Solution:** Most modern terminals support colors. If not:
- Use a different terminal (e.g., bash, zsh)
- Or pipe to `cat` to remove color codes

---

## Future Script Ideas

Potential scripts to add in the future:

- `lint_all.sh` - Run linters on all code
- `test_all.sh` - Run all tests (backend + frontend)
- `setup_dev.sh` - One-command dev environment setup
- `check_dependencies.sh` - Verify all dependencies are installed
- `backup_db.sh` - Backup database
- `deploy.sh` - Deployment automation
- `health_check.sh` - Comprehensive health check of all services

---

## Contributing

When adding scripts:
1. Test thoroughly
2. Document in this README
3. Follow existing patterns
4. Add error handling
5. Make output user-friendly

---

Last Updated: 2025-11-11
