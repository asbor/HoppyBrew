# AI Agent Army Deployment Plan - November 2025

## Executive Summary

The HoppyBrew project has evolved significantly with:
- ✅ Recipe detail pages with 11 components
- ✅ Profile management (equipment, water chemistry)
- ✅ Wiki documentation published
- ✅ Backend code formatted and linted
- ✅ 27 stale branches cleaned up
- ✅ 80 obsolete issues closed (130 → 50)

**Current State**: Strong foundation, ready for coordinated enhancement across all areas.

## New Agents Required

### 1. 🏗️ Architecture & Diagram Agent (PRIORITY: CRITICAL)
**File**: `CODEX_AGENT_ARCHITECTURE.md`

**Mission**: Fix and maintain architectural diagrams
- **Immediate Task**: Issue #348 - Remove order management system from ComponentDiagram-HoppuBrew.puml
- Replace with proper brewing component diagram
- Update all PlantUML diagrams to reflect current architecture
- Ensure diagrams match actual codebase
- Maintain consistency across Architecture.md, Diagram-Catalog.md

**Capabilities**:
- PlantUML diagram generation and validation
- Architecture documentation accuracy verification
- Component relationship mapping
- System context diagram maintenance
- Deployment topology documentation

**Target Files**:
- `documents/docs/plantuml/*.puml`
- `documents/wiki-exports/Architecture.md`
- `documents/wiki-exports/Diagram-Catalog.md`
- `wiki/Architecture.md` (wiki repository)

---

### 2. 📊 Data Model & Schema Agent
**File**: `CODEX_AGENT_DATA_MODEL.md`

**Mission**: Analyze and optimize database schema
- Document all SQLAlchemy models and relationships
- Create ER diagrams for all tables
- Identify missing indexes and constraints
- Suggest normalization improvements
- Document migration strategy

**Capabilities**:
- SQLAlchemy model analysis
- Database schema documentation
- ERD generation with PlantUML
- Index optimization recommendations
- Migration script validation

**Target Files**:
- `services/backend/Database/Models/**/*.py`
- `services/backend/database.py`
- `documents/wiki-exports/Database-Schema.md`

---

### 3. 🎨 Frontend Component Library Agent
**File**: `CODEX_AGENT_COMPONENT_LIBRARY.md`

**Mission**: Organize and document frontend components
- Audit all Vue components (recipe, profile, batch, inventory)
- Create component hierarchy documentation
- Identify reusable component patterns
- Document props, events, and slots
- Create component usage examples

**Capabilities**:
- Vue 3 Composition API analysis
- Component dependency mapping
- Props interface documentation
- Storybook integration planning
- Design system consistency checks

**Target Files**:
- `services/nuxt3-shadcn/components/**/*.vue`
- `services/nuxt3-shadcn/composables/**/*.ts`
- `documents/wiki-exports/Frontend-Guide.md`

---

### 4. 🔌 API Documentation Agent
**File**: `CODEX_AGENT_API_DOCS.md`

**Mission**: Document all REST endpoints
- Generate OpenAPI/Swagger documentation
- Document request/response schemas
- Add endpoint examples with curl commands
- Document authentication requirements
- Create API versioning strategy

**Capabilities**:
- FastAPI endpoint discovery
- OpenAPI schema generation
- Request/response example creation
- Error code documentation
- Rate limiting documentation

**Target Files**:
- `services/backend/api/endpoints/**/*.py`
- `services/backend/main.py`
- `documents/wiki-exports/API-Reference.md`

---

### 5. 🧪 Test Coverage Expansion Agent (UPDATED)
**File**: `CODEX_AGENT_TEST_COVERAGE.md` (existing, needs update)

**Mission**: Achieve 80%+ test coverage
- **Priority**: Recipe components (11 new components)
- **Priority**: Profile endpoints (equipment, water)
- Generate unit tests for all untested modules
- Add integration tests for critical workflows
- Create e2e tests for user journeys

**New Focus Areas**:
- `services/nuxt3-shadcn/components/recipe/*`
- `services/nuxt3-shadcn/pages/profiles/*`
- `services/backend/api/endpoints/equipment.py`
- `services/backend/api/endpoints/water_profiles.py`

---

### 6. 📱 Mobile & Responsive Design Agent
**File**: `CODEX_AGENT_MOBILE_UX.md`

**Mission**: Optimize for mobile brewing workflows
- Audit all pages for mobile responsiveness
- Implement touch-friendly controls
- Optimize bundle size for mobile networks
- Add PWA features (offline support, install prompt)
- Test on actual mobile devices

**Capabilities**:
- Responsive design analysis
- Tailwind breakpoint optimization
- Touch interaction improvements
- PWA manifest generation
- Mobile performance profiling

**Target Files**:
- `services/nuxt3-shadcn/pages/**/*.vue`
- `services/nuxt3-shadcn/layouts/**/*.vue`
- `services/nuxt3-shadcn/app.vue`

---

### 7. 🔄 Brewing Workflow Agent
**File**: `CODEX_AGENT_BREWING_WORKFLOW.md`

**Mission**: Implement end-to-end brewing workflows
- Recipe creation → Batch planning → Brew day → Fermentation → Packaging
- Implement batch state machine
- Add batch timeline visualization
- Create brew day checklists
- Integrate ISpindel telemetry display

**Capabilities**:
- State machine implementation
- Workflow orchestration
- Timeline visualization
- Checklist generation
- Real-time data integration

**Target Files**:
- `services/backend/api/endpoints/batches.py`
- `services/nuxt3-shadcn/pages/batches/**/*.vue`
- New: `services/backend/modules/workflow_engine.py`

---

### 8. 🏠 HomeAssistant Integration Agent
**File**: `CODEX_AGENT_HOMEASSISTANT.md`

**Mission**: Enhance HomeAssistant integration
- Document existing REST sensor endpoints
- Add MQTT discovery support
- Create HomeAssistant dashboard templates
- Implement fermentation alerts
- Add gravity tracking automation

**Capabilities**:
- HomeAssistant YAML generation
- MQTT integration
- REST sensor documentation
- Automation blueprint creation
- Dashboard card configuration

**Target Files**:
- `services/backend/api/endpoints/homeassistant.py`
- `services/backend/modules/homeassistant_mqtt.py` (new)
- `documents/wiki-exports/HomeAssistant-Integration.md` (new)

---

### 9. 📦 Deployment & Operations Agent
**File**: `CODEX_AGENT_DEVOPS.md` (update existing)

**Mission**: Streamline deployment and operations
- Update docker-compose configurations
- Document Unraid deployment
- Add health check endpoints
- Implement log aggregation
- Create monitoring dashboards

**Capabilities**:
- Docker optimization
- CI/CD pipeline enhancement
- Monitoring setup (Prometheus/Grafana)
- Log aggregation (Loki)
- Backup automation

**Target Files**:
- `docker-compose.yml`
- `docker-compose.prod.yml`
- `.github/workflows/*.yml`
- `services/backend/health.py` (new)

---

### 10. 🔐 Security & Compliance Agent
**File**: `CODEX_AGENT_SECURITY.md` (update existing)

**Mission**: Enhance security posture
- Implement authentication/authorization
- Add input validation middleware
- Secure API endpoints
- Document security best practices
- Set up security scanning in CI/CD

**Capabilities**:
- OAuth2/JWT implementation
- RBAC policy definition
- Input sanitization
- Secrets management
- Vulnerability scanning

**Target Files**:
- `services/backend/auth.py` (new)
- `services/backend/middleware/security.py` (new)
- `.github/workflows/security-scan.yml` (new)

---

## Deployment Strategy

### Phase 1: Foundation (Week 1)
**Priority**: CRITICAL agents that unblock others
1. 🏗️ Architecture & Diagram Agent → Fix issue #348
2. 📊 Data Model & Schema Agent → Document current state
3. 🔌 API Documentation Agent → Enable integration work

### Phase 2: Enhancement (Week 2)
**Priority**: HIGH priority feature development
4. 🎨 Frontend Component Library Agent → Organize components
5. 🧪 Test Coverage Expansion Agent → New components/endpoints
6. 📱 Mobile & Responsive Design Agent → Mobile optimization

### Phase 3: Workflows (Week 3)
**Priority**: MEDIUM priority feature completion
7. 🔄 Brewing Workflow Agent → End-to-end flows
8. 🏠 HomeAssistant Integration Agent → Smart home features

### Phase 4: Operations (Week 4)
**Priority**: LOW priority operational excellence
9. 📦 Deployment & Operations Agent → Production readiness
10. 🔐 Security & Compliance Agent → Security hardening

---

## Coordination Rules

### File Ownership Matrix

| Agent | Primary Files | Shared Files |
|-------|--------------|--------------|
| Architecture | `documents/docs/plantuml/` | `wiki/` |
| Data Model | `services/backend/Database/` | `wiki/Database-Schema.md` |
| Frontend Library | `services/nuxt3-shadcn/components/` | `wiki/Frontend-Guide.md` |
| API Docs | `services/backend/api/` | `wiki/API-Reference.md` |
| Test Coverage | `services/backend/tests/` | All test files |
| Mobile UX | `services/nuxt3-shadcn/pages/` | `tailwind.config.js` |
| Brewing Workflow | `services/backend/modules/` | Batch-related files |
| HomeAssistant | `services/backend/api/endpoints/homeassistant.py` | Integration docs |
| DevOps | Docker configs, CI/CD | Deployment docs |
| Security | Auth/middleware | Security docs |

### Coordination Protocol

1. **Before Starting**: Agent reads all active agent contexts
2. **File Modification**: Agent declares intent in its context file
3. **Shared Resources**: Agent checks for conflicts before modifying
4. **Status Updates**: Agent updates context every 2 hours
5. **Completion**: Agent updates coordinator with final status

### Conflict Resolution

- **Priority 1 (CRITICAL)** agents have exclusive access to contested files
- **Priority 2 (HIGH)** agents wait for Priority 1 completion
- **Priority 3 (MEDIUM)** agents queue behind higher priorities
- **Priority 4 (LOW)** agents work on non-contested files only

---

## Success Metrics

### Architecture Agent
- ✅ Issue #348 resolved
- ✅ All PlantUML diagrams reflect current codebase
- ✅ Wiki Architecture.md updated and accurate

### Data Model Agent
- ✅ All models documented with relationships
- ✅ ERD diagrams generated for all tables
- ✅ Index recommendations documented

### Frontend Library Agent
- ✅ Component hierarchy documented
- ✅ All components have prop documentation
- ✅ Reusable patterns identified

### API Docs Agent
- ✅ OpenAPI schema generated
- ✅ All endpoints documented with examples
- ✅ Authentication documented

### Test Coverage Agent
- ✅ Coverage > 80% for backend
- ✅ Coverage > 70% for frontend
- ✅ All new components/endpoints tested

### Mobile UX Agent
- ✅ All pages mobile-responsive
- ✅ PWA manifest configured
- ✅ Mobile performance score > 90

### Brewing Workflow Agent
- ✅ Recipe → Batch workflow implemented
- ✅ Batch state machine working
- ✅ Brew day checklist functional

### HomeAssistant Agent
- ✅ MQTT discovery implemented
- ✅ Dashboard templates created
- ✅ REST sensors documented

### DevOps Agent
- ✅ Production docker-compose ready
- ✅ Health checks implemented
- ✅ Monitoring dashboards deployed

### Security Agent
- ✅ Authentication implemented
- ✅ Input validation middleware active
- ✅ Security scanning in CI/CD

---

## Deployment Commands

```bash
# Deploy Phase 1 agents (Critical)
./scripts/deploy-phase-1-agents.sh

# Check agent status
./scripts/agent-status.sh

# Deploy Phase 2 agents (High priority)
./scripts/deploy-phase-2-agents.sh

# Monitor all agents
watch -n 30 './scripts/agent-status.sh'

# Generate agent progress report
./scripts/puppet-master-report.sh
```

---

## Risk Mitigation

### Risk: Agent Conflicts
**Mitigation**: Strict file ownership matrix, priority-based queueing

### Risk: Incomplete Work
**Mitigation**: 2-hour status updates, 10-minute timeout per task

### Risk: Documentation Drift
**Mitigation**: Wiki Agent validates all documentation changes

### Risk: Test Breakage
**Mitigation**: CI/CD runs on all agent commits, auto-rollback on failure

### Risk: Security Vulnerabilities
**Mitigation**: Security Agent reviews all code changes, automated scanning

---

## Next Steps

1. ✅ Review and approve this deployment plan
2. ⏳ Update existing agent context files with new focus areas
3. ⏳ Create new agent context files for new agents
4. ⏳ Deploy Phase 1 agents (Architecture, Data Model, API Docs)
5. ⏳ Monitor Phase 1 progress and resolve conflicts
6. ⏳ Deploy Phase 2 agents after Phase 1 completion
7. ⏳ Iterate through all phases with continuous monitoring

---

**Status**: 🎯 PLAN READY FOR APPROVAL  
**Created**: 2025-11-08  
**Estimated Completion**: 4 weeks with 10 concurrent agents  
**Expected Impact**: Complete project documentation + 30% feature completion boost
