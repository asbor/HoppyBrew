# HoppyBrew TODO

This document organizes work based on the **COMPREHENSIVE_WORKFLOW_ANALYSIS** and **IMPLEMENTATION_ROADMAP**. Tasks are grouped by priority and functional area for efficient parallel development.

**Last Updated**: November 7, 2025 (Evening)  
**Recent Progress**: Schema drift resolved, 23 issues closed, critical blockers tracked  
**Reference Documents**: 
- COMPREHENSIVE_WORKFLOW_ANALYSIS.md (300+ identified features)
- IMPLEMENTATION_ROADMAP.md (32-week sprint plan)
- SCHEMA_DRIFT_RESOLUTION.md (Migration fixes)
- Issue #226 (Critical Production Blockers tracking)

---

## ✅ Completed Recently (November 7, 2025 Evening)

### Schema & Migrations (PR #227)
- [x] **Resolved schema drift** - Fixed duplicate revision ID conflicts
- [x] **Migration chain linearized** - 0001 → 0002 (beer styles) → 0003 (water profiles)
- [x] **Made migrations idempotent** - Table/column existence checks added
- [x] **Created SCHEMA_DRIFT_RESOLUTION.md** - Complete documentation of fix

### API Documentation
- [x] **Created api_endpoint_catalog.md** - Comprehensive endpoint documentation
- [x] **Created endpoint_inventory.tsv** - Machine-readable endpoint list
- [x] All endpoints documented with methods, paths, handlers, responses

### GitHub Issue Management (23 Issues Closed)
- [x] **Closed 22 duplicate security alerts** (#195-225)
- [x] **Closed #87: BJCP Style Guidelines** - Feature fully implemented
- [x] **Updated #226** - Critical blockers tracking (5/11 fixed)
- [x] **Updated #123** - Database performance with 11 missing FK indexes
- [x] **Updated #152** - Equipment profiles status
- [x] **Updated #153** - Mash profiles backend complete

### Features Confirmed Implemented
- [x] **Beer Style Management** - Complete BJCP style guidelines system
- [x] **Mash Profile System** - Profiles + multi-step scheduling API
- [x] **Equipment Profiles** - Basic CRUD operations

---

## ✅ Completed Previously (November 5-7, 2025)

### Backend Fixes
- [x] Fixed MashStepBase schema export causing backend startup failure
- [x] Updated equipment and mash profile schemas and endpoints
- [x] PostgreSQL connection string verified working correctly
- [x] Session management with dependency injection verified
- [x] Batch relationships matching ORM models verified
- [x] Primary keys made non-nullable (StyleGuidelines, Styles)
- [x] Placeholder modules fixed (export/import_references)
- [x] Alembic migrations and seed scripts ready
- [x] **Added batches.status column** - Fixed 500 error on /batches endpoint
- [x] **Created comprehensive seed data** - 10 recipes, 4 batches, 32 inventory items

### Frontend Improvements
- [x] Fixed null pointer crashes in Dashboard and Batches pages (batch.status handling)
- [x] Rebuilt Dashboard with brewing metrics, recent activity, quick actions
- [x] Rebuilt Recipe List (8 focused columns, search, error handling)
- [x] Rebuilt Batch List (9 columns, status badges, filters)
- [x] Created Tools page with 7 brewing calculators
- [x] Centralized API URLs using runtime config
- [x] Created typed API client with useApi composable
- [x] Added Home Assistant dark theme (#111111 bg, #03A9F4 primary)
- [x] Added checkbox component for future use

### DevOps & Documentation
- [x] Docker Compose health checks verified
- [x] .env.example created
- [x] Deployment guide documented
- [x] Session summary documentation created

---

## 🔴 HIGH PRIORITY - Current Sprint

### 🚨 Critical Production Blockers (Issue #226) - 9 Remaining

**Week 1 Focus:**
- [ ] **Testing Infrastructure** - Fix SQLite permissions for test suite
- [ ] **Missing FK Indexes** - Add 11 indexes from #123 analysis (HIGH IMPACT)
  ```sql
  -- Inventory tables (batch_id, recipe_id) - 8 indexes
  -- Profile relationships - 3 indexes
  -- See Issue #123 for complete SQL
  ```
- [ ] **Question/Choice Cascade** - Fix FK constraint violations
- [ ] **Frontend Dialog Component** - Resolve Dialog errors

**Week 2 Focus:**
- [ ] **Authentication Layer** - Add user authentication system
- [ ] **Secrets Management** - Move secrets from docker-compose to env/vault
- [ ] **Docker Optimization** - Multi-stage build, non-root user
- [ ] **Device API Tokens** - Encrypt/hash plaintext tokens
- [ ] **Water Profile Schema** - Verify migration 0003 correctness

**Progress**: 5/11 fixed (45%) | **Estimated Time**: 2-3 weeks

---

## 🔴 HIGH PRIORITY - Feature Development

### Database & Backend
- [x] **Add comprehensive seed data** ✅ COMPLETED
  - [x] 10 diverse sample recipes (American IPA, Irish Stout, German Pilsner, Hefeweizen, English Bitter, Belgian Dubbel, American Pale Ale, Porter, Kolsch, West Coast IPA)
  - [x] 27+ recipe ingredients (fermentables, hops, yeasts, miscs)
  - [x] 4 sample batches in different stages (planning, primary_fermentation, conditioning)
  - [x] 3 equipment profiles (Grainfather G30, Anvil Foundry, BIAB)
  - [x] 4 water profiles (soft, balanced, hoppy IPA, malty stout)
  - [x] All batches with proper inventory allocation
- [ ] Introduce service/repository layer to reduce CRUD duplication
- [ ] Extend Makefile for linting, tests, formatters

### Frontend - Recipe Detail Page
- [ ] Build recipes/[id].vue with complete recipe display
- [ ] Create RecipeBlock component (overview)
- [ ] Create EquipmentBlock component
- [ ] Create StyleBlock component
- [ ] Create FermentablesBlock component
- [ ] Create HopsBlock component
- [ ] Create MiscsBlock component
- [ ] Create YeastBlock component
- [ ] Create MashBlock component
- [ ] Create FermentationBlock component
- [ ] Create WaterBlock component
- [ ] Create NotesBlock component
- [ ] Add edit mode, clone recipe, start batch actions
- [ ] Add inventory availability check

### Frontend - Inventory Pages
- [x] Create Inventory Pages
  - ✅ inventory/hops - Complete with CRUD, search, filtering, low stock/expiry warnings
  - ✅ inventory/fermentables - Complete with color visualization, yield tracking
  - ✅ inventory/yeasts - Complete with temperature ranges, attenuation, flocculation
  - ✅ inventory/miscs - Complete with type/use tracking, flexible units

### Frontend - Profile Pages
- [ ] Create /profiles/equipment page (CRUD for equipment profiles)
- [ ] Create /profiles/mash page (CRUD for mash profiles)
- [ ] Create /profiles/water page (CRUD for water profiles)
- [ ] Create /profiles/fermentation page (CRUD for fermentation profiles)
- [ ] Add profile templates library

---

## 🟡 MEDIUM PRIORITY - Next Sprint

### Backend APIs
- [ ] Decide on Selenium-based scraper (keep, improve, or remove)
- [ ] Finalize beer style ingestion flow
- [ ] Document data ownership for reference material

### Frontend - Batch Detail & Workflow
- [ ] Build /batches/[id] detail page
- [ ] Create brew day workflow interface
- [ ] Add fermentation monitoring dashboard
- [ ] Implement batch status progression controls
- [ ] Add batch logs and notes interface
- [ ] Create printable brew sheet view

### Frontend - Polish
- [ ] Replace placeholder dashboard data with real endpoints
- [ ] Implement Pinia for shared state management
- [ ] Add pagination to large tables
- [ ] Add column selection to tables
- [ ] Improve mobile responsiveness
- [ ] Add validation feedback to all forms

### Integration - iSpindel
- [ ] Research iSpindel API and data format
- [ ] Build iSpindel integration endpoint
- [ ] Create fermentation monitoring dashboard with iSpindel data
- [ ] Add real-time gravity and temperature tracking
- [ ] Implement alerts for fermentation issues

---

## 🟢 LOW PRIORITY - Future Enhancements

### Frontend Enhancements
- [ ] Migrate remaining 20+ pages to use centralized API
- [ ] Build pages for style guidelines and references
- [ ] Add dark mode toggle (currently always dark)
- [ ] Add keyboard shortcuts for power users
- [ ] Add contextual help tooltips

### Data & Integrations
- [ ] Complete BeerXML import/export functionality
- [ ] Add recipe PDF export
- [ ] Add recipe versioning
- [ ] Add recipe comparison view
- [ ] Build recipe templates library

### Testing
- [ ] Add unit/integration tests for recipes
- [ ] Add tests for references import/export
- [ ] Add tests for beer style ingestion
- [ ] Introduce frontend unit tests (Vitest) for critical components
- [ ] Add E2E tests for core workflows

### Documentation
- [x] Update README.md to remove any remaining template placeholders - COMPLETED
- [ ] Refresh setup instructions for various platforms
- [ ] Create user manual with screenshots
- [ ] Create video tutorials for key workflows
- [ ] Update API documentation (Swagger/ReDoc)
- [ ] Create troubleshooting guide

---

## 🎯 Known Issues & Technical Debt

### Frontend Console Warnings (Non-Critical)
**Status**: Expected and non-blocking  
Console shows warnings for missing components on recipe detail page:
- RecipeBlock, EquipmentBlock, StyleBlock
- FermentablesBlock, HopsBlock, MiscsBlock, YeastBlock
- MashBlock, FermentationBlock, WaterBlock, NotesBlock

These are on the todo list above and don't affect functionality.

### Technical Debt
- [ ] Pydantic v2 migration (20 failing tests - needs attention)
- [ ] Standardize error handling patterns across backend
- [ ] Add structured logging throughout application
- [ ] Set up application performance monitoring
- [ ] Configure dependency vulnerability scanning
- [ ] Set up automated database backups
- [ ] Add database migration version control workflow

---

## 📊 Progress Tracking

### Application Status
- **Backend**: ✅ Stable, health checks passing
- **Frontend**: ✅ Stable, core pages rebuilt
- **Database**: ✅ Healthy, schemas complete
- **Docker**: ✅ All containers healthy

### Feature Completion Estimate
- Equipment Management: 15% → Target: 100%
- Inventory Management: 20% → Target: 100%
- Recipe Design: 35% → Target: 100%
- Batch Management: 30% → Target: 100%
- Brew Day Tracking: 0% → Target: 100%
- Fermentation Monitoring: 5% → Target: 100%
- Packaging: 0% → Target: 100%
- Quality Control: 0% → Target: 100%
- Analytics: 10% → Target: 80%
- Home Assistant Integration: 30% → Target: 90%

**Current Overall Progress**: ~25%  
**Target for MVP**: ~60%  
**Target for Production**: ~85%

---

## 🚀 Immediate Next Actions

1. ~~**Resolve TODO.md merge conflict**~~ ✅ COMPLETED
2. ~~**Add comprehensive seed data**~~ ✅ COMPLETED
3. **Test inventory pages** with real seed data (hops, fermentables, yeasts, miscs)
4. **Build Recipe Detail components** to eliminate console warnings
5. **Create Profile management pages** for equipment/mash/water/fermentation

---

**Reference Documents**:
- SESSION_SUMMARY_2025-11-07.md - Latest bug fixes and stabilization
- COMPREHENSIVE_WORKFLOW_ANALYSIS.md - Full feature analysis (300+ features)
- IMPLEMENTATION_ROADMAP.md - 32-week sprint plan
- FRONTEND_ARCHITECTURE.md - Frontend composables and patterns
- FRONTEND_API_URL_MIGRATION.md - API centralization guide

**Last Updated**: November 7, 2025  
**Next Review**: After seed data completion
