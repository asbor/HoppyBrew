#!/bin/bash

# HoppyBrew - GitHub Issues Creation Script
# This script creates all planned issues on GitHub using GitHub CLI (gh)
# 
# Prerequisites:
# 1. Install GitHub CLI: https://cli.github.com/
# 2. Authenticate: gh auth login
# 3. Make this script executable: chmod +x create_github_issues.sh
#
# Usage:
#   ./create_github_issues.sh [dry-run|create-p0|create-p1|create-p2|create-p3|create-all]
#
#   dry-run     - Show what would be created without creating anything
#   create-p0   - Create only P0 (Critical) issues
#   create-p1   - Create only P1 (High Priority) issues
#   create-p2   - Create only P2 (Medium Priority) issues
#   create-p3   - Create only P3 (Low Priority) issues
#   create-all  - Create all issues (use with caution!)

set -e

REPO="asbor/HoppyBrew"
MODE="${1:-dry-run}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to create an issue
create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    local assignees="$4"
    
    if [ "$MODE" = "dry-run" ]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would create: ${GREEN}${title}${NC}"
        echo -e "  Labels: ${YELLOW}${labels}${NC}"
        return 0
    fi
    
    echo -e "${GREEN}Creating:${NC} ${title}"
    gh issue create \
        --repo "$REPO" \
        --title "$title" \
        --body "$body" \
        --label "$labels" \
        ${assignees:+--assignee "$assignees"}
    
    sleep 1  # Rate limiting
}

# Function to create issue with full details
create_full_issue() {
    local number="$1"
    local title="$2"
    local priority="$3"
    local component="$4"
    local estimate="$5"
    local description="$6"
    local dependencies="$7"
    local blocks="$8"
    
    local labels="$priority,$component"
    
    # Build issue body
    local body="## Description
${description}

## Details
- **Priority**: ${priority}
- **Component**: ${component}
- **Estimate**: ${estimate}
- **Dependencies**: ${dependencies:-None}
- **Blocks**: ${blocks:-None}

## Reference
See comprehensive analysis: [GITHUB_ISSUES_COMPREHENSIVE.md](https://github.com/${REPO}/blob/main/documents/issues/GITHUB_ISSUES_COMPREHENSIVE.md#issue-${number})

---

Generated from comprehensive brewing tracker analysis."
    
    create_issue "ISSUE #${number}: ${title}" "$body" "$labels"
}

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}   HoppyBrew - GitHub Issues Creation Script           ${BLUE}║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Mode: ${YELLOW}${MODE}${NC}"
echo -e "Repository: ${GREEN}${REPO}${NC}"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed.${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub CLI.${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# P0 - Critical Issues
if [ "$MODE" = "create-p0" ] || [ "$MODE" = "create-all" ]; then
    echo -e "\n${RED}═══ Creating P0 (Critical) Issues ═══${NC}\n"
    
    create_full_issue "1" \
        "Batch Status Workflow System" \
        "P0-Critical" \
        "backend,frontend" \
        "5 days" \
        "Implement a complete batch status workflow system to track the brewing lifecycle from planning to completion. Add status enum field to batches table with states: planning, brewing, fermenting, conditioning, packaging, complete, archived. Create state machine logic with valid state transitions." \
        "None" \
        "#2, #3, #6"
    
    create_full_issue "2" \
        "Fermentation Tracking System" \
        "P0-Critical" \
        "backend,frontend,database" \
        "8 days" \
        "Implement comprehensive fermentation tracking to monitor gravity, temperature, and fermentation progress. Create fermentation_readings table, add CRUD endpoints, build chart visualization, and automatic ABV calculation." \
        "#1" \
        "#6, #18"
    
    create_full_issue "3" \
        "Inventory Integration with Batches" \
        "P0-Critical" \
        "backend,frontend" \
        "5 days" \
        "Integrate inventory system with batch creation to prevent brewing without ingredients and track usage. Add availability checking, inventory allocation, and automatic deduction on batch status change." \
        "None" \
        "#4, #7"
    
    create_full_issue "4" \
        "Interactive Recipe Editor" \
        "P0-Critical" \
        "frontend" \
        "7 days" \
        "Build comprehensive, user-friendly recipe creation and editing interface with live calculations. Multi-step wizard, drag-and-drop, ingredient autocomplete, real-time calculation updates, validation, and BeerXML export." \
        "#3" \
        "None"
    
    create_full_issue "5" \
        "Brewing Calculators Suite" \
        "P0-Critical" \
        "backend,frontend" \
        "6 days" \
        "Implement comprehensive brewing calculator tools as both standalone pages and integrated components. Add 10+ calculation functions (priming sugar, yeast pitch rate, strike water, refractometer, etc.) with API endpoints and UI components." \
        "None" \
        "#4"
fi

# P1 - High Priority Issues
if [ "$MODE" = "create-p1" ] || [ "$MODE" = "create-all" ]; then
    echo -e "\n${YELLOW}═══ Creating P1 (High Priority) Issues ═══${NC}\n"
    
    create_full_issue "6" \
        "Brew Day Tracking System" \
        "P1-High" \
        "backend,frontend" \
        "6 days" \
        "Create step-by-step brew day tracking system with timers, checklists, and real-time data entry. Includes mash tracking, boil timer, hop addition alerts, cooling phase, and OG measurement." \
        "#1" \
        "None"
    
    create_full_issue "7" \
        "Complete Inventory Management UI" \
        "P1-High" \
        "frontend" \
        "5 days" \
        "Build full CRUD interfaces for all inventory types (fermentables, hops, yeasts, miscs). List view with search/filter/sort, create/edit modals, bulk import, low stock warnings, and expiration tracking." \
        "#3" \
        "None"
    
    create_full_issue "8" \
        "Packaging Management System" \
        "P1-High" \
        "backend,frontend" \
        "4 days" \
        "Implement packaging workflow for bottling and kegging, including carbonation tracking. Packaging wizard, priming sugar calculation, conditioning timeline, and ready date estimation." \
        "#5" \
        "None"
    
    create_full_issue "9" \
        "Quality Control & Tasting Notes" \
        "P1-High" \
        "backend,frontend,database" \
        "5 days" \
        "Implement comprehensive quality control system with tasting notes, ratings, and sensory evaluation. BJCP-style scorecard, photo upload, defect identification, and batch rating visualization." \
        "#1" \
        "None"
    
    create_full_issue "10" \
        "Analytics Dashboard" \
        "P1-High" \
        "backend,frontend" \
        "6 days" \
        "Create comprehensive analytics dashboard with batch metrics, trends, and insights. Total batches, success rate, efficiency trends, cost analysis, brewing frequency, and interactive visualizations." \
        "#9" \
        "None"
    
    # Additional P1 issues (11-15) - Infrastructure & Technical Debt
    create_full_issue "35" \
        "Pydantic v2 Migration" \
        "P1-High" \
        "backend,bugfix" \
        "3 days" \
        "Complete migration to Pydantic v2 to fix 20 failing tests. Update all schema files to use ConfigDict, replace .dict() with .model_dump(), fix circular imports, and ensure 38/38 tests passing." \
        "None" \
        "Multiple issues"
    
    create_full_issue "36" \
        "State Management Implementation" \
        "P1-High" \
        "frontend,infrastructure" \
        "4 days" \
        "Implement centralized state management with Pinia. Create stores for user, recipes, batches, inventory, and UI state. Replace direct API calls with actions." \
        "None" \
        "All frontend issues"
    
    create_full_issue "37" \
        "Form Validation Library" \
        "P1-High" \
        "frontend,infrastructure" \
        "2 days" \
        "Implement consistent form validation across all forms. Install Vuelidate/VeeValidate, create validation rules library, standardize error messages, and add real-time validation." \
        "None" \
        "All form-based issues"
    
    create_full_issue "38" \
        "Error Handling Patterns" \
        "P1-High" \
        "frontend,infrastructure" \
        "3 days" \
        "Standardize error handling and user feedback. Global error handler, API error interceptor, toast notifications, user-friendly messages, and retry mechanisms." \
        "None" \
        "None"
    
    create_full_issue "42" \
        "API Documentation" \
        "P1-High" \
        "documentation" \
        "3 days" \
        "Complete and enhance API documentation. Finish README_API.md, add Swagger annotations, example requests/responses, authentication docs, and error code reference." \
        "All API endpoints" \
        "None"
    
    create_full_issue "45" \
        "Frontend Test Suite" \
        "P1-High" \
        "frontend,testing" \
        "8 days" \
        "Implement comprehensive frontend testing. Component unit tests, integration tests, E2E tests with Playwright, visual regression, accessibility tests, and test coverage >70%." \
        "All frontend features" \
        "None"
    
    create_full_issue "46" \
        "Backend Test Coverage" \
        "P1-High" \
        "backend,testing" \
        "5 days" \
        "Increase backend test coverage to 80%+. Add missing endpoint tests, business logic tests, database model tests, edge cases, and integration tests." \
        "#35" \
        "None"
    
    create_full_issue "48" \
        "CI/CD Pipeline Enhancement" \
        "P1-High" \
        "devops" \
        "4 days" \
        "Enhance CI/CD pipeline for automated testing and deployment. Automated testing on PR, code quality checks, security scanning, deployment to staging, and rollback capability." \
        "#45, #46" \
        "None"
    
    create_full_issue "49" \
        "Production Deployment Setup" \
        "P1-High" \
        "devops" \
        "5 days" \
        "Setup production-ready deployment infrastructure. Docker compose for production, reverse proxy, SSL/TLS, environment management, migration strategy, and monitoring." \
        "#30, #31, #32, #34" \
        "Production launch"
fi

# P2 - Medium Priority Issues
if [ "$MODE" = "create-p2" ] || [ "$MODE" = "create-all" ]; then
    echo -e "\n${GREEN}═══ Creating P2 (Medium Priority) Issues ═══${NC}\n"
    
    create_full_issue "11" \
        "Water Chemistry Management" \
        "P2-Medium" \
        "backend,frontend" \
        "5 days" \
        "Implement water profile management and chemistry calculations for advanced brewers. Water profile editor, chemistry calculator, salt additions, pH adjustment, and profile comparisons." \
        "None" \
        "None"
    
    create_full_issue "12" \
        "Equipment Profile Management" \
        "P2-Medium" \
        "frontend" \
        "3 days" \
        "Build UI for equipment profile creation and management. Equipment CRUD interface, equipment-specific calculations, selection in recipe/batch, and efficiency tracking." \
        "None" \
        "None"
    
    create_full_issue "13" \
        "Fermentation Profile Templates" \
        "P2-Medium" \
        "backend,frontend,database" \
        "4 days" \
        "Create reusable fermentation profile templates for common schedules. CRUD for profiles, application to batches, pre-loaded common profiles (ale, lager, saison)." \
        "#2" \
        "None"
    
    # Add more P2 issues as needed (14-20, 33-34, 39-44, 47, 50)
    echo -e "${YELLOW}Note: Additional P2 issues (#14-20, #33-34, #39-44, #47, #50) can be created individually as needed.${NC}"
fi

# P3 - Low Priority Issues
if [ "$MODE" = "create-p3" ] || [ "$MODE" = "create-all" ]; then
    echo -e "\n${BLUE}═══ Creating P3 (Low Priority) Issues ═══${NC}\n"
    
    create_full_issue "21" \
        "Mobile Responsiveness" \
        "P3-Low" \
        "frontend,ui-ux" \
        "8 days" \
        "Complete mobile optimization for all features, critical for brew day use. Mobile-first responsive design, touch-optimized controls, PWA functionality, and offline support." \
        "All frontend issues" \
        "None"
    
    create_full_issue "22" \
        "Notification System" \
        "P3-Low" \
        "backend,frontend" \
        "5 days" \
        "Implement notification system for reminders and alerts. Email notifications, in-app notifications, preferences, and various reminder types (fermentation, dry hop, packaging, etc.)." \
        "None" \
        "None"
    
    create_full_issue "23" \
        "User Authentication & Authorization" \
        "P3-Low" \
        "backend,frontend,security" \
        "6 days" \
        "Implement secure user authentication and authorization system. User registration, login, password reset, profile management, RBAC, JWT tokens, and OAuth integration." \
        "None" \
        "#14"
    
    # Add more P3 issues as needed (24-30)
    echo -e "${BLUE}Note: Additional P3 issues (#24-30) can be created individually as needed.${NC}"
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Issue creation process complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""

if [ "$MODE" = "dry-run" ]; then
    echo -e "${YELLOW}This was a dry run. No issues were created.${NC}"
    echo -e "To create issues, run with: ${GREEN}create-p0${NC}, ${GREEN}create-p1${NC}, ${GREEN}create-p2${NC}, ${GREEN}create-p3${NC}, or ${GREEN}create-all${NC}"
fi

echo ""
echo -e "View all issues: ${BLUE}https://github.com/${REPO}/issues${NC}"
echo ""
