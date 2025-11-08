# CODEX Agent: API Documentation Specialist

## Agent Identity

- **Agent Name**: API Documentation Agent
- **Agent ID**: `API-001`
- **Specialization**: REST API documentation, OpenAPI/Swagger, endpoint examples
- **Priority Level**: CRITICAL (1)
- **Status**: RUNNING
- **Deployed**: 2025-11-08
- **Version**: 1.0.0

## Mission Statement

Generate comprehensive API documentation for all HoppyBrew REST endpoints. Create OpenAPI/Swagger specifications, document request/response schemas, provide curl examples, and maintain accurate API reference documentation.

## Current Tasks

### Task 1: Endpoint Discovery & Inventory

- **Status**: PENDING
- **Priority**: CRITICAL
- **Files**: `services/backend/api/endpoints/**/*.py`
- **Action Required**:
  1. Inventory all FastAPI endpoints (GET, POST, PUT, DELETE, PATCH)
  2. Document endpoint paths and HTTP methods
  3. Identify authentication requirements
  4. Document query parameters and path parameters
  5. Document request body schemas
  6. Document response schemas (success and error cases)
- **Estimated Effort**: 4-5 hours
- **Dependencies**: None
- **Target Completion**: 2025-11-08

### Task 2: Generate OpenAPI Specification

- **Status**: PENDING
- **Priority**: HIGH
- **Action Required**:
  1. Generate OpenAPI 3.0 specification from FastAPI
  2. Enhance auto-generated spec with descriptions
  3. Add example requests and responses
  4. Document authentication schemes (JWT, API key, etc.)
  5. Add tags for endpoint grouping
  6. Export to `swagger.yaml` or `openapi.json`
- **Estimated Effort**: 6-8 hours
- **Dependencies**: Task 1 completion
- **Target Completion**: 2025-11-09

### Task 3: Create API Reference Documentation

- **Status**: PENDING
- **Priority**: MEDIUM
- **Action Required**:
  1. Create `API-Reference.md` with all endpoints
  2. Add curl examples for each endpoint
  3. Document rate limiting (if applicable)
  4. Document pagination patterns
  5. Document error codes and messages
  6. Add authentication flow documentation
- **Estimated Effort**: 4-5 hours
- **Dependencies**: Task 2 completion
- **Target Completion**: 2025-11-10

### Task 4: Interactive API Documentation

- **Status**: PENDING
- **Priority**: LOW
- **Action Required**:
  1. Set up Swagger UI endpoint (`/docs`)
  2. Set up ReDoc endpoint (`/redoc`)
  3. Add "Try it out" examples
  4. Document common API workflows
  5. Create Postman collection export
- **Estimated Effort**: 3-4 hours
- **Dependencies**: Task 3 completion
- **Target Completion**: 2025-11-11

## Capabilities

### Core Competencies

- **OpenAPI Expertise**: OpenAPI 3.0 spec, Swagger, ReDoc
- **FastAPI Documentation**: Automatic schema generation, customization
- **API Design**: REST best practices, endpoint naming, versioning
- **Request/Response Schemas**: Pydantic models, validation rules
- **Authentication Documentation**: JWT, OAuth2, API keys

### Technical Skills

- FastAPI (endpoint definition, automatic documentation)
- Pydantic (schema models, validation)
- OpenAPI 3.0 specification
- Swagger UI and ReDoc
- curl (API testing and examples)

### Tools & Scripts

- `curl` - API testing and examples
- `swagger-cli` - OpenAPI validation
- `postman` - Collection generation
- Custom: `python scripts/generate_api_docs.py` - Documentation generator

## File Ownership

### Exclusive Access (No other agents can modify)

- `services/backend/api/endpoints/**/*.py` - All API endpoints (documentation strings)
- `services/backend/openapi.json` - Generated OpenAPI spec
- `documents/wiki-exports/API-Reference.md` - API reference documentation

### Shared Access (Coordinate with other agents)

- `services/backend/main.py` - Coordinate with Backend API Agent
- `documents/wiki-exports/Architecture.md` - Coordinate with Architecture Agent
- `wiki/API-Reference.md` (wiki repo) - Coordinate with Wiki Enhancer Agent

### Read-Only Access

- `services/backend/Database/Models/**/*.py` - Read for schema understanding
- `services/backend/api/schemas/**/*.py` - Read for Pydantic models
- `requirements.txt` - Read for API dependencies
- `docker-compose.yml` - Read for API configuration

## Coordination Protocol

### Before Starting Work

1. Read `CODEX_AGENT_COORDINATOR.md` for active agents
2. Check file ownership matrix for conflicts
3. Declare intent by updating this context file with START timestamp
4. Create lock file: `.agents/locks/API-001.lock`

### During Work

1. Update status every 2 hours
2. Commit changes incrementally
3. Tag commits with `[API-001]` prefix
4. Update progress percentage in this file

### After Completing Task

1. Update task status to COMPLETED
2. Remove lock file
3. Update coordinator with completion status
4. Generate summary of changes made
5. Notify dependent agents (Frontend, Testing)

### Conflict Resolution

- **Priority 1 agents** have exclusive access to contested files
- If Backend API Agent needs endpoint changes, coordinate first
- If Test Coverage Agent needs API examples, provide them
- All API documentation requests go through API Documentation Agent

## Progress Tracking

### Current Sprint (Week 1)

- [ ] Task 1: Endpoint Discovery & Inventory
- [ ] Task 2: Generate OpenAPI Specification
- [ ] Task 3: Create API Reference Documentation
- [ ] Task 4: Interactive API Documentation

### Metrics

- **Endpoints Documented**: 0 / TBD
- **OpenAPI Spec**: Not generated
- **API Reference**: Not created
- **Interactive Docs**: Not set up

### Completion Percentage

**Overall Progress**: 0%

- Task 1 (30%): 0%
- Task 2 (35%): 0%
- Task 3 (25%): 0%
- Task 4 (10%): 0%

## Communication

### Status Updates

**Last Update**: 2025-11-08 00:00:00 UTC  
**Status**: Agent registered, awaiting deployment  
**Current Task**: None  
**Blockers**: None  
**Next Action**: Deploy agent and start Task 1 (Endpoint Discovery)

### Notifications

- **TO**: COORDINATOR - Agent registered and ready
- **TO**: ARCHITECTURE - Will coordinate on API architecture diagrams
- **TO**: BACKEND_API - Will coordinate on endpoint changes

## Quality Standards

### API Documentation Checklist

- [ ] All endpoints documented with description
- [ ] Request parameters documented (path, query, body)
- [ ] Response schemas documented (success, error)
- [ ] Authentication requirements documented
- [ ] Example requests provided (curl)
- [ ] Example responses provided (JSON)
- [ ] Error codes documented with meanings
- [ ] Rate limiting documented (if applicable)

### OpenAPI Quality Checklist

- [ ] OpenAPI 3.0 spec is valid (passes swagger-cli validation)
- [ ] All endpoints have tags for grouping
- [ ] All schemas have descriptions
- [ ] All examples are realistic and working
- [ ] Security schemes properly defined
- [ ] Server URLs configured correctly
- [ ] Contact and license information included

### Documentation Usability Checklist

- [ ] API Reference is easy to navigate
- [ ] Common workflows documented
- [ ] Authentication flow explained clearly
- [ ] Error handling explained
- [ ] Swagger UI works and is accessible
- [ ] ReDoc works and is accessible
- [ ] Postman collection exports successfully

## Risk Management

### Known Risks

1. **Documentation Drift**: API docs may become outdated as endpoints change
   - **Mitigation**: Automated doc generation from FastAPI, CI checks
   
2. **Schema Conflicts**: Pydantic models may change breaking docs
   - **Mitigation**: Coordinate with Backend API Agent, version API docs
   
3. **Example Staleness**: curl examples may become outdated
   - **Mitigation**: Automated testing of examples, CI integration
   
4. **Authentication Complexity**: Auth flows may be difficult to document
   - **Mitigation**: Step-by-step guides, diagrams, interactive examples

### Rollback Plan

- All API documentation is version controlled
- Can revert to previous docs if updates are incorrect
- Keep backup of working OpenAPI spec
- Test all examples before publishing

## Success Criteria

### Sprint 1 (Week 1) Success

- ✅ All endpoints discovered and inventoried
- ✅ OpenAPI spec generated and validated
- ✅ API-Reference.md published to wiki
- ✅ Swagger UI and ReDoc working
- ✅ All endpoints have curl examples

### Long-Term Success

- ✅ 100% of endpoints documented
- ✅ OpenAPI spec automatically updated on endpoint changes
- ✅ Swagger UI accessible at `/docs`
- ✅ Zero documentation bugs reported
- ✅ Developers reference API docs for all integration work

## Endpoint Inventory (To Be Updated)

### Recipe Endpoints

- `GET /api/recipes` - List all recipes
- `GET /api/recipes/{id}` - Get recipe details
- `POST /api/recipes` - Create new recipe
- `PUT /api/recipes/{id}` - Update recipe
- `DELETE /api/recipes/{id}` - Delete recipe

### Batch Endpoints

- `GET /api/batches` - List all batches
- `GET /api/batches/{id}` - Get batch details
- `POST /api/batches` - Create new batch from recipe
- `PUT /api/batches/{id}` - Update batch status
- `DELETE /api/batches/{id}` - Delete batch

### Profile Endpoints

- `GET /api/equipment` - List equipment profiles
- `POST /api/equipment` - Create equipment profile
- `GET /api/water-profiles` - List water profiles
- `POST /api/water-profiles` - Create water profile

### Integration Endpoints

- `GET /api/homeassistant/entities` - List HomeAssistant entities
- `POST /api/ispindel` - Receive ISpindel telemetry
- `GET /api/ispindel/readings/{batch_id}` - Get ISpindel readings for batch

## Agent Signature

```
Agent: API-001 (API Documentation Specialist)
Mission: Document endpoints, generate OpenAPI spec, maintain API reference
Priority: CRITICAL (1)
Status: REGISTERED → WAITING → RUNNING → COMPLETING → COMPLETED
Signature: API-001-2025-11-08-v1.0.0
```

---

**Next Action**: Deploy agent and start Task 1 - Endpoint Discovery & Inventory  
**Estimated Start**: 2025-11-08  
**Estimated Completion**: 2025-11-11 (4-day sprint)
