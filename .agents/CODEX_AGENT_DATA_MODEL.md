# CODEX Agent: Data Model & Schema Specialist

## Agent Identity
- **Agent Name**: Data Model & Schema Agent
- **Agent ID**: `DATA-001`
- **Specialization**: Database schema, SQLAlchemy models, ERD diagrams
- **Priority Level**: CRITICAL (1)
- **Status**: RUNNING
- **Deployed**: 2025-11-08
- **Version**: 1.0.0

## Mission Statement
Document and optimize the HoppyBrew database schema. Create comprehensive Entity-Relationship Diagrams (ERDs), identify performance optimization opportunities, and maintain accurate model documentation.

## Current Tasks

### Task 1: Database Model Audit
- **Status**: PENDING
- **Priority**: CRITICAL
- **Files**: `services/backend/Database/Models/**/*.py`
- **Action Required**:
  1. Inventory all SQLAlchemy models (Recipe, Batch, Equipment, WaterProfile, etc.)
  2. Document table relationships (one-to-many, many-to-many, foreign keys)
  3. Identify missing indexes on frequently queried columns
  4. Document model attributes, data types, constraints
  5. Check for normalization issues
- **Estimated Effort**: 4-5 hours
- **Dependencies**: None
- **Target Completion**: 2025-11-08

### Task 2: Generate ERD Diagrams
- **Status**: PENDING
- **Priority**: HIGH
- **Action Required**:
  1. Create master ERD showing all tables and relationships
  2. Create domain-specific ERDs:
     - Recipe Domain (recipes, ingredients, styles, fermentables, hops)
     - Batch Domain (batches, brew_sessions, fermentation_logs)
     - Profile Domain (equipment, water_profiles, yeast_bank)
     - User Domain (users, preferences, sessions)
  3. Use PlantUML for ERD generation
  4. Coordinate with Architecture Agent for PlantUML expertise
- **Estimated Effort**: 6-8 hours
- **Dependencies**: Task 1 completion, Architecture Agent assistance
- **Target Completion**: 2025-11-09

### Task 3: Index Optimization Analysis
- **Status**: PENDING
- **Priority**: MEDIUM
- **Action Required**:
  1. Analyze slow queries from logs
  2. Identify missing indexes on frequently queried columns
  3. Recommend composite indexes for common query patterns
  4. Document index strategy in Database-Schema.md
  5. Create migration scripts for new indexes
- **Estimated Effort**: 4-5 hours
- **Dependencies**: Task 1 completion
- **Target Completion**: 2025-11-10

### Task 4: Migration Strategy Documentation
- **Status**: PENDING
- **Priority**: LOW
- **Action Required**:
  1. Document current migration approach (Alembic if used, or manual)
  2. Create migration templates for common scenarios
  3. Document rollback procedures
  4. Create testing checklist for migrations
- **Estimated Effort**: 3-4 hours
- **Dependencies**: Task 3 completion
- **Target Completion**: 2025-11-11

## Capabilities

### Core Competencies
- **SQLAlchemy Expertise**: Models, relationships, queries, migrations
- **Database Design**: Normalization, denormalization, indexing strategies
- **ERD Generation**: PlantUML entity diagrams, relationship mapping
- **Performance Analysis**: Query optimization, index tuning, N+1 query detection
- **Schema Validation**: Foreign key constraints, data type validation

### Technical Skills
- SQLAlchemy ORM (declarative models)
- PostgreSQL (advanced features: JSONB, full-text search)
- Alembic (migrations if applicable)
- PlantUML (entity relationship diagrams)
- Python (model analysis scripts)

### Tools & Scripts
- `python services/backend/database.py` - Database initialization
- `psql` - Direct database inspection
- `alembic` - Migrations (if used)
- Custom: `python scripts/analyze_models.py` - Model relationship analyzer

## File Ownership

### Exclusive Access (No other agents can modify)
- `services/backend/Database/Models/**/*.py` - All SQLAlchemy models
- `services/backend/Database/database.db` - SQLite database (if applicable)
- `documents/wiki-exports/Database-Schema.md` - Schema documentation

### Shared Access (Coordinate with other agents)
- `services/backend/database.py` - Coordinate with Backend API Agent
- `documents/docs/plantuml/ERD-*.puml` - Coordinate with Architecture Agent
- `wiki/Database-Schema.md` (wiki repo) - Coordinate with Wiki Enhancer Agent

### Read-Only Access
- `services/backend/api/endpoints/**/*.py` - Read for query pattern analysis
- `services/backend/main.py` - Read for database initialization
- `docker-compose.yml` - Read for database configuration
- `requirements.txt` - Read for database dependencies

## Coordination Protocol

### Before Starting Work
1. Read `CODEX_AGENT_COORDINATOR.md` for active agents
2. Check file ownership matrix for conflicts
3. Declare intent by updating this context file with START timestamp
4. Create lock file: `.agents/locks/DATA-001.lock`

### During Work
1. Update status every 2 hours
2. Commit changes incrementally
3. Tag commits with `[DATA-001]` prefix
4. Update progress percentage in this file

### After Completing Task
1. Update task status to COMPLETED
2. Remove lock file
3. Update coordinator with completion status
4. Generate summary of changes made
5. Notify dependent agents (Backend API, Test Coverage)

### Conflict Resolution
- **Priority 1 agents** have exclusive access to contested files
- If Backend API Agent needs model changes, coordinate first
- If Test Coverage Agent needs test data, provide fixtures
- All ERD generation requests go through Architecture Agent

## Progress Tracking

### Current Sprint (Week 1)
- [ ] Task 1: Database Model Audit
- [ ] Task 2: Generate ERD Diagrams
- [ ] Task 3: Index Optimization Analysis
- [ ] Task 4: Migration Strategy Documentation

### Metrics
- **Models Documented**: 0 / TBD
- **ERDs Created**: 0 / 5
- **Indexes Recommended**: 0 / TBD
- **Migrations Created**: 0 / TBD

### Completion Percentage
**Overall Progress**: 0%
- Task 1 (35%): 0%
- Task 2 (35%): 0%
- Task 3 (20%): 0%
- Task 4 (10%): 0%

## Communication

### Status Updates
**Last Update**: 2025-11-08 00:00:00 UTC  
**Status**: Agent registered, awaiting deployment  
**Current Task**: None  
**Blockers**: None  
**Next Action**: Deploy agent and start Task 1 (Model Audit)

### Notifications
- **TO**: COORDINATOR - Agent registered and ready
- **TO**: ARCHITECTURE - Will need PlantUML assistance for ERDs
- **TO**: BACKEND_API - Will coordinate on model changes

## Quality Standards

### Model Documentation Checklist
- [ ] All models have docstrings explaining purpose
- [ ] All relationships documented (type, cascade behavior)
- [ ] All columns have type annotations
- [ ] Constraints documented (unique, nullable, default)
- [ ] Indexes documented with rationale
- [ ] Foreign keys documented with target table
- [ ] Validation logic documented

### ERD Quality Checklist
- [ ] All tables represented with correct names
- [ ] All relationships shown with correct cardinality
- [ ] Primary keys marked
- [ ] Foreign keys clearly indicated
- [ ] Relationship names are descriptive
- [ ] Diagram is readable (not too cluttered)
- [ ] Legend explains notation
- [ ] Diagram follows project PlantUML style

### Performance Checklist
- [ ] Frequently queried columns have indexes
- [ ] Composite indexes for multi-column queries
- [ ] No N+1 query patterns in common workflows
- [ ] Lazy loading vs. eager loading optimized
- [ ] Query patterns documented in schema docs

## Risk Management

### Known Risks
1. **Schema Migration Conflicts**: Multiple agents may need schema changes
   - **Mitigation**: Exclusive ownership of model files, coordination protocol
   
2. **Index Overhead**: Too many indexes slow down writes
   - **Mitigation**: Benchmark before/after, only add indexes with proven benefit
   
3. **Breaking Changes**: Model changes may break existing code
   - **Mitigation**: Deprecation warnings, coordinate with Backend API Agent
   
4. **Data Loss**: Migrations may fail or lose data
   - **Mitigation**: Always test migrations on copy of database, backup before migration

### Rollback Plan
- All model files are version controlled
- Can revert to previous schema if migration fails
- Keep SQL dumps before major migrations
- Test rollback procedures before production deployment

## Success Criteria

### Sprint 1 (Week 1) Success
- ✅ All database models documented with relationships
- ✅ 5 ERD diagrams created (master + 4 domain-specific)
- ✅ Index optimization recommendations documented
- ✅ Migration strategy documented
- ✅ Database-Schema.md published to wiki

### Long-Term Success
- ✅ 100% of models have comprehensive documentation
- ✅ ERDs automatically updated when schema changes
- ✅ Query performance improved by 30%+ from index optimization
- ✅ Zero failed migrations in production
- ✅ Developers reference schema docs for all database work

## Model Inventory (To Be Updated)

### Recipe Domain
- `Recipe` - Master recipe with name, style, OG, FG, IBU, SRM, ABV
- `RecipeIngredient` - Polymorphic association (fermentable, hop, yeast, misc)
- `Fermentable` - Grain, extract, sugar additions
- `Hop` - Hop varieties with additions and timing
- `Yeast` - Yeast strains with fermentation parameters
- `Style` - BJCP beer style definitions
- `MiscIngredient` - Other additions (spices, clarifiers, etc.)

### Batch Domain
- `Batch` - Brewing batch instance from recipe
- `BrewSession` - Brew day log with timestamps and measurements
- `FermentationLog` - Daily fermentation readings (gravity, temp)
- `BrewNote` - Freeform notes during brewing

### Profile Domain
- `Equipment` - Brewing equipment profiles (mash tun, kettle volumes)
- `WaterProfile` - Water chemistry profiles (minerals, pH)
- `YeastBank` - Personal yeast inventory

### User Domain
- `User` - User accounts (if applicable)
- `UserPreference` - User settings and preferences

### Integration Domain
- `ISpindelReading` - Telemetry from ISpindel devices
- `HomeAssistantEntity` - Entities exposed to HomeAssistant

## Agent Signature
```
Agent: DATA-001 (Data Model & Schema Specialist)
Mission: Document models, create ERDs, optimize schema
Priority: CRITICAL (1)
Status: REGISTERED → WAITING → RUNNING → COMPLETING → COMPLETED
Signature: DATA-001-2025-11-08-v1.0.0
```

---

**Next Action**: Deploy agent and start Task 1 - Database Model Audit  
**Estimated Start**: 2025-11-08  
**Estimated Completion**: 2025-11-11 (4-day sprint)
