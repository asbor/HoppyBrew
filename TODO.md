# HoppyBrew TODO

This document organizes work based on the **COMPREHENSIVE_WORKFLOW_ANALYSIS** and **IMPLEMENTATION_ROADMAP**. Tasks are grouped by priority and functional area for efficient parallel development.

**Last Updated**: November 5, 2025  
**Reference Documents**: 
- COMPREHENSIVE_WORKFLOW_ANALYSIS.md (300+ identified features)
- IMPLEMENTATION_ROADMAP.md (32-week sprint plan)

---

## 🔴 P0 - CRITICAL (Weeks 1-12)

Must complete for MVP functionality. Without these, the application cannot support a basic brewing workflow.

### Backend - Critical Infrastructure
- [ ] Add missing fields to inventory tables:
  - [ ] `cost_per_unit` to all inventory tables
  - [ ] `expiration_date` to all inventory tables
  - [ ] `min_stock_level` to all inventory tables
  - [ ] `supplier_id` to all inventory tables
- [ ] Create `suppliers` table and model
- [ ] Create `equipment_templates` table for pre-defined systems
- [ ] Create `inventory_transactions` table for tracking purchases/usage
- [ ] Create `fermentation_readings` table (id, batch_id, date, gravity, temp, pH, notes)
- [ ] Create `batch_state_history` table for status transitions
- [ ] Add `status` enum field to batches table (design, planning, brewing, fermenting, conditioning, packaging, complete)
- [ ] Add actual readings fields to batches (actual_og, actual_fg, actual_abv, actual_efficiency)
- [ ] Fix PostgreSQL connection string construction in `services/backend/database.py`
- [ ] Remove module-level `SessionLocal()` in `services/backend/api/endpoints/users.py`
- [ ] Audit `services/backend/api/endpoints/batches.py` relationships to match ORM models

### Backend - P0 API Endpoints
- [ ] GET/POST `/api/equipment-profiles/templates` - Equipment templates
- [ ] GET `/api/inventory/low-stock` - Low stock items
- [ ] GET `/api/inventory/expiring` - Expiring ingredients
- [ ] POST `/api/inventory/check-availability` - Check recipe ingredient availability
- [ ] GET/POST `/api/suppliers` - Supplier CRUD
- [ ] PUT `/api/batches/{id}/status` - Update batch status
- [ ] POST `/api/batches/{id}/allocate-inventory` - Reserve ingredients
- [ ] GET `/api/batches/{id}/brew-sheet` - Generate brew day sheet
- [ ] POST `/api/batches/{id}/fermentation/readings` - Add fermentation reading
- [ ] GET `/api/batches/{id}/fermentation/readings` - List fermentation readings
- [ ] PUT `/api/batches/{id}/fermentation/readings/{id}` - Update reading
- [ ] DELETE `/api/batches/{id}/fermentation/readings/{id}` - Delete reading
- [ ] GET `/api/batches/{id}/fermentation/chart-data` - Chart data for fermentation

### Frontend - P0 Equipment Management
- [ ] Create Equipment Profile Creation Form:
  - [ ] Basic info (name, type, batch size capacity)
  - [ ] Mash tun volume and dimensions
  - [ ] Boil kettle volume and boil-off rate
  - [ ] Fermenter types and sizes
  - [ ] Loss factors (trub, dead space)
  - [ ] Efficiency settings
- [ ] Create Equipment Profile Selector with visual cards
- [ ] Create Equipment Templates Library (Grainfather, Anvil, BIAB, etc.)
- [ ] Add equipment validation

### Frontend - P0 Inventory Management
- [ ] Complete CRUD form for Fermentables:
  - [ ] Type, name, origin, color, potential
  - [ ] Amount, cost, supplier, purchase date
  - [ ] Expiration date, lot number, notes
- [ ] Complete CRUD form for Hops:
  - [ ] Variety, type, form, alpha/beta acid %
  - [ ] Origin, harvest year, amount, cost
  - [ ] Supplier, storage temp, lot number
- [ ] Complete CRUD form for Yeasts:
  - [ ] Lab, product code, strain, type, form
  - [ ] Attenuation, temp range, flocculation
  - [ ] Packages, manufacture/expiry dates, viability, cost
- [ ] Complete CRUD form for Miscs:
  - [ ] Type, name, use, amount, cost, expiration
- [ ] Enhance Inventory Dashboard:
  - [ ] Low stock alert component (configurable thresholds)
  - [ ] Expiring ingredients alert component
  - [ ] Inventory value calculation display
- [ ] Create Supplier Management page
- [ ] Add inventory search and filtering
- [ ] Add bulk edit operations

### Frontend - P0 Recipe Editor
- [ ] Create Interactive Recipe Editor form:
  - [ ] Basic info (name, style, type, batch size, boil time, efficiency)
  - [ ] Equipment profile selector
  - [ ] Fermentables section with ingredient picker from inventory
  - [ ] Hops section with variety picker and timing
  - [ ] Yeast section with strain picker
  - [ ] Miscs section
- [ ] Integrate RecipeCalculatorWidget (already exists in components)
- [ ] Add live calculation updates on ingredient changes
- [ ] Add style guidelines comparison panel
- [ ] Add recipe validation warnings
- [ ] Add ingredient availability checker
- [ ] Create recipe scaling calculator UI
- [ ] Add recipe save/update/delete actions
- [ ] Add visual SRM color preview

### Frontend - P0 Batch Management
- [ ] Create Batch Creation Wizard:
  - [ ] Step 1: Select recipe with preview
  - [ ] Step 2: Set brew date and time
  - [ ] Step 3: Check ingredient availability
  - [ ] Step 4: Select equipment profile
  - [ ] Step 5: Review and create batch
- [ ] Integrate BatchStatusTimeline component (already exists)
- [ ] Create Batch Dashboard with status cards (brewing, fermenting, etc.)
- [ ] Create Printable Brew Day Sheet
- [ ] Create Brew Day Checklist generator
- [ ] Enhance Batch Detail page with all batch info
- [ ] Create batch list with filtering and sorting
- [ ] Add batch status badges and transitions

### Frontend - P0 Fermentation Tracking
- [ ] Create Fermentation Log Entry Form:
  - [ ] Date/time picker
  - [ ] Gravity input (SG/Plato selector)
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
  - [ ] Fermentation stage indicator
- [ ] Add fermentation timeline to batch detail page
- [ ] Create fermentation completion indicator
- [ ] Add stable gravity detection (3 days same reading)

### Testing - P0
- [ ] Unit tests for equipment validation
- [ ] Unit tests for inventory calculations
- [ ] Unit tests for recipe calculations (ABV, IBU, SRM, attenuation)
- [ ] Unit tests for batch state machine
- [ ] Integration tests for inventory CRUD
- [ ] Integration tests for recipe CRUD
- [ ] Integration tests for batch creation
- [ ] Integration tests for fermentation readings
- [ ] E2E test: Create equipment profile
- [ ] E2E test: Add ingredients with costs
- [ ] E2E test: Create complete recipe
- [ ] E2E test: Create batch from recipe
- [ ] E2E test: Log fermentation readings

---

## 🟡 P1 - HIGH PRIORITY (Weeks 13-24)

Essential for complete brewing experience. Required for production readiness.

### Backend - P1 Infrastructure
- [ ] Create `brew_day_sessions` table for detailed brew day tracking
- [ ] Create `brew_day_steps` table for step-by-step logging
- [ ] Create `packaging_details` table (method, carbonation, volumes, counts)
- [ ] Create `tastings` table (ratings, notes, photos, style comparison)
- [ ] Add photo upload support (storage configuration)
- [ ] Add batch comparison query functions
- [ ] Add trend calculation functions

### Backend - P1 API Endpoints
- [ ] POST `/api/batches/{id}/brew-day/start` - Start brew day session
- [ ] POST `/api/batches/{id}/brew-day/step` - Log brew day step
- [ ] PUT `/api/batches/{id}/brew-day/step/{step_id}` - Update step
- [ ] POST `/api/batches/{id}/brew-day/complete` - Complete brew day
- [ ] POST `/api/batches/{id}/packaging` - Add packaging details
- [ ] PUT `/api/batches/{id}/packaging` - Update packaging
- [ ] POST `/api/tools/calculate/priming-sugar` - Priming calculator
- [ ] POST `/api/tools/calculate/carbonation-psi` - Force carb calculator
- [ ] POST `/api/batches/{id}/tastings` - Add tasting note
- [ ] GET `/api/batches/{id}/tastings` - List tastings
- [ ] PUT `/api/batches/{id}/tastings/{id}` - Update tasting
- [ ] DELETE `/api/batches/{id}/tastings/{id}` - Delete tasting
- [ ] GET `/api/analytics/batches/summary` - Batch statistics
- [ ] GET `/api/analytics/efficiency` - Efficiency trends
- [ ] GET `/api/analytics/costs` - Cost analysis
- [ ] GET `/api/analytics/inventory/usage` - Ingredient usage
- [ ] GET `/api/analytics/recipes/popular` - Top recipes
- [ ] GET `/api/analytics/calendar` - Brewing calendar data

### Frontend - P1 Brew Day Tracking
- [ ] Create Brew Day Workflow UI:
  - [ ] Pre-brew checklist
  - [ ] Mashing phase tracker
  - [ ] Boil phase tracker with timer
  - [ ] Hop addition timer with alerts
  - [ ] Cooling phase tracker
  - [ ] Yeast pitching logger
- [ ] Create Brew Day Timer Component with notifications
- [ ] Create Actual Readings Forms:
  - [ ] Strike water temperature
  - [ ] Mash temperature and pH
  - [ ] Pre-boil gravity and volume
  - [ ] Original Gravity (OG)
  - [ ] Post-boil volume
  - [ ] Fermenter volume
  - [ ] Pitching temperature
- [ ] Create Deviation Tracker for recipe variances
- [ ] Add brew day progress indicator
- [ ] Create mobile-optimized brew day view
- [ ] Add efficiency calculation from actuals

### Frontend - P1 Packaging
- [ ] Create Packaging Form:
  - [ ] Packaging date
  - [ ] Method (Bottle/Keg/Can)
  - [ ] Carbonation method (Natural/Forced/Cask)
  - [ ] Final gravity
  - [ ] Volume packaged
  - [ ] Bottle/keg count
  - [ ] Conditioning schedule
- [ ] Integrate priming sugar calculator from useCalculators
- [ ] Create force carbonation PSI calculator
- [ ] Create CO2 volumes calculator
- [ ] Add packaging completion workflow
- [ ] Add ready date tracking and countdown
- [ ] Add packaging photo upload

### Frontend - P1 Quality Control
- [ ] Create Tasting Notes Form:
  - [ ] Tasting date
  - [ ] Overall rating (1-5 stars)
  - [ ] Category ratings (Appearance, Aroma, Flavor, Mouthfeel)
  - [ ] Carbonation assessment
  - [ ] Clarity rating
  - [ ] Detailed notes
  - [ ] Photo upload
- [ ] Create Tasting History Timeline
- [ ] Add style comparison scorecard
- [ ] Create rating display components
- [ ] Support multiple tastings per batch

### Frontend - P1 Analytics Dashboard
- [ ] Create Analytics Dashboard:
  - [ ] Summary statistics cards
  - [ ] Efficiency trend chart
  - [ ] Cost per batch chart
  - [ ] Brewing frequency chart
  - [ ] Style distribution pie chart
  - [ ] Top recipes list
- [ ] Create Batch Comparison View (side-by-side)
- [ ] Create Brewing Calendar view
- [ ] Add date range filtering
- [ ] Create export to PDF/Excel functionality
- [ ] Add ingredient usage report
- [ ] Create cost breakdown charts

### Testing - P1
- [ ] Unit tests for efficiency calculation
- [ ] Unit tests for carbonation calculations
- [ ] Unit tests for analytics calculations
- [ ] Integration tests for brew day workflow
- [ ] Integration tests for packaging
- [ ] Integration tests for tastings
- [ ] Integration tests for analytics endpoints
- [ ] E2E test: Complete brew day workflow
- [ ] E2E test: Package batch
- [ ] E2E test: Add tasting notes
- [ ] E2E test: View analytics dashboard

---

## 🟢 P2 - MEDIUM PRIORITY (Weeks 25-32)

Enhanced features for advanced users and Home Assistant integration.

### Backend - P2 Infrastructure
- [ ] Add MQTT client library (paho-mqtt)
- [ ] Create MQTT broker connection manager
- [ ] Implement MQTT discovery protocol
- [ ] Add MQTT publish functions for sensors
- [ ] Create device integration framework
- [ ] Add iSpindel integration (HTTP endpoint for data)
- [ ] Add WebSocket support for real-time updates
- [ ] Add water chemistry calculation functions
- [ ] Complete BeerXML import parser
- [ ] Add BeerXML export generator

### Backend - P2 API Endpoints
- [ ] POST `/api/devices` - Register device
- [ ] GET `/api/devices` - List devices
- [ ] PUT `/api/devices/{id}` - Update device
- [ ] DELETE `/api/devices/{id}` - Remove device
- [ ] POST `/api/devices/ispindel/data` - iSpindel data webhook
- [ ] POST `/api/tools/calculate/strike-water` - Strike water temp
- [ ] POST `/api/tools/calculate/yeast-pitch` - Yeast pitch rate
- [ ] POST `/api/tools/calculate/refractometer` - Refractometer correction
- [ ] POST `/api/tools/calculate/dilution` - Dilution calculator
- [ ] POST `/api/tools/calculate/water-chemistry` - Water chemistry
- [ ] POST `/api/tools/calculate/mash-ph` - Mash pH prediction
- [ ] POST `/api/recipes/import/beerxml` - BeerXML import
- [ ] GET `/api/recipes/{id}/export/beerxml` - BeerXML export
- [ ] GET `/api/recipes/{id}/export/pdf` - PDF export

### Frontend - P2 Home Assistant Integration
- [ ] Create Device Management page:
  - [ ] Add/edit/delete devices
  - [ ] Device status display
  - [ ] Device configuration
- [ ] Create Real-time Dashboard with WebSocket
- [ ] Add device pairing wizard
- [ ] Add device status indicators
- [ ] Create HA integration documentation

### Frontend - P2 Water Chemistry & Tools
- [ ] Create Tools page with calculator widgets
- [ ] Create Water Chemistry Calculator:
  - [ ] Source water profile input
  - [ ] Target water profile selection
  - [ ] Mineral additions calculator
  - [ ] pH prediction display
- [ ] Create Advanced Calculator Tools:
  - [ ] Strike water temperature
  - [ ] Yeast pitch rate calculator
  - [ ] Starter size calculator
  - [ ] Refractometer correction
  - [ ] Dilution calculator
  - [ ] Alcohol correction for hydrometer

### Frontend - P2 Recipe Features
- [ ] Complete BeerXML Import page with validation
- [ ] Add BeerXML Export functionality
- [ ] Add recipe PDF export
- [ ] Create recipe print view
- [ ] Add recipe versioning UI
- [ ] Add recipe comparison view
- [ ] Add recipe templates library
- [ ] Add recipe search with filters
- [ ] Add recipe tags and categories

### Frontend - P2 UI Polish
- [ ] Add loading states to all components
- [ ] Add error handling to all forms
- [ ] Add success toast notifications
- [ ] Improve mobile responsiveness across all pages
- [ ] Add dark mode support
- [ ] Add keyboard shortcuts for power users
- [ ] Add contextual help tooltips

### Testing - P2
- [ ] Unit tests for MQTT functions
- [ ] Unit tests for water chemistry calculations
- [ ] Integration tests with MQTT broker
- [ ] Integration tests for device data flow
- [ ] E2E test: Device pairing and data
- [ ] E2E test: BeerXML import/export
- [ ] Test HA discovery protocol
- [ ] Test real-time updates via WebSocket

### Documentation - P2
- [ ] Create user manual with screenshots
- [ ] Create video tutorials for key workflows
- [ ] Update API documentation (Swagger/ReDoc)
- [ ] Create deployment guide for various platforms
- [ ] Create troubleshooting guide
- [ ] Document Home Assistant setup procedures
- [ ] Document device integration procedures
- [ ] Create contribution guidelines

---

## �� P3 - LOW PRIORITY (Future Enhancements)

Nice-to-have features for future releases.

### Advanced Features
- [ ] AI recipe suggestions based on inventory
- [ ] Recipe builder wizard for beginners
- [ ] Community recipe sharing platform
- [ ] Recipe voting and popularity tracking
- [ ] Batch blending support
- [ ] Multi-batch scheduling
- [ ] Brew buddy invitations/collaboration
- [ ] Competition entry tracking
- [ ] Medal tracking
- [ ] Native mobile apps (iOS/Android)
- [ ] Voice control integration
- [ ] Augmented reality color matching
- [ ] Smart brewing equipment integration
- [ ] Marketplace integration
- [ ] Brew club features

---

## 🛠️ TECHNICAL DEBT & MAINTENANCE

### Current Technical Debt
- [ ] Pydantic v2 migration (20 failing tests currently)
- [ ] Frontend state management (implement Pinia)
- [ ] Centralize API base URLs using Nuxt runtime config
- [ ] Create typed API client with Zod validation
- [ ] Standardize error handling patterns
- [ ] Introduce service/repository layer in backend
- [ ] Add Alembic migrations version control
- [ ] Align Docker Compose with container entrypoints
- [ ] Remove `--reload` from production backend image
- [ ] Add `.env.example` file
- [ ] Extend Makefile for linting, tests, formatters
- [ ] Make primary keys non-nullable (e.g., StyleGuidelines.id)
- [ ] Review cascades/constraints to avoid orphaned rows
- [ ] Decide on Selenium scraper (keep or remove)
- [ ] Replace placeholder modules in `services/backend/modules`

### DevOps & Infrastructure
- [ ] Configure CI (GitHub Actions) for linting, type checks, tests
- [ ] Set up automated frontend unit tests (Vitest)
- [ ] Harden database configuration (secrets, health checks)
- [ ] Set up automated database backups
- [ ] Add structured logging throughout application
- [ ] Set up application performance monitoring
- [ ] Configure dependency vulnerability scanning
- [ ] Set up Docker Hub automated builds

### Documentation Maintenance
- [ ] Update README.md to remove template placeholders
- [ ] Refresh setup instructions (Docker, local, testing)
- [ ] Add concise architecture overview
- [ ] Create changelog/decision log
- [ ] Maintain weekly status updates in `documents/status/`
- [ ] Create per-agent prompt templates

---

## 📊 PROGRESS TRACKING

### Overall Completion Estimate
- Equipment Management: 5% → Target: 100%
- Inventory Management: 15% → Target: 100%
- Recipe Design: 25% → Target: 100%
- Batch Management: 20% → Target: 100%
- Brew Day Tracking: 0% → Target: 100%
- Fermentation Monitoring: 5% → Target: 100%
- Packaging: 0% → Target: 100%
- Quality Control: 0% → Target: 100%
- Analytics: 0% → Target: 80%
- Home Assistant Integration: 30% → Target: 90%

**Current Overall Progress**: ~15-20%  
**Target for MVP (P0 Complete)**: ~60%  
**Target for Production (P0+P1 Complete)**: ~85%

---

**Last Updated**: November 5, 2025  
**Next Review**: After Sprint 1 (Week 2)
