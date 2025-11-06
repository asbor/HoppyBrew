# HoppyBrew Implementation Roadmap

**Generated**: November 5, 2025  
**Based On**: COMPREHENSIVE_WORKFLOW_ANALYSIS.md  
**Objective**: Transform HoppyBrew into a production-ready brewing management platform

---

## 📊 Current State Summary

**Overall Completeness**: ~15-20% of target features
- Backend API: 40% complete (30+ endpoints exist, many missing)
- Frontend UI: 20% complete (pages exist but mostly empty templates)
- Business Logic: 25% complete (basic calculations only)
- Integration: 15% complete (basic HA, no MQTT, no devices)

---

## 🎯 SPRINT PLANNING (Agile 2-Week Sprints)

### MILESTONE 1: Foundation & Core Inventory (Weeks 1-6)

#### Sprint 1-2: Equipment & Inventory Infrastructure (Weeks 1-4)
**Goal**: Enable brewers to configure equipment and manage ingredient inventory

**Backend Tasks**:
- [ ] Add missing fields to inventory tables (cost, expiration, min_stock, supplier)
- [ ] Create equipment_templates table for pre-defined systems
- [ ] Add inventory_transactions table for tracking purchases/usage
- [ ] Create suppliers table
- [ ] Add API endpoints:
  - [ ] GET/POST `/api/equipment-profiles/templates`
  - [ ] GET `/api/inventory/low-stock`
  - [ ] GET `/api/inventory/expiring`
  - [ ] POST `/api/inventory/check-availability`
  - [ ] GET/POST `/api/suppliers`
- [ ] Add validation for equipment profiles
- [ ] Add inventory cost calculation functions

**Frontend Tasks**:
- [ ] Create Equipment Profile Creation Form:
  - [ ] Basic info (name, type, batch size)
  - [ ] Vessel volumes (mash tun, boil kettle, fermenter)
  - [ ] Loss factors (trub, dead space, boil-off)
  - [ ] Efficiency settings
- [ ] Create Equipment Profile Selector with cards
- [ ] Create Equipment Templates library
- [ ] Enhance Inventory Dashboard:
  - [ ] Complete CRUD forms for fermentables
  - [ ] Complete CRUD forms for hops
  - [ ] Complete CRUD forms for yeasts
  - [ ] Complete CRUD forms for miscs
  - [ ] Add cost tracking fields
  - [ ] Add expiration date fields
  - [ ] Add supplier selection
  - [ ] Add min stock level settings
- [ ] Create Low Stock Alert component
- [ ] Create Expiring Ingredients Alert component
- [ ] Add inventory search and filtering
- [ ] Create Supplier Management page

**Testing**:
- [ ] Unit tests for equipment validation
- [ ] Unit tests for inventory calculations
- [ ] Integration tests for inventory CRUD
- [ ] E2E test: Create equipment profile
- [ ] E2E test: Add ingredients with costs

**Deliverables**:
- ✅ Equipment profiles fully functional
- ✅ Complete inventory management UI
- ✅ Low stock and expiration alerts working
- ✅ Supplier tracking enabled

---

#### Sprint 3: Recipe Editor Foundation (Weeks 5-6)
**Goal**: Enable creating complete recipes with live calculations

**Backend Tasks**:
- [ ] Add recipe validation endpoint
- [ ] Add recipe scaling endpoint UI integration
- [ ] Enhance recipe endpoints to include all relationships
- [ ] Add style guidelines comparison function
- [ ] Create recipe availability check endpoint

**Frontend Tasks**:
- [ ] Create Interactive Recipe Editor:
  - [ ] Basic info form (name, style, batch size, type)
  - [ ] Equipment profile selector
  - [ ] Fermentables section:
    - [ ] Ingredient picker from inventory
    - [ ] Amount input with units
    - [ ] Usage dropdown (Mash/Boil/Fermentation)
    - [ ] Percentage of grain bill display
  - [ ] Hops section:
    - [ ] Hop variety picker from inventory
    - [ ] Amount input
    - [ ] Use dropdown (First Wort/Boil/Whirlpool/Dry Hop)
    - [ ] Time input
  - [ ] Yeast section:
    - [ ] Yeast strain picker from inventory
    - [ ] Amount/packages input
    - [ ] Temperature range
  - [ ] Miscs section
- [ ] Integrate RecipeCalculatorWidget (already exists)
- [ ] Add live calculation updates
- [ ] Add style guidelines panel
- [ ] Add recipe validation warnings
- [ ] Add ingredient availability checker
- [ ] Create recipe scaling calculator
- [ ] Add recipe save/update/delete actions

**Testing**:
- [ ] Unit tests for recipe calculations
- [ ] Integration tests for recipe CRUD
- [ ] E2E test: Create complete recipe
- [ ] E2E test: Scale recipe
- [ ] Test live calculations update

**Deliverables**:
- ✅ Full-featured recipe editor
- ✅ Live calculations working
- ✅ Style guidelines comparison
- ✅ Recipe validation

---

### MILESTONE 2: Batch Tracking & Fermentation (Weeks 7-12)

#### Sprint 4-5: Batch Management & Brew Day Prep (Weeks 7-10)
**Goal**: Enable batch creation and brew day preparation

**Backend Tasks**:
- [ ] Add batch status enum to batches table
- [ ] Create batch state transition validation
- [ ] Add batch_state_history table
- [ ] Add inventory allocation system
- [ ] Create brew day sheet generator endpoint
- [ ] Add endpoints:
  - [ ] PUT `/api/batches/{id}/status`
  - [ ] POST `/api/batches/{id}/allocate-inventory`
  - [ ] GET `/api/batches/{id}/brew-sheet`
  - [ ] GET `/api/batches/{id}/timeline`

**Frontend Tasks**:
- [ ] Create Batch Creation Wizard:
  - [ ] Step 1: Select recipe
  - [ ] Step 2: Set brew date
  - [ ] Step 3: Check ingredient availability
  - [ ] Step 4: Select equipment profile
  - [ ] Step 5: Review and create
- [ ] Integrate BatchStatusTimeline component (already exists)
- [ ] Create Batch Dashboard with status cards
- [ ] Create Printable Brew Day Sheet
- [ ] Create Brew Day Checklist
- [ ] Add Batch Detail page enhancements
- [ ] Create batch list with filtering
- [ ] Add batch status badges

**Testing**:
- [ ] Unit tests for batch state machine
- [ ] Integration tests for batch creation
- [ ] E2E test: Create batch from recipe
- [ ] E2E test: Allocate inventory
- [ ] Test printable brew sheet

**Deliverables**:
- ✅ Batch creation wizard functional
- ✅ Inventory allocation working
- ✅ Batch status tracking enabled
- ✅ Brew day sheet printable

---

#### Sprint 6: Fermentation Tracking (Weeks 11-12)
**Goal**: Enable fermentation monitoring and logging

**Backend Tasks**:
- [ ] Create fermentation_readings table
- [ ] Add fermentation reading endpoints:
  - [ ] POST `/api/batches/{id}/fermentation/readings`
  - [ ] GET `/api/batches/{id}/fermentation/readings`
  - [ ] PUT `/api/batches/{id}/fermentation/readings/{reading_id}`
  - [ ] DELETE `/api/batches/{id}/fermentation/readings/{reading_id}`
- [ ] Add fermentation chart data endpoint
- [ ] Add fermentation completion detection logic
- [ ] Add attenuation calculation

**Frontend Tasks**:
- [ ] Create Fermentation Log Entry Form:
  - [ ] Date/time picker
  - [ ] Gravity input (with unit selection SG/Plato)
  - [ ] Temperature input
  - [ ] pH input (optional)
  - [ ] Notes textarea
  - [ ] Photo upload
- [ ] Create Fermentation Charts:
  - [ ] Gravity over time line chart
  - [ ] Temperature over time line chart
  - [ ] Combined gravity/temp chart
- [ ] Create Fermentation Progress Widget:
  - [ ] Current attenuation %
  - [ ] Expected vs actual FG
  - [ ] Days in fermentation
  - [ ] Fermentation stage (Active/Slowing/Complete)
- [ ] Add fermentation timeline to batch detail
- [ ] Create fermentation completion indicator

**Testing**:
- [ ] Unit tests for attenuation calculation
- [ ] Integration tests for fermentation readings
- [ ] E2E test: Log fermentation readings
- [ ] E2E test: View fermentation charts
- [ ] Test chart rendering with various data

**Deliverables**:
- ✅ Fermentation logging functional
- ✅ Gravity and temperature charts working
- ✅ Progress tracking enabled
- ✅ Completion detection working

---

### MILESTONE 3: Brew Day & Packaging (Weeks 13-18)

#### Sprint 7-8: Brew Day Tracking (Weeks 13-16)
**Goal**: Enable step-by-step brew day execution tracking

**Backend Tasks**:
- [ ] Create brew_day_sessions table
- [ ] Create brew_day_steps table
- [ ] Add brew day actual readings fields to batches
- [ ] Add endpoints:
  - [ ] POST `/api/batches/{id}/brew-day/start`
  - [ ] POST `/api/batches/{id}/brew-day/step`
  - [ ] PUT `/api/batches/{id}/brew-day/step/{step_id}`
  - [ ] POST `/api/batches/{id}/brew-day/complete`
- [ ] Add deviation tracking
- [ ] Add efficiency calculation from actuals

**Frontend Tasks**:
- [ ] Create Brew Day Workflow UI:
  - [ ] Pre-brew checklist
  - [ ] Mashing phase tracking
  - [ ] Boil phase tracking
  - [ ] Hop addition timer and alerts
  - [ ] Cooling phase tracking
  - [ ] Yeast pitching logging
- [ ] Create Brew Day Timer Component
- [ ] Create Actual Readings Forms:
  - [ ] Strike water temperature
  - [ ] Mash temperature
  - [ ] Mash pH
  - [ ] Pre-boil gravity
  - [ ] Pre-boil volume
  - [ ] Original Gravity
  - [ ] Post-boil volume
  - [ ] Fermenter volume
  - [ ] Pitching temperature
- [ ] Create Deviation Tracker
- [ ] Add brew day progress indicator
- [ ] Create mobile-optimized brew day view

**Testing**:
- [ ] Unit tests for efficiency calculation
- [ ] Integration tests for brew day workflow
- [ ] E2E test: Complete brew day workflow
- [ ] Test timer functionality
- [ ] Test mobile responsiveness

**Deliverables**:
- ✅ Brew day workflow functional
- ✅ Timers and alerts working
- ✅ Actual readings logged
- ✅ Efficiency calculated from actuals

---

#### Sprint 9: Packaging (Weeks 17-18)
**Goal**: Enable packaging and carbonation tracking

**Backend Tasks**:
- [ ] Create packaging_details table
- [ ] Add carbonation calculations
- [ ] Add endpoints:
  - [ ] POST `/api/batches/{id}/packaging`
  - [ ] PUT `/api/batches/{id}/packaging`
  - [ ] POST `/api/tools/calculate/priming-sugar`
  - [ ] POST `/api/tools/calculate/carbonation-psi`

**Frontend Tasks**:
- [ ] Create Packaging Form:
  - [ ] Packaging date
  - [ ] Packaging method (Bottle/Keg/Can)
  - [ ] Carbonation method (Natural/Forced/Cask)
  - [ ] Final gravity
  - [ ] Volume packaged
  - [ ] Priming sugar calculation (integrated)
  - [ ] Force carbonation PSI calculator
  - [ ] Bottle/keg count
  - [ ] Conditioning schedule
- [ ] Integrate priming sugar calculator (exists in useCalculators)
- [ ] Create force carbonation PSI calculator
- [ ] Add packaging completion action
- [ ] Add ready date tracking

**Testing**:
- [ ] Unit tests for carbonation calculations
- [ ] Integration tests for packaging
- [ ] E2E test: Package batch
- [ ] Test priming calculations

**Deliverables**:
- ✅ Packaging tracking functional
- ✅ Carbonation calculators working
- ✅ Bottle/keg inventory tracking

---

### MILESTONE 4: Quality Control & Analytics (Weeks 19-24)

#### Sprint 10: Quality Control & Tasting (Weeks 19-20)
**Goal**: Enable quality assessment and tasting notes

**Backend Tasks**:
- [ ] Create tastings table
- [ ] Add tasting endpoints:
  - [ ] POST `/api/batches/{id}/tastings`
  - [ ] GET `/api/batches/{id}/tastings`
  - [ ] PUT `/api/batches/{id}/tastings/{tasting_id}`
  - [ ] DELETE `/api/batches/{id}/tastings/{tasting_id}`
- [ ] Add photo upload support
- [ ] Add style comparison scoring

**Frontend Tasks**:
- [ ] Create Tasting Notes Form:
  - [ ] Tasting date
  - [ ] Overall rating (1-5 stars)
  - [ ] Category ratings (Appearance, Aroma, Flavor, Mouthfeel)
  - [ ] Carbonation assessment
  - [ ] Clarity rating
  - [ ] Detailed notes textarea
  - [ ] Photo upload
- [ ] Create Tasting History Timeline
- [ ] Add style comparison scorecard
- [ ] Create rating display components
- [ ] Add multiple tastings per batch

**Testing**:
- [ ] Integration tests for tastings
- [ ] E2E test: Add tasting notes
- [ ] Test photo upload
- [ ] Test rating system

**Deliverables**:
- ✅ Tasting notes functional
- ✅ Rating system working
- ✅ Photo uploads enabled
- ✅ Tasting history tracked

---

#### Sprint 11-12: Analytics Dashboard (Weeks 21-24)
**Goal**: Enable brewing analytics and insights

**Backend Tasks**:
- [ ] Create analytics query functions
- [ ] Add analytics endpoints:
  - [ ] GET `/api/analytics/batches/summary`
  - [ ] GET `/api/analytics/efficiency`
  - [ ] GET `/api/analytics/costs`
  - [ ] GET `/api/analytics/inventory/usage`
  - [ ] GET `/api/analytics/recipes/popular`
  - [ ] GET `/api/analytics/calendar`
- [ ] Add batch comparison query
- [ ] Add trend calculation functions

**Frontend Tasks**:
- [ ] Create Analytics Dashboard:
  - [ ] Summary statistics cards
  - [ ] Efficiency trend chart
  - [ ] Cost per batch chart
  - [ ] Brewing frequency chart
  - [ ] Style distribution pie chart
  - [ ] Top recipes list
- [ ] Create Batch Comparison View
- [ ] Create Brewing Calendar
- [ ] Add date range filtering
- [ ] Create export to PDF/Excel
- [ ] Add ingredient usage report
- [ ] Create cost breakdown charts

**Testing**:
- [ ] Unit tests for analytics calculations
- [ ] Integration tests for analytics endpoints
- [ ] E2E test: View analytics dashboard
- [ ] Test chart rendering
- [ ] Test data export

**Deliverables**:
- ✅ Analytics dashboard functional
- ✅ Charts and graphs working
- ✅ Batch comparison enabled
- ✅ Reports exportable

---

### MILESTONE 5: Home Assistant Integration (Weeks 25-28)

#### Sprint 13-14: MQTT & Device Integration (Weeks 25-28)
**Goal**: Enable real-time Home Assistant integration and device support

**Backend Tasks**:
- [ ] Add MQTT client library (paho-mqtt)
- [ ] Create MQTT broker connection manager
- [ ] Implement MQTT discovery protocol
- [ ] Add MQTT publish functions for all sensors
- [ ] Create device integration framework
- [ ] Add iSpindel integration:
  - [ ] HTTP endpoint for iSpindel data
  - [ ] Parse iSpindel JSON payload
  - [ ] Store readings in fermentation_readings
  - [ ] Publish to MQTT
- [ ] Add Tilt integration (if possible via HTTP bridge)
- [ ] Add WebSocket support for real-time updates
- [ ] Create HA service call handlers

**Frontend Tasks**:
- [ ] Create Device Management page:
  - [ ] Add/edit/delete devices
  - [ ] Device status display
  - [ ] Device configuration
- [ ] Create Real-time Dashboard
- [ ] Add WebSocket connection for live updates
- [ ] Create device pairing wizard
- [ ] Add device status indicators

**Configuration Tasks**:
- [ ] Create MQTT broker configuration
- [ ] Document MQTT topic structure
- [ ] Create Home Assistant discovery payloads
- [ ] Create example HA configuration
- [ ] Document device setup procedures

**Testing**:
- [ ] Unit tests for MQTT functions
- [ ] Integration tests with MQTT broker
- [ ] E2E test: Device data flow
- [ ] Test HA discovery
- [ ] Test real-time updates

**Deliverables**:
- ✅ MQTT integration working
- ✅ iSpindel integration functional
- ✅ Real-time updates enabled
- ✅ HA discovery working

---

### MILESTONE 6: Advanced Features (Weeks 29-32)

#### Sprint 15: Water Chemistry & Advanced Calculators (Weeks 29-30)
**Goal**: Enable advanced brewing calculations

**Backend Tasks**:
- [ ] Add water chemistry calculation functions
- [ ] Add endpoints:
  - [ ] POST `/api/tools/calculate/strike-water`
  - [ ] POST `/api/tools/calculate/yeast-pitch`
  - [ ] POST `/api/tools/calculate/refractometer`
  - [ ] POST `/api/tools/calculate/dilution`
  - [ ] POST `/api/tools/calculate/water-chemistry`
  - [ ] POST `/api/tools/calculate/mash-ph`

**Frontend Tasks**:
- [ ] Create Tools page with calculator widgets
- [ ] Create Water Chemistry Calculator:
  - [ ] Source water profile input
  - [ ] Target water profile selection
  - [ ] Mineral additions calculator
  - [ ] pH prediction
- [ ] Create Advanced Calculator Tools:
  - [ ] Strike water temperature
  - [ ] Yeast pitch rate
  - [ ] Starter size
  - [ ] Refractometer correction
  - [ ] Dilution calculator
  - [ ] Alcohol correction for hydrometer
- [ ] Integrate all calculators from useCalculators composable

**Deliverables**:
- ✅ Water chemistry tools working
- ✅ All calculators accessible
- ✅ Tools page functional

---

#### Sprint 16: BeerXML & Polish (Weeks 31-32)
**Goal**: Enable recipe import/export and final polish

**Backend Tasks**:
- [ ] Complete BeerXML import parser
- [ ] Add BeerXML export generator
- [ ] Add validation for BeerXML files
- [ ] Add conflict resolution for imports

**Frontend Tasks**:
- [ ] Complete BeerXML Import page
- [ ] Add BeerXML Export functionality
- [ ] Add recipe PDF export
- [ ] Create recipe print view
- [ ] Polish all UIs for consistency
- [ ] Add loading states everywhere
- [ ] Add error handling everywhere
- [ ] Add success notifications
- [ ] Improve mobile responsiveness

**Documentation**:
- [ ] Update user manual
- [ ] Create video tutorials
- [ ] Update API documentation
- [ ] Create deployment guide
- [ ] Create troubleshooting guide

**Deliverables**:
- ✅ BeerXML import/export working
- ✅ PDF export functional
- ✅ UI polished and consistent
- ✅ Documentation complete

---

## 📈 EFFORT SUMMARY

| Milestone | Sprints | Weeks | Backend | Frontend | Testing | Docs |
|-----------|---------|-------|---------|----------|---------|------|
| M1: Foundation | 3 | 6 | 80h | 120h | 40h | 20h |
| M2: Batch & Fermentation | 3 | 6 | 100h | 140h | 50h | 20h |
| M3: Brew Day & Packaging | 3 | 6 | 90h | 130h | 45h | 15h |
| M4: QC & Analytics | 3 | 6 | 70h | 110h | 40h | 20h |
| M5: Home Assistant | 2 | 4 | 80h | 60h | 40h | 30h |
| M6: Advanced | 2 | 4 | 40h | 60h | 20h | 20h |
| **TOTAL** | **16** | **32** | **460h** | **620h** | **235h** | **125h** |

**Total Project Effort**: ~1,440 hours (36 weeks @ 40h/week, or 8 months)

---

## 🎯 SUCCESS METRICS

### Technical Metrics
- [ ] Test coverage: >80%
- [ ] API response time: <200ms (95th percentile)
- [ ] Frontend load time: <2s
- [ ] Zero critical security vulnerabilities
- [ ] All CI/CD tests passing

### Feature Completeness
- [ ] Equipment management: 100%
- [ ] Inventory management: 100%
- [ ] Recipe editor: 100%
- [ ] Batch tracking: 100%
- [ ] Brew day workflow: 100%
- [ ] Fermentation tracking: 100%
- [ ] Packaging: 100%
- [ ] Quality control: 100%
- [ ] Analytics: 80%
- [ ] Home Assistant: 90%

### User Experience
- [ ] Complete brew workflow: <30 minutes
- [ ] Recipe creation: <10 minutes
- [ ] Batch tracking: Daily engagement during fermentation
- [ ] Home Assistant integration: <15 minutes setup

---

## 🚀 GETTING STARTED

### Immediate Actions (Week 1):
1. Set up project board with all sprints
2. Create detailed tickets for Sprint 1
3. Set up CI/CD pipeline
4. Configure development environment
5. Review and approve this roadmap
6. Assign team members to milestones

### Weekly Cadence:
- **Monday**: Sprint planning, ticket review
- **Wednesday**: Mid-sprint check-in
- **Friday**: Sprint demo, retrospective
- **Daily**: 15-minute standup

### Decision Points:
- After M1: Validate equipment & inventory UX
- After M2: Validate batch workflow
- After M3: Validate brew day experience
- After M4: Validate analytics value
- After M5: Validate HA integration
- After M6: Production readiness review

---

**End of Implementation Roadmap**
