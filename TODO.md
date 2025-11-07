# HoppyBrew TODO

This document organizes work based on the **COMPREHENSIVE_WORKFLOW_ANALYSIS** and **IMPLEMENTATION_ROADMAP**. Tasks are grouped by priority and functional area for efficient parallel development.

**Last Updated**: November 7, 2025  
**Recent Progress**: Application stabilized, critical bug fixes completed, frontend pages rebuilt  
**Reference Documents**: 
- COMPREHENSIVE_WORKFLOW_ANALYSIS.md (300+ identified features)
- IMPLEMENTATION_ROADMAP.md (32-week sprint plan)
- SESSION_SUMMARY_2025-11-07.md (Latest session details)

---

## ✅ Completed Recently (November 5-7, 2025)

### Backend Fixes
- [x] Fixed MashStepBase schema export causing backend startup failure
- [x] Updated equipment and mash profile schemas and endpoints
- [x] PostgreSQL connection string verified working correctly
- [x] Session management with dependency injection verified
- [x] Batch relationships matching ORM models verified
- [x] Primary keys made non-nullable (StyleGuidelines, Styles)
- [x] Placeholder modules fixed (export/import_references)
- [x] Alembic migrations and seed scripts ready

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

### Database & Backend
- [ ] **Add comprehensive seed data** ⚠️ BLOCKING
  - [ ] 10+ sample recipes (IPA, Stout, Lager, Pale Ale, Porter, Wheat, etc.)
  - [ ] 50+ inventory items with quantities and costs (EUR)
  - [ ] Sample batches in different stages (all with proper status field)
  - [ ] Equipment profiles (Grainfather, Anvil, BIAB)
  - [ ] Water profiles (soft, hard, balanced)
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
- [-] Create Inventory Pages
  - ✅ inventory/hops - Complete with CRUD, search, low stock warnings, expiry tracking
  - ✅ inventory/fermentables - Complete with CRUD, search, color visualization, low stock warnings
  - ⏳ inventory/yeasts - TODO: Build with temperature ranges, attenuation, flocculation
  - ⏳ inventory/miscs - TODO: Build with usage tracking, water agents, spices

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
- [ ] Update README.md to remove any remaining template placeholders
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

1. **Resolve TODO.md merge conflict** (this file)
2. **Add comprehensive seed data** to enable proper testing
3. **Build Recipe Detail components** to eliminate console warnings
4. **Create Inventory CRUD pages** for ingredient management
5. **Build Profile management pages** for equipment/mash/water/fermentation

---

**Reference Documents**:
- SESSION_SUMMARY_2025-11-07.md - Latest bug fixes and stabilization
- COMPREHENSIVE_WORKFLOW_ANALYSIS.md - Full feature analysis (300+ features)
- IMPLEMENTATION_ROADMAP.md - 32-week sprint plan
- FRONTEND_ARCHITECTURE.md - Frontend composables and patterns
- FRONTEND_API_URL_MIGRATION.md - API centralization guide

**Last Updated**: November 7, 2025  
**Next Review**: After seed data completion
