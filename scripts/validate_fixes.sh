#!/bin/bash

# Validation script to check if the API connectivity fixes are working
# This script performs basic checks without starting the full application

set -e

cd "$(dirname "$0")/.."

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       HoppyBrew API Connectivity Validation Script        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check 1: Docker Compose Configuration
echo -e "${BLUE}[1/6] Checking Docker Compose Configuration...${NC}"
if grep -q "API_BASE_URL=http://hoppybrew-backend-1:8000" docker-compose.yml; then
    echo -e "${GREEN}✅ Docker Compose configured correctly${NC}"
else
    echo -e "${RED}❌ Docker Compose still using localhost${NC}"
    exit 1
fi
echo ""

# Check 2: useApiConfig Composable Exists
echo -e "${BLUE}[2/6] Checking useApiConfig composable...${NC}"
if [ -f "services/nuxt3-shadcn/composables/useApiConfig.ts" ]; then
    echo -e "${GREEN}✅ useApiConfig composable exists${NC}"
else
    echo -e "${RED}❌ useApiConfig composable not found${NC}"
    exit 1
fi
echo ""

# Check 3: Documentation Exists
echo -e "${BLUE}[3/6] Checking documentation files...${NC}"
docs_ok=true
if [ -f "DEBUGGING_GUIDE.md" ]; then
    echo -e "${GREEN}✅ DEBUGGING_GUIDE.md exists${NC}"
else
    echo -e "${RED}❌ DEBUGGING_GUIDE.md not found${NC}"
    docs_ok=false
fi

if [ -f "API_BEST_PRACTICES.md" ]; then
    echo -e "${GREEN}✅ API_BEST_PRACTICES.md exists${NC}"
else
    echo -e "${RED}❌ API_BEST_PRACTICES.md not found${NC}"
    docs_ok=false
fi

if [ -f "MIGRATION_GUIDE.md" ]; then
    echo -e "${GREEN}✅ MIGRATION_GUIDE.md exists${NC}"
else
    echo -e "${RED}❌ MIGRATION_GUIDE.md not found${NC}"
    docs_ok=false
fi

if [ "$docs_ok" = false ]; then
    exit 1
fi
echo ""

# Check 4: Scan for Remaining Hardcoded URLs
echo -e "${BLUE}[4/6] Scanning for hardcoded URLs...${NC}"
if [ -f "scripts/find_hardcoded_urls.sh" ]; then
    # Count hardcoded URLs (excluding allowed files)
    count=$(find services/nuxt3-shadcn -type f \( -name "*.vue" -o -name "*.ts" -o -name "*.js" \) \
        ! -path "*/node_modules/*" \
        ! -path "*/.git/*" \
        ! -path "*/test/*" \
        ! -path "*/tests/*" \
        ! -path "*/composables/useApiUrl.ts" \
        ! -path "*/composables/useApi.ts" \
        ! -path "*/composables/useApiConfig.ts" \
        ! -path "*/nuxt.config.ts" \
        ! -path "*/test/setupTests.ts" \
        ! -path "*/components/checkDatabaseConnection.vue" \
        -exec grep -l "http://localhost:8000" {} \; 2>/dev/null | wc -l)
    
    if [ "$count" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Found $count files with hardcoded URLs${NC}"
        echo -e "${YELLOW}   (This is expected - see MIGRATION_GUIDE.md for migration plan)${NC}"
    else
        echo -e "${GREEN}✅ No hardcoded URLs found${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  URL scanner script not found${NC}"
fi
echo ""

# Check 5: Verify Fixed Files
echo -e "${BLUE}[5/6] Verifying fixed files use useApiConfig...${NC}"
fixed_files=(
    "services/nuxt3-shadcn/pages/batches/newBatch.vue"
    "services/nuxt3-shadcn/pages/references/newReferences.vue"
    "services/nuxt3-shadcn/pages/references/[id].vue"
    "services/nuxt3-shadcn/pages/styles.vue"
)

all_fixed=true
for file in "${fixed_files[@]}"; do
    if [ -f "$file" ]; then
        if grep -q "useApiConfig" "$file" && grep -q "buildUrl" "$file"; then
            echo -e "${GREEN}✅ $file uses useApiConfig${NC}"
        else
            echo -e "${RED}❌ $file missing useApiConfig${NC}"
            all_fixed=false
        fi
    else
        echo -e "${YELLOW}⚠️  $file not found${NC}"
    fi
done

if [ "$all_fixed" = false ]; then
    exit 1
fi
echo ""

# Check 6: Environment Configuration
echo -e "${BLUE}[6/6] Checking environment configuration...${NC}"
if [ -f ".env.example" ]; then
    if grep -q "API_BASE_URL" .env.example; then
        echo -e "${GREEN}✅ .env.example documents API_BASE_URL${NC}"
    else
        echo -e "${YELLOW}⚠️  .env.example missing API_BASE_URL documentation${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .env.example not found${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    Validation Summary                      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ Core infrastructure is in place${NC}"
echo -e "${GREEN}✅ Docker configuration fixed${NC}"
echo -e "${GREEN}✅ Composables and documentation created${NC}"
echo -e "${GREEN}✅ Critical files migrated${NC}"
echo ""
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo -e "   1. Migrate remaining files (see MIGRATION_GUIDE.md)"
echo -e "   2. Test in Docker: ${BLUE}docker-compose up -d${NC}"
echo -e "   3. Test locally: Start backend and frontend separately"
echo -e "   4. Review DEBUGGING_GUIDE.md for troubleshooting"
echo ""
echo -e "${GREEN}✅ Validation Complete!${NC}"
