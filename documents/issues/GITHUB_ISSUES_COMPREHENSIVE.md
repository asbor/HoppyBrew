# GitHub Issues - Comprehensive Brewing Tracker

**Generated**: November 5, 2025  
**Total Issues**: 50+  
**Priority Levels**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)

---

## 🚨 P0 - Critical (Must Have for MVP)

### ISSUE #1: Batch Status Workflow System
**Priority**: P0  
**Component**: Backend + Frontend  
**Estimate**: 5 days

**Description**:
Implement a complete batch status workflow system to track the brewing lifecycle from planning to completion.

**Requirements**:
- Add `status` enum field to `batches` table: `planning`, `brewing`, `fermenting`, `conditioning`, `packaging`, `complete`, `archived`
- Create state machine logic with valid state transitions
- Add API endpoints:
  - `PUT /batches/{id}/status` - Update batch status
  - `GET /batches/{id}/workflow` - Get workflow history
- Create batch status timeline visualization in frontend
- Add status-based filtering and sorting
- Implement automatic status progression triggers

**Acceptance Criteria**:
- [ ] Database migration adds status field with enum constraint
- [ ] State transitions are validated (can't skip states)
- [ ] Frontend displays current status with visual indicator
- [ ] Status change triggers are logged in batch_logs
- [ ] Tests cover all status transitions

**Dependencies**: None  
**Blocks**: #2, #3, #6

---

### ISSUE #2: Fermentation Tracking System
**Priority**: P0  
**Component**: Backend + Frontend + Database  
**Estimate**: 8 days

**Description**:
Implement comprehensive fermentation tracking to monitor gravity, temperature, and fermentation progress.

**Requirements**:

**Backend**:
- Create `fermentation_readings` table:
  - batch_id (FK to batches)
  - reading_date (timestamp)
  - gravity (float)
  - temperature (float)
  - ph (float, optional)
  - notes (text, optional)
- Add endpoints:
  - `POST /batches/{id}/fermentation/start` - Start fermentation
  - `POST /batches/{id}/fermentation/readings` - Add reading
  - `GET /batches/{id}/fermentation/readings` - List readings
  - `PUT /batches/{id}/fermentation/readings/{reading_id}` - Update reading
  - `DELETE /batches/{id}/fermentation/readings/{reading_id}` - Delete reading
- Add fermentation completion detection logic (3 consecutive stable readings)

**Frontend**:
- Fermentation reading input form with date/time picker
- Chart visualization of gravity over time
- Temperature trend chart
- Fermentation progress indicator
- Automatic ABV calculation display
- Quick-add reading modal
- Reading history table

**Acceptance Criteria**:
- [ ] Can record multiple readings per day
- [ ] Charts display properly with multiple data points
- [ ] Gravity readings calculate apparent attenuation
- [ ] Temperature deviations are highlighted
- [ ] Fermentation completion is detected automatically
- [ ] Mobile-friendly input form
- [ ] Tests cover CRUD operations and calculations

**Dependencies**: #1 (batch status)  
**Blocks**: #6, #18

---

### ISSUE #3: Inventory Integration with Batches
**Priority**: P0  
**Component**: Backend + Frontend  
**Estimate**: 5 days

**Description**:
Integrate inventory system with batch creation to prevent brewing without ingredients and track usage.

**Requirements**:

**Backend**:
- Add inventory availability check endpoint:
  - `POST /inventory/check-availability` (body: recipe_id, batch_size)
- Add inventory allocation endpoint:
  - `POST /inventory/allocate` (body: batch_id)
- Add inventory deduction logic on batch status change to 'brewing'
- Add inventory restoration on batch deletion/cancellation
- Add `allocated_to_batch_id` field to inventory tables

**Frontend**:
- Pre-batch-creation availability check
- Visual indicator of ingredient availability in recipe view
- Insufficient ingredients warning modal
- Inventory deduction confirmation
- Batch ingredient cost calculation display

**Business Logic**:
- Calculate required ingredient quantities based on recipe and batch size
- Check inventory quantities against requirements
- Reserve ingredients when batch is created (allocated)
- Deduct inventory when batch status moves to 'brewing'
- Release allocation if batch is cancelled before brewing

**Acceptance Criteria**:
- [ ] Cannot create batch without sufficient ingredients
- [ ] Inventory shows allocated quantities
- [ ] Batch creation wizard shows ingredient availability
- [ ] Inventory deduction is atomic (all-or-nothing)
- [ ] Batch cost is calculated from inventory costs
- [ ] Tests cover edge cases (concurrent batches, partial availability)

**Dependencies**: None  
**Blocks**: #4, #7

---

### ISSUE #4: Interactive Recipe Editor
**Priority**: P0  
**Component**: Frontend  
**Estimate**: 7 days

**Description**:
Build a comprehensive, user-friendly recipe creation and editing interface with live calculations.

**Requirements**:

**Recipe Editor Features**:
- Multi-step form wizard (Info → Fermentables → Hops → Yeast → Misc → Review)
- Drag-and-drop ingredient ordering
- Ingredient selection from inventory with autocomplete
- Live calculation updates (OG, FG, ABV, IBU, SRM)
- Recipe validation with error highlighting
- Save as draft functionality
- Recipe cloning
- Recipe versioning UI
- Print-friendly recipe view
- Recipe export to BeerXML

**Ingredient Management**:
- Add ingredient button with modal
- Inline editing of ingredient quantities
- Percentage-based vs weight-based input toggle
- Hop addition timing selector (First Wort, 60min, 30min, etc.)
- Yeast attenuation calculator
- Misc ingredient usage selector (Boil, Fermentation, Bottling)

**Calculations Panel**:
- Real-time OG/FG/ABV display
- IBU with method selector (Tinseth, Rager)
- Color (SRM/EBC) with visual indicator
- Estimated efficiency
- Batch cost estimate
- Style guideline comparison

**Acceptance Criteria**:
- [ ] All recipe fields can be edited
- [ ] Calculations update on every change
- [ ] Ingredient autocomplete searches inventory
- [ ] Validation prevents invalid recipes
- [ ] Can save incomplete recipe as draft
- [ ] Recipe loads correctly for editing
- [ ] Mobile-responsive design
- [ ] Keyboard navigation support

**Dependencies**: #3 (inventory integration)  
**Blocks**: None

---

### ISSUE #5: Brewing Calculators Suite
**Priority**: P0  
**Component**: Backend + Frontend  
**Estimate**: 6 days

**Description**:
Implement comprehensive brewing calculator tools as both standalone pages and integrated components.

**Requirements**:

**Backend Calculations** (add to brewing_calculations.py):
- `calculate_priming_sugar(batch_size, co2_volumes, temperature)` - Priming sugar for carbonation
- `calculate_yeast_pitch_rate(batch_size, og, yeast_viability, cell_count)` - Yeast pitching
- `calculate_strike_water_temp(grain_temp, mash_temp, grain_weight, water_volume)` - Strike water
- `calculate_refractometer_correction(brix_reading, wort_correction_factor)` - Refractometer to SG
- `calculate_dilution(current_gravity, current_volume, target_gravity)` - Water addition
- `calculate_concentration(current_gravity, current_volume, target_gravity)` - Boil-off
- `calculate_mash_water_volume(grain_weight, mash_ratio)` - Mash water
- `calculate_sparge_water_volume(target_preboil, grain_weight, mash_ratio)` - Sparge water
- `calculate_hydrometer_correction(reading, temp, calibration_temp)` - Temperature correction
- `calculate_attenuation(og, fg)` - Apparent/Real attenuation

**API Endpoints**:
- `POST /tools/calculate/abv` (body: {og, fg})
- `POST /tools/calculate/ibu` (body: {alpha_acid, weight, boil_time, batch_size, gravity})
- `POST /tools/calculate/srm` (body: {grain_color, grain_weight, batch_size})
- `POST /tools/calculate/priming-sugar` (body: {batch_size, co2_volumes, temp})
- `POST /tools/calculate/yeast-pitch` (body: {batch_size, og, viability, cell_count})
- `POST /tools/calculate/strike-water` (body: {grain_temp, mash_temp, grain_weight, water_volume})
- `POST /tools/calculate/refractometer` (body: {brix, wcf})
- `POST /tools/calculate/dilution` (body: {current_gravity, current_volume, target_gravity})
- `POST /tools/calculate/hydrometer-correction` (body: {reading, temp, calibration_temp})

**Frontend Components**:
- Calculator card component (reusable)
- Individual calculator pages under /tools/
- Integration into recipe editor
- Integration into batch fermentation tracking
- Input validation with helpful error messages
- Unit conversion support (Imperial/Metric)
- Save calculation history
- Share calculation results

**Acceptance Criteria**:
- [ ] All calculations return accurate results
- [ ] API endpoints have comprehensive tests
- [ ] Frontend validates inputs before API call
- [ ] Calculators work offline with cached logic
- [ ] Results display with appropriate precision
- [ ] Unit conversion is seamless
- [ ] Mobile-friendly layouts
- [ ] Keyboard shortcuts for power users

**Dependencies**: None  
**Blocks**: #4 (recipe editor integration)

---

## 📌 P1 - High Priority (Complete Experience)

### ISSUE #6: Brew Day Tracking System
**Priority**: P1  
**Component**: Frontend + Backend  
**Estimate**: 6 days

**Description**:
Create a step-by-step brew day tracking system with timers, checklists, and real-time data entry.

**Requirements**:

**Brew Day Session**:
- Start brew day session (creates brewing_session record)
- Pre-brew checklist (equipment, ingredients ready)
- Mash steps with temperature/time tracking
- Mash-out confirmation
- Sparge tracking (volume, gravity)
- Boil timer with hop addition alerts
- Hop addition checklist
- Cooling phase tracking
- Transfer to fermenter
- OG measurement and recording
- Yeast pitching confirmation
- Cleanup checklist

**Frontend Features**:
- Brew day dashboard with current step highlighted
- Countdown timers for boil/mash
- Audio/visual alerts for hop additions
- Quick note-taking
- Photo upload for brew day
- Gravity reading quick-entry
- Equipment temperature tracking
- Volume measurement tracking
- Pause/resume brew session

**Backend**:
- `brewing_sessions` table (batch_id, start_time, end_time, steps_json)
- `POST /batches/{id}/brew-session/start`
- `PUT /batches/{id}/brew-session/step` - Update step status
- `POST /batches/{id}/brew-session/complete`
- Store actual vs expected metrics
- Calculate efficiency from measurements

**Acceptance Criteria**:
- [ ] Can start and complete brew session
- [ ] Timers count down accurately
- [ ] Alerts trigger at correct times
- [ ] Can pause and resume session
- [ ] All measurements are saved
- [ ] Efficiency is calculated automatically
- [ ] Mobile-optimized for brew day use
- [ ] Works offline (PWA)

**Dependencies**: #1 (batch status)  
**Blocks**: None

---

### ISSUE #7: Complete Inventory Management UI
**Priority**: P1  
**Component**: Frontend  
**Estimate**: 5 days

**Description**:
Build full CRUD interfaces for all inventory types (fermentables, hops, yeasts, miscs).

**Requirements**:

**Per Ingredient Type**:
- List view with search/filter/sort
- Create new inventory item modal
- Edit inventory item modal
- Delete with confirmation
- Bulk import from CSV
- Quick actions (duplicate, adjust quantity)

**Fermentables**:
- Fields: name, type (grain, extract, sugar, etc.), origin, supplier, color, potential, quantity, unit, cost, notes, expiration_date, min_stock
- Type-specific fields (diastatic power for grains, moisture for extracts)

**Hops**:
- Fields: name, variety, origin, alpha_acid, beta_acid, form (pellet, whole, plug), quantity, unit, cost, harvest_year, notes, expiration_date, min_stock
- AA% degradation calculator

**Yeasts**:
- Fields: name, lab, product_id, type (ale, lager, etc.), form (dry, liquid, slant), attenuation, temp_range, flocculation, quantity, unit, cost, manufacture_date, expiration_date, min_stock
- Viability calculator

**Miscs**:
- Fields: name, type (spice, fining, flavor, etc.), use (boil, fermentation, bottling), quantity, unit, cost, notes, expiration_date, min_stock

**Common Features**:
- Low stock warnings
- Expiration date warnings
- Cost per unit tracking
- Supplier management
- Purchase history
- Usage history (linked to batches)
- Inventory adjustments log
- Export inventory report

**Acceptance Criteria**:
- [ ] Full CRUD for all four ingredient types
- [ ] Search works across all fields
- [ ] Filters work correctly (in stock, low stock, expired)
- [ ] Sorting works on all columns
- [ ] CSV import validates data
- [ ] Warnings display prominently
- [ ] Mobile-responsive tables
- [ ] Pagination for large inventories

**Dependencies**: #3 (inventory integration)  
**Blocks**: None

---

### ISSUE #8: Packaging Management System
**Priority**: P1  
**Component**: Backend + Frontend  
**Estimate**: 4 days

**Description**:
Implement packaging workflow for bottling and kegging, including carbonation tracking.

**Requirements**:

**Database**:
- `packaging_details` table:
  - batch_id (FK)
  - packaging_type (bottle, keg)
  - packaging_date
  - target_carbonation (CO2 volumes)
  - priming_method (sugar, forced)
  - priming_sugar_type (if applicable)
  - priming_sugar_amount
  - bottle_count / keg_size
  - conditioning_temp
  - ready_date (estimated)
  - notes

**Backend**:
- `POST /batches/{id}/packaging/start` - Initialize packaging
- `POST /batches/{id}/packaging/calculate-priming` - Calculate priming sugar
- `PUT /batches/{id}/packaging` - Update packaging details
- `POST /batches/{id}/packaging/complete` - Finalize packaging

**Frontend**:
- Packaging wizard (type selection → priming calculation → details → confirmation)
- Priming sugar calculator integration
- Bottle/keg quantity input
- Conditioning timeline calculator
- Ready date estimator
- Label generation (optional)

**Acceptance Criteria**:
- [ ] Can package batch as bottles or keg
- [ ] Priming sugar calculates correctly
- [ ] Conditioning time estimates accurately
- [ ] Ready date displayed on batch list
- [ ] Can update packaging details
- [ ] Batch status updates to 'complete' after packaging
- [ ] Tests cover both bottling and kegging

**Dependencies**: #5 (priming calculator)  
**Blocks**: None

---

### ISSUE #9: Quality Control & Tasting Notes
**Priority**: P1  
**Component**: Backend + Frontend + Database  
**Estimate**: 5 days

**Description**:
Implement comprehensive quality control system with tasting notes, ratings, and sensory evaluation.

**Requirements**:

**Database**:
- `tastings` table:
  - batch_id (FK)
  - tasting_date
  - taster_name
  - appearance_score (1-5)
  - appearance_notes
  - aroma_score (1-5)
  - aroma_notes
  - flavor_score (1-5)
  - flavor_notes
  - mouthfeel_score (1-5)
  - mouthfeel_notes
  - overall_score (1-5)
  - overall_notes
  - defects (array of defect types)
  - photo_url
  - would_brew_again (boolean)

**Backend**:
- `POST /batches/{id}/tastings` - Add tasting note
- `GET /batches/{id}/tastings` - List all tastings for batch
- `PUT /batches/{id}/tastings/{tasting_id}` - Update tasting
- `DELETE /batches/{id}/tastings/{tasting_id}` - Delete tasting
- `GET /tastings/my` - Get all my tastings
- Calculate average scores per batch

**Frontend**:
- Tasting note form (BJCP-style scorecard)
- Appearance: clarity, color, head retention
- Aroma: malt, hops, fermentation, other
- Flavor: malt, hops, bitterness, balance, finish
- Mouthfeel: body, carbonation, warmth
- Overall impression
- Defect selection (DMS, diacetyl, oxidation, infection, etc.)
- Photo upload for appearance
- Rating visualization (radar chart)
- Tasting history per batch
- Best batches ranking

**Acceptance Criteria**:
- [ ] Can create multiple tastings per batch
- [ ] Scores are validated (1-5 range)
- [ ] Photos upload successfully
- [ ] Defects are categorized correctly
- [ ] Average batch score calculates
- [ ] Tasting history displays chronologically
- [ ] Mobile-friendly scorecard
- [ ] Can export tasting notes

**Dependencies**: #1 (batch status - only complete batches)  
**Blocks**: None

---

### ISSUE #10: Analytics Dashboard
**Priority**: P1  
**Component**: Backend + Frontend  
**Estimate**: 6 days

**Description**:
Create comprehensive analytics dashboard with batch metrics, trends, and insights.

**Requirements**:

**Analytics Endpoints**:
- `GET /analytics/batches/summary` - Total batches, success rate, avg rating
- `GET /analytics/efficiency` - Mash efficiency trends over time
- `GET /analytics/costs` - Cost per batch, ingredient costs breakdown
- `GET /analytics/inventory/usage` - Most used ingredients
- `GET /analytics/recipes/popular` - Most brewed recipes
- `GET /analytics/styles/distribution` - Batch count by style
- `GET /analytics/timeline` - Brewing frequency calendar

**Metrics**:
- Total batches brewed
- Total volume produced
- Average batch rating
- Success rate (batches rated >4)
- Average efficiency
- Average cost per batch
- Most brewed recipe
- Most used hops/fermentables/yeast
- Brewing frequency (batches per month)
- Current batches in process
- Inventory value

**Visualizations**:
- Batch count over time (line chart)
- Efficiency trends (line chart)
- Cost breakdown (pie chart)
- Style distribution (donut chart)
- Brewing frequency heatmap (calendar)
- Ingredient usage (bar chart)
- Batch ratings distribution (histogram)
- Current batch status (progress cards)

**Acceptance Criteria**:
- [ ] All analytics endpoints return correct data
- [ ] Charts render correctly with real data
- [ ] Date range filtering works
- [ ] Metrics update in real-time
- [ ] Dashboard is responsive
- [ ] Data can be exported to CSV
- [ ] Loading states for slow queries
- [ ] Caching for expensive calculations

**Dependencies**: #9 (tasting ratings needed for success metrics)  
**Blocks**: None

---

## 🔧 P2 - Medium Priority (Enhanced Features)

### ISSUE #11: Water Chemistry Management
**Priority**: P2  
**Component**: Backend + Frontend  
**Estimate**: 5 days

**Description**:
Implement water profile management and chemistry calculations for advanced brewers.

**Requirements**:
- Expand water_profiles table (Ca, Mg, Na, Cl, SO4, HCO3)
- Water profile editor UI
- Water chemistry calculator
- Salt addition calculator
- Water treatment recommendations
- pH adjustment calculator
- Water profile comparison with target styles

**Dependencies**: None  
**Blocks**: None

---

### ISSUE #12: Equipment Profile Management
**Priority**: P2  
**Component**: Frontend  
**Estimate**: 3 days

**Description**:
Build UI for equipment profile creation and management.

**Requirements**:
- Equipment profile CRUD interface
- Equipment-specific calculations (boil-off rate, deadspace, etc.)
- Equipment selection in recipe/batch
- Multi-equipment support
- Equipment efficiency tracking

**Dependencies**: None  
**Blocks**: None

---

### ISSUE #13: Fermentation Profile Templates
**Priority**: P2  
**Component**: Backend + Frontend + Database  
**Estimate**: 4 days

**Description**:
Create reusable fermentation profile templates for common fermentation schedules.

**Requirements**:
- `fermentation_profiles` table (name, description, stages_json)
- CRUD for fermentation profiles
- Profile application to batches
- Common profiles pre-loaded (ale, lager, saison, etc.)
- Custom profile creation

**Dependencies**: #2 (fermentation tracking)  
**Blocks**: None

---

### ISSUE #14: Recipe Sharing & Community
**Priority**: P2  
**Component**: Backend + Frontend  
**Estimate**: 6 days

**Description**:
Enable recipe sharing, commenting, and community features.

**Requirements**:
- Recipe visibility setting (private, public, shared)
- Recipe sharing by link
- Recipe voting/likes
- Recipe comments
- Recipe forking (clone with attribution)
- Popular recipes page
- User profiles

**Dependencies**: Need authentication system  
**Blocks**: None

---

### ISSUE #15: Advanced Calculation Tools
**Priority**: P2  
**Component**: Backend  
**Estimate**: 4 days

**Description**:
Add specialized brewing calculations for advanced users.

**Requirements**:
- Color blending calculator
- Hop substitution calculator
- Yeast blending calculator
- Extract to all-grain conversion
- All-grain to extract conversion
- Recipe scaling (complex - maintains hop utilization)
- IBU methods (Rager, Garetz, Daniels)
- Color methods (Daniels, Mosher)

**Dependencies**: #5 (calculator infrastructure)  
**Blocks**: None

---

### ISSUE #16: Batch Comparison Tool
**Priority**: P2  
**Component**: Frontend  
**Estimate**: 3 days

**Description**:
Create side-by-side batch comparison interface.

**Requirements**:
- Select multiple batches to compare
- Side-by-side metrics comparison
- Fermentation curves overlay
- Tasting notes comparison
- Recipe differences highlight
- Export comparison report

**Dependencies**: #9, #10 (tasting and analytics)  
**Blocks**: None

---

### ISSUE #17: Recipe Recommendations
**Priority**: P2  
**Component**: Backend  
**Estimate**: 5 days

**Description**:
AI-powered recipe suggestions based on inventory and preferences.

**Requirements**:
- Suggest recipes based on available inventory
- Suggest ingredient substitutions
- Recipe similarity matching
- Style-based recommendations
- Seasonal recipe suggestions
- Beginner-friendly recipe filtering

**Dependencies**: #7 (inventory UI)  
**Blocks**: None

---

### ISSUE #18: Dry Hopping Schedule Manager
**Priority**: P2  
**Component**: Frontend + Backend  
**Estimate**: 3 days

**Description**:
Manage dry hop additions during fermentation with reminders.

**Requirements**:
- Dry hop schedule definition
- Calendar integration
- Reminder notifications
- Dry hop addition logging
- Impact on IBU calculation

**Dependencies**: #2 (fermentation tracking)  
**Blocks**: None

---

### ISSUE #19: Batch Notes & Photos
**Priority**: P2  
**Component**: Frontend + Backend  
**Estimate**: 4 days

**Description**:
Enhanced note-taking and photo management for batches.

**Requirements**:
- Rich text editor for notes
- Photo gallery per batch
- Photo tagging (brew day, fermentation, final product)
- Note timestamps
- Search through notes
- Export notes with batch

**Dependencies**: None  
**Blocks**: None

---

### ISSUE #20: BeerXML Import/Export
**Priority**: P2  
**Component**: Backend + Frontend  
**Estimate**: 4 days

**Description**:
Support BeerXML format for recipe import/export.

**Requirements**:
- Import BeerXML files
- Export recipes to BeerXML
- Batch import multiple recipes
- Validation of imported data
- Mapping of BeerXML fields to database

**Dependencies**: None  
**Blocks**: None

---

## 🎨 P3 - Low Priority (Nice to Have)

### ISSUE #21: Mobile Responsiveness
**Priority**: P3  
**Component**: Frontend  
**Estimate**: 8 days

**Description**:
Complete mobile optimization for all features, critical for brew day use.

**Requirements**:
- Mobile-first responsive design
- Touch-optimized controls
- PWA functionality (offline support)
- Home screen installation
- Mobile navigation optimization
- Simplified forms for mobile

**Dependencies**: All frontend issues  
**Blocks**: None

---

### ISSUE #22: Notification System
**Priority**: P3  
**Component**: Backend + Frontend  
**Estimate**: 5 days

**Description**:
Implement notification system for reminders and alerts.

**Requirements**:
- Email notifications
- In-app notifications
- Notification preferences
- Reminder types:
  - Fermentation reading due
  - Dry hop addition
  - Packaging ready
  - Low inventory
  - Batch ready to drink
- Notification history

**Dependencies**: None  
**Blocks**: None

---

### ISSUE #23: User Authentication & Authorization
**Priority**: P3  
**Component**: Backend + Frontend  
**Estimate**: 6 days

**Description**:
Implement secure user authentication and authorization system.

**Requirements**:
- User registration
- User login (email/password)
- Password reset
- User profile management
- Role-based access control (admin, user)
- JWT token authentication
- Session management
- OAuth integration (Google, Facebook)

**Dependencies**: None  
**Blocks**: #14 (recipe sharing needs auth)

---

### ISSUE #24: Multi-User Collaboration
**Priority**: P3  
**Component**: Backend + Frontend  
**Estimate**: 7 days

**Description**:
Enable multiple users to collaborate on batches and recipes.

**Requirements**:
- Brew club/team management
- Shared inventory
- Collaborative batch tracking
- Permission system
- Activity feed
- User mentions in notes

**Dependencies**: #23 (authentication)  
**Blocks**: None

---

### ISSUE #25: Competition Management
**Priority**: P3  
**Component**: Backend + Frontend + Database  
**Estimate**: 5 days

**Description**:
Track brewing competition entries and results.

**Requirements**:
- `competitions` table (name, date, location, style_categories)
- `competition_entries` table (batch_id, competition_id, category, result, scores, feedback)
- Competition entry tracking
- Score recording
- Feedback storage
- Competition history
- Success rate by style

**Dependencies**: #9 (tasting integration)  
**Blocks**: None

---

### ISSUE #26: IoT Sensor Integration
**Priority**: P3  
**Component**: Backend + Frontend  
**Estimate**: 8 days

**Description**:
Integrate with IoT temperature sensors for automated fermentation monitoring.

**Requirements**:
- Sensor registration
- Real-time temperature data ingestion
- WebSocket for live updates
- Temperature alerts
- Chart updates in real-time
- Multiple sensor support
- Sensor calibration

**Dependencies**: #2 (fermentation tracking)  
**Blocks**: None

---

### ISSUE #27: Voice Control
**Priority**: P3  
**Component**: Frontend  
**Estimate**: 6 days

**Description**:
Hands-free brew day tracking via voice commands.

**Requirements**:
- Voice command recognition
- Brew day step navigation
- Note dictation
- Timer control
- Gravity reading entry
- Works in noisy environments

**Dependencies**: #6 (brew day tracking)  
**Blocks**: None

---

### ISSUE #28: Ingredient Marketplace Integration
**Priority**: P3  
**Component**: Backend + Frontend  
**Estimate**: 7 days

**Description**:
Integrate with ingredient suppliers for direct purchasing.

**Requirements**:
- Supplier API integration
- Ingredient price comparison
- Direct ordering
- Order tracking
- Automatic inventory updates on delivery
- Wish list functionality

**Dependencies**: #7 (inventory management)  
**Blocks**: None

---

### ISSUE #29: Augmented Reality Color Matching
**Priority**: P3  
**Component**: Frontend  
**Estimate**: 5 days

**Description**:
Use camera to match beer color to SRM scale.

**Requirements**:
- Camera access
- AR overlay with SRM guide
- Color detection algorithm
- SRM value extraction
- Photo storage
- Lighting compensation

**Dependencies**: None  
**Blocks**: None

---

### ISSUE #30: Automated Backup System
**Priority**: P3  
**Component**: Backend/DevOps  
**Estimate**: 3 days

**Description**:
Implement automated database backup and restore.

**Requirements**:
- Daily automated backups
- Backup rotation (keep 7 daily, 4 weekly, 12 monthly)
- Backup verification
- One-click restore
- Backup to cloud storage
- Disaster recovery plan

**Dependencies**: None  
**Blocks**: None

---

## 🔒 Security & Infrastructure Issues

### ISSUE #31: API Authentication & Authorization
**Priority**: P1  
**Component**: Backend  
**Estimate**: 4 days

**Description**:
Secure all API endpoints with authentication and authorization.

**Requirements**:
- JWT token generation
- Token refresh mechanism
- Protected endpoints
- Role-based access
- API key management
- Rate limiting

**Dependencies**: #23 (user authentication)  
**Blocks**: Production deployment

---

### ISSUE #32: Input Validation & Sanitization
**Priority**: P1  
**Component**: Backend + Frontend  
**Estimate**: 3 days

**Description**:
Comprehensive input validation to prevent security vulnerabilities.

**Requirements**:
- SQL injection prevention (parameterized queries)
- XSS prevention (output encoding)
- CSRF protection
- File upload validation
- Schema validation on all endpoints
- Error message sanitization

**Dependencies**: None  
**Blocks**: Production deployment

---

### ISSUE #33: Database Migration Version Control
**Priority**: P2  
**Component**: Backend/DevOps  
**Estimate**: 2 days

**Description**:
Properly version control and manage database migrations.

**Requirements**:
- Alembic migration workflow
- Migration naming convention
- Rollback capability
- Migration testing
- Production migration process
- Migration documentation

**Dependencies**: None  
**Blocks**: None

---

### ISSUE #34: Monitoring & Logging System
**Priority**: P2  
**Component**: Backend/DevOps  
**Estimate**: 4 days

**Description**:
Implement comprehensive monitoring and structured logging.

**Requirements**:
- Structured JSON logging
- Log aggregation (ELK stack or similar)
- Error tracking (Sentry)
- Performance monitoring (APM)
- Uptime monitoring
- Alert system
- Log retention policy

**Dependencies**: None  
**Blocks**: None

---

### ISSUE #35: Pydantic v2 Migration
**Priority**: P1  
**Component**: Backend  
**Estimate**: 3 days

**Description**:
Complete migration to Pydantic v2 to fix failing tests.

**Requirements**:
- Update all schema files to use ConfigDict
- Replace `.dict()` with `.model_dump()`
- Replace `.parse_obj()` with `.model_validate()`
- Update `Optional` field handling
- Fix circular import issues
- Update all tests
- Ensure 38/38 tests passing

**Dependencies**: None  
**Blocks**: Multiple issues (tests must pass)

---

## 📱 Frontend Technical Debt

### ISSUE #36: State Management Implementation
**Priority**: P1  
**Component**: Frontend  
**Estimate**: 4 days

**Description**:
Implement centralized state management with Pinia.

**Requirements**:
- Install and configure Pinia
- Create stores for:
  - User state
  - Recipes state
  - Batches state
  - Inventory state
  - UI state
- Replace direct API calls with actions
- Implement getters for computed state
- Persist state to localStorage where appropriate

**Dependencies**: None  
**Blocks**: All frontend issues

---

### ISSUE #37: Form Validation Library
**Priority**: P1  
**Component**: Frontend  
**Estimate**: 2 days

**Description**:
Implement consistent form validation across all forms.

**Requirements**:
- Install Vuelidate or VeeValidate
- Create validation rules library
- Standardize error message display
- Add validation to all forms
- Real-time validation feedback
- Accessibility support

**Dependencies**: None  
**Blocks**: All form-based issues

---

### ISSUE #38: Error Handling Patterns
**Priority**: P1  
**Component**: Frontend  
**Estimate**: 3 days

**Description**:
Standardize error handling and user feedback.

**Requirements**:
- Global error handler
- API error interceptor
- Toast notification system
- Error boundary components
- User-friendly error messages
- Retry mechanisms
- Offline detection

**Dependencies**: None  
**Blocks**: None

---

### ISSUE #39: Loading States & Skeleton Screens
**Priority**: P2  
**Component**: Frontend  
**Estimate**: 2 days

**Description**:
Implement consistent loading states across the application.

**Requirements**:
- Skeleton screen components
- Loading spinner component
- Progress indicators
- Optimistic UI updates
- Loading state management
- Timeout handling

**Dependencies**: None  
**Blocks**: None

---

### ISSUE #40: TypeScript Strict Mode
**Priority**: P2  
**Component**: Frontend  
**Estimate**: 5 days

**Description**:
Enable TypeScript strict mode and fix all type errors.

**Requirements**:
- Enable strict mode in tsconfig.json
- Add types for all API responses
- Fix implicit any errors
- Add proper null checks
- Type all component props
- Create shared type definitions

**Dependencies**: None  
**Blocks**: None

---

## 📝 Documentation Issues

### ISSUE #41: User Manual
**Priority**: P2  
**Component**: Documentation  
**Estimate**: 5 days

**Description**:
Create comprehensive user manual for end users.

**Requirements**:
- Getting started guide
- Recipe creation tutorial
- Batch tracking guide
- Inventory management guide
- Calculators usage
- Troubleshooting section
- FAQ
- Video tutorials (optional)

**Dependencies**: All user-facing features  
**Blocks**: None

---

### ISSUE #42: API Documentation
**Priority**: P1  
**Component**: Documentation  
**Estimate**: 3 days

**Description**:
Complete and enhance API documentation.

**Requirements**:
- Complete README_API.md
- Swagger/OpenAPI annotations
- Example requests/responses
- Authentication documentation
- Error code reference
- Rate limiting documentation
- Webhook documentation (if applicable)

**Dependencies**: All API endpoints  
**Blocks**: None

---

### ISSUE #43: Architecture Documentation
**Priority**: P2  
**Component**: Documentation  
**Estimate**: 4 days

**Description**:
Document system architecture and design decisions.

**Requirements**:
- System architecture diagram
- Database ER diagram
- Frontend component hierarchy
- API architecture
- Deployment architecture
- Technology stack documentation
- Design decision records (ADRs)

**Dependencies**: None  
**Blocks**: None

---

### ISSUE #44: Developer Onboarding Guide
**Priority**: P2  
**Component**: Documentation  
**Estimate**: 3 days

**Description**:
Create comprehensive developer onboarding documentation.

**Requirements**:
- Development environment setup
- Code structure overview
- Coding standards and conventions
- Git workflow
- Testing guide
- Deployment process
- Contributing guidelines (expand CONTRIBUTING.md)
- Troubleshooting common issues

**Dependencies**: None  
**Blocks**: None

---

## 🧪 Testing Issues

### ISSUE #45: Frontend Test Suite
**Priority**: P1  
**Component**: Frontend/Testing  
**Estimate**: 8 days

**Description**:
Implement comprehensive frontend testing.

**Requirements**:
- Setup Vitest (already configured)
- Component unit tests
- Integration tests
- E2E tests with Playwright
- Visual regression tests
- Accessibility tests
- Test coverage >70%
- CI integration

**Dependencies**: All frontend features  
**Blocks**: None

---

### ISSUE #46: Backend Test Coverage
**Priority**: P1  
**Component**: Backend/Testing  
**Estimate**: 5 days

**Description**:
Increase backend test coverage to 80%+.

**Requirements**:
- Add missing endpoint tests
- Add business logic tests
- Add database model tests
- Add edge case tests
- Add integration tests
- Test fixtures improvement
- Coverage reporting

**Dependencies**: #35 (Pydantic migration)  
**Blocks**: None

---

### ISSUE #47: Performance Testing
**Priority**: P2  
**Component**: Backend/Testing  
**Estimate**: 3 days

**Description**:
Implement performance testing and benchmarking.

**Requirements**:
- Load testing with Locust
- API response time benchmarks
- Database query optimization
- N+1 query detection
- Memory leak detection
- Performance regression tests

**Dependencies**: None  
**Blocks**: None

---

## 🚀 DevOps & Deployment

### ISSUE #48: CI/CD Pipeline Enhancement
**Priority**: P1  
**Component**: DevOps  
**Estimate**: 4 days

**Description**:
Enhance CI/CD pipeline for automated testing and deployment.

**Requirements**:
- Automated testing on PR
- Code quality checks (linting, formatting)
- Security scanning
- Automated deployment to staging
- Manual approval for production
- Rollback capability
- Deployment notifications

**Dependencies**: #45, #46 (test suites)  
**Blocks**: None

---

### ISSUE #49: Production Deployment Setup
**Priority**: P1  
**Component**: DevOps  
**Estimate**: 5 days

**Description**:
Setup production-ready deployment infrastructure.

**Requirements**:
- Docker compose for production
- Reverse proxy (Nginx)
- SSL/TLS certificates
- Environment variable management
- Database migration strategy
- Backup strategy
- Monitoring setup
- Log aggregation

**Dependencies**: #30, #31, #32, #34  
**Blocks**: Production launch

---

### ISSUE #50: Performance Optimization
**Priority**: P2  
**Component**: Backend + Frontend  
**Estimate**: 5 days

**Description**:
Optimize application performance for production use.

**Requirements**:
- Database indexing optimization
- Query optimization
- API response caching
- Frontend bundle optimization
- Lazy loading
- Image optimization
- CDN setup
- Connection pooling

**Dependencies**: None  
**Blocks**: None

---

## 📊 Issue Summary

**Total Issues**: 50

**By Priority**:
- P0 (Critical): 5 issues - 31 days
- P1 (High): 15 issues - 75 days
- P2 (Medium): 20 issues - 85 days
- P3 (Low): 10 issues - 63 days

**By Component**:
- Backend: 18 issues
- Frontend: 20 issues
- Full Stack: 8 issues
- DevOps: 4 issues

**Estimated Total Effort**: ~254 developer-days

**MVP Estimate** (P0 + Critical P1): ~106 developer-days (5-6 months with 1 developer)

**Complete Product** (P0 + P1): ~181 developer-days (9-10 months with 1 developer)

