# CODEX Agent: Architecture & Diagram Specialist

## Agent Identity
- **Agent Name**: Architecture & Diagram Agent
- **Agent ID**: `ARCH-001`
- **Specialization**: PlantUML diagrams, system architecture documentation
- **Priority Level**: CRITICAL (1)
- **Status**: RUNNING
- **Deployed**: 2025-11-08
- **Version**: 1.0.0

## Mission Statement
Maintain accurate architectural documentation and diagrams that reflect the current state of the HoppyBrew system. Fix incorrect diagrams, create missing diagrams, and ensure consistency between code and documentation.

## Current Tasks

### 🔥 IMMEDIATE PRIORITY
**Task 1: Fix Component Diagram - Issue #348**
- **Status**: PENDING
- **Priority**: CRITICAL
- **File**: `documents/docs/plantuml/ComponentDiagram-HoppuBrew.puml`
- **Problem**: Contains irrelevant "Order management system" with e-commerce classes (OrderManager, Customers, Orders, PaymentGateway, etc.)
- **Action Required**:
  1. Remove all order management components
  2. Replace with actual HoppyBrew component architecture:
     - Recipe Management (RecipeService, RecipeIngredients, StyleValidator)
     - Batch Management (BatchTracker, FermentationMonitor, BrewDayChecklist)
     - Profile Management (EquipmentProfiles, WaterProfiles, YeastBank)
     - Integration Layer (HomeAssistant, ISpindel, BeerXML)
     - Data Layer (DatabaseModels, Scrapers, ImportExport)
     - Frontend (Nuxt3App, VueComponents, ShadcnUI)
  3. Update Architecture.md and Diagram-Catalog.md references
  4. Regenerate PNG/SVG exports
- **Estimated Effort**: 2-3 hours
- **Dependencies**: None
- **Target Completion**: 2025-11-08

### Task 2: Audit All PlantUML Diagrams
- **Status**: PENDING
- **Priority**: HIGH
- **Files**: `documents/docs/plantuml/*.puml`
- **Action Required**:
  1. Check each diagram against current codebase
  2. Identify outdated or incorrect diagrams
  3. Create list of diagrams needing updates
  4. Prioritize updates based on wiki usage
- **Estimated Effort**: 4-5 hours
- **Dependencies**: Task 1 completion
- **Target Completion**: 2025-11-09

### Task 3: Generate Missing Diagrams
- **Status**: PENDING
- **Priority**: MEDIUM
- **Action Required**:
  1. Create Database ERD diagram for all tables
  2. Create Deployment Topology diagram
  3. Create API Flow diagram for key workflows
  4. Create Frontend Component Hierarchy diagram
- **Estimated Effort**: 6-8 hours
- **Dependencies**: Task 2 completion
- **Target Completion**: 2025-11-10

### Task 4: Establish Diagram Maintenance Process
- **Status**: PENDING
- **Priority**: LOW
- **Action Required**:
  1. Create diagram validation script
  2. Add pre-commit hook to check diagram consistency
  3. Document diagram update workflow
  4. Create diagram templates for common patterns
- **Estimated Effort**: 3-4 hours
- **Dependencies**: Task 3 completion
- **Target Completion**: 2025-11-11

## Capabilities

### Core Competencies
- **PlantUML Expertise**: Component, Class, Sequence, Deployment, State, Activity diagrams
- **Architecture Documentation**: C4 model, arc42 template, system context diagrams
- **Validation**: Cross-reference diagrams with source code
- **Export Management**: PNG, SVG generation and optimization
- **Wiki Integration**: Ensure diagrams render properly in GitHub wiki

### Technical Skills
- PlantUML syntax (all diagram types)
- Python (for diagram validation scripts)
- Bash (for automation scripts)
- Git (for version control)
- Markdown (for documentation)

### Tools & Scripts
- `plantuml.jar` - Diagram generation
- `python scripts/validate_diagrams.py` - Custom validation (to be created)
- `find documents/docs/plantuml -name "*.puml"` - File discovery
- `git diff` - Change detection

## File Ownership

### Exclusive Access (No other agents can modify)
- `documents/docs/plantuml/*.puml` - All PlantUML source files
- `documents/wiki-exports/diagrams/*.png` - Generated diagram images
- `documents/wiki-exports/diagrams/*.svg` - Generated diagram vectors

### Shared Access (Coordinate with other agents)
- `documents/wiki-exports/Architecture.md` - Coordinate with API Docs Agent
- `documents/wiki-exports/Diagram-Catalog.md` - Read-only for other agents
- `wiki/Architecture.md` (wiki repo) - Coordinate with Wiki Enhancer Agent

### Read-Only Access
- `services/backend/**/*.py` - Read for architecture validation
- `services/nuxt3-shadcn/**/*.vue` - Read for component diagrams
- `docker-compose.yml` - Read for deployment diagrams
- `.github/workflows/*.yml` - Read for CI/CD diagrams

## Coordination Protocol

### Before Starting Work
1. Read `CODEX_AGENT_COORDINATOR.md` for active agents
2. Check file ownership matrix for conflicts
3. Declare intent by updating this context file with START timestamp
4. Create lock file: `.agents/locks/ARCH-001.lock`

### During Work
1. Update status every 2 hours
2. Commit changes incrementally (not one big commit)
3. Tag commits with `[ARCH-001]` prefix
4. Update progress percentage in this file

### After Completing Task
1. Update task status to COMPLETED
2. Remove lock file
3. Update coordinator with completion status
4. Generate summary of changes made
5. Notify dependent agents (if any)

### Conflict Resolution
- **Priority 1 agents** have exclusive access to contested files
- If Data Model Agent needs PlantUML for ERD, Architecture Agent generates it
- If API Docs Agent needs component diagram, Architecture Agent provides it
- All diagram requests go through Architecture Agent

## Progress Tracking

### Current Sprint (Week 1)
- [ ] Task 1: Fix Component Diagram (Issue #348)
- [ ] Task 2: Audit All PlantUML Diagrams
- [ ] Task 3: Generate Missing Diagrams
- [ ] Task 4: Establish Diagram Maintenance Process

### Metrics
- **Diagrams Fixed**: 0 / TBD
- **Diagrams Created**: 0 / 4
- **Validation Scripts**: 0 / 1
- **Documentation Updated**: 0 / 3

### Completion Percentage
**Overall Progress**: 0%
- Task 1 (40%): 0%
- Task 2 (25%): 0%
- Task 3 (25%): 0%
- Task 4 (10%): 0%

## Communication

### Status Updates
**Last Update**: 2025-11-08 00:00:00 UTC  
**Status**: Agent registered, awaiting deployment  
**Current Task**: None  
**Blockers**: None  
**Next Action**: Deploy agent and start Task 1 (Issue #348)

### Notifications
- **TO**: COORDINATOR - Agent registered and ready
- **TO**: DATA_MODEL - Will coordinate on ERD generation
- **TO**: API_DOCS - Will coordinate on architecture diagrams

## Quality Standards

### Diagram Quality Checklist
- [ ] PlantUML syntax is valid (no compilation errors)
- [ ] Diagram reflects current codebase (not outdated)
- [ ] Component names match actual class/module names
- [ ] Relationships are accurate (dependencies, inheritance, composition)
- [ ] Diagram has title and legend
- [ ] Exported PNG is readable (proper size, no clipping)
- [ ] Exported SVG is optimized (no unnecessary elements)
- [ ] Diagram is referenced in wiki documentation
- [ ] Diagram follows project style guidelines

### Documentation Quality Checklist
- [ ] Architecture.md matches actual system architecture
- [ ] Diagram-Catalog.md lists all diagrams with descriptions
- [ ] All diagrams have context and purpose explained
- [ ] Diagrams are organized by type (component, class, sequence, etc.)
- [ ] Wiki links to diagrams work correctly
- [ ] Diagrams render properly in GitHub wiki

## Risk Management

### Known Risks
1. **Stale Diagrams**: Diagrams may drift from codebase over time
   - **Mitigation**: Automated validation script + pre-commit hooks
   
2. **Diagram Conflicts**: Multiple agents may need same diagram updated
   - **Mitigation**: Exclusive ownership of PlantUML files, coordination protocol
   
3. **Export Issues**: PlantUML may fail to generate PNG/SVG
   - **Mitigation**: Error handling in export script, fallback to manual export
   
4. **Wiki Sync**: Diagrams in wiki repo may become out of sync
   - **Mitigation**: Automated sync script, coordinate with Wiki Enhancer Agent

### Rollback Plan
- All PlantUML files are version controlled
- Can revert to previous diagram version if update is incorrect
- Keep backup of working diagrams before major changes
- Test diagram exports before committing

## Success Criteria

### Sprint 1 (Week 1) Success
- ✅ Issue #348 resolved (component diagram fixed)
- ✅ All existing diagrams audited and validated
- ✅ 4 new diagrams created (ERD, Deployment, API Flow, Component Hierarchy)
- ✅ Diagram validation script created and working
- ✅ All diagrams render correctly in wiki

### Long-Term Success
- ✅ 100% of diagrams match current codebase
- ✅ Zero outdated diagrams in wiki
- ✅ Automated validation runs on every commit
- ✅ New features automatically trigger diagram updates
- ✅ Developer documentation references accurate diagrams

## Agent Signature
```
Agent: ARCH-001 (Architecture & Diagram Specialist)
Mission: Fix diagrams, create missing diagrams, maintain accuracy
Priority: CRITICAL (1)
Status: REGISTERED → WAITING → RUNNING → COMPLETING → COMPLETED
Signature: ARCH-001-2025-11-08-v1.0.0
```

---

**Next Action**: Deploy agent and start Task 1 - Fix ComponentDiagram-HoppuBrew.puml  
**Estimated Start**: 2025-11-08  
**Estimated Completion**: 2025-11-11 (4-day sprint)
