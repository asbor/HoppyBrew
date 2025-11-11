#!/bin/bash

# Script to find hardcoded API URLs in the frontend codebase
# This helps identify files that need to be refactored to use useApiConfig()

echo "🔍 Scanning for hardcoded API URLs in frontend code..."
echo ""

cd "$(dirname "$0")/.."

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Find files with hardcoded localhost:8000
echo -e "${BLUE}Files with hardcoded 'http://localhost:8000':${NC}"
echo ""

count=0
while IFS= read -r file; do
    if [[ "$file" == *"node_modules"* ]] || [[ "$file" == *".git"* ]]; then
        continue
    fi
    
    # Skip the composables that are supposed to have the fallback
    if [[ "$file" == *"composables/useApiUrl.ts"* ]] || \
       [[ "$file" == *"composables/useApi.ts"* ]] || \
       [[ "$file" == *"composables/useApiConfig.ts"* ]] || \
       [[ "$file" == *"nuxt.config.ts"* ]] || \
       [[ "$file" == *"test/"* ]] || \
       [[ "$file" == *"tests/"* ]]; then
        continue
    fi
    
    line_count=$(grep -c "http://localhost:8000" "$file" 2>/dev/null)
    if [ "$line_count" -gt 0 ]; then
        echo -e "${RED}❌ $file${NC} (${line_count} occurrence(s))"
        # Show the actual lines
        grep -n "http://localhost:8000" "$file" | head -5 | while IFS= read -r line; do
            echo -e "${YELLOW}   $line${NC}"
        done
        echo ""
        count=$((count + line_count))
    fi
done < <(find services/nuxt3-shadcn -type f \( -name "*.vue" -o -name "*.ts" -o -name "*.js" \) 2>/dev/null)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Summary:${NC}"
echo -e "Total hardcoded URLs found: ${RED}$count${NC}"
echo ""

if [ "$count" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Action Required:${NC}"
    echo "   Replace these hardcoded URLs with useApiConfig():"
    echo ""
    echo "   ❌ Bad:"
    echo "      const response = await fetch('http://localhost:8000/recipes')"
    echo ""
    echo "   ✅ Good:"
    echo "      const { buildUrl } = useApiConfig()"
    echo "      const response = await fetch(buildUrl('/recipes'))"
    echo ""
    echo "   See DEBUGGING_GUIDE.md for more information."
else
    echo -e "${GREEN}✅ No hardcoded URLs found! Good job!${NC}"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
