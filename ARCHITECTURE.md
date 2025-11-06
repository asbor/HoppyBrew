# HoppyBrew Architecture Overview

**Last Updated**: November 6, 2025  
**Status**: Active Development

## System Architecture

HoppyBrew is a self-hosted brewing management platform designed for homebrewers. The system follows a modern three-tier architecture with a clear separation between presentation, business logic, and data layers.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  Nuxt 3 + Vue 3 + Shadcn UI Components + TypeScript        │
│                    (Port 3000)                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       Backend Layer                          │
│        FastAPI + SQLAlchemy + Pydantic + Python 3.11        │
│                    (Port 8000)                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SQL
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Database Layer                          │
│              PostgreSQL 16 (Port 5432)                       │
│              SQLite (Testing Only)                           │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: Nuxt 3 (Vue 3 with SSR capabilities)
- **UI Library**: Shadcn-vue (Radix Vue components)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Composables (considering Pinia for complex state)
- **API Client**: Built-in `useFetch` and custom composables

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **Server**: Uvicorn (ASGI server)
- **Authentication**: Planned (JWT-based OAuth2)
- **Documentation**: OpenAPI/Swagger (auto-generated)

### Database
- **Production**: PostgreSQL 16+
- **Testing**: SQLite (in-memory or file-based)
- **Migrations**: Alembic
- **Connection Pooling**: SQLAlchemy default pooling

### DevOps & Infrastructure
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Testing**: pytest (backend), Vitest (frontend - planned)
- **Code Quality**: Black, Flake8 (backend), ESLint (frontend)
- **Monitoring**: Health check endpoints

## Directory Structure

```
HoppyBrew/
├── services/
│   ├── backend/              # FastAPI backend service
│   │   ├── api/
│   │   │   ├── endpoints/    # API route handlers
│   │   │   └── router.py     # Main API router
│   │   ├── Database/
│   │   │   ├── Models/       # SQLAlchemy ORM models
│   │   │   └── Schemas/      # Pydantic schemas
│   │   ├── modules/          # Business logic modules
│   │   ├── tests/            # Backend test suite
│   │   ├── database.py       # Database configuration
│   │   ├── main.py           # FastAPI application
│   │   └── requirements.txt  # Python dependencies
│   │
│   └── nuxt3-shadcn/         # Nuxt 3 frontend service
│       ├── components/       # Vue components
│       ├── composables/      # Vue composables (API clients, state)
│       ├── pages/            # Nuxt pages (auto-routing)
│       ├── public/           # Static assets
│       └── nuxt.config.ts    # Nuxt configuration
│
├── alembic/                  # Database migrations
│   ├── versions/             # Migration scripts
│   └── env.py                # Alembic environment
│
├── seeds/                    # Database seed scripts
│   ├── seed_beer_styles.py   # Seed BJCP styles
│   ├── seed_references.py    # Seed reference data
│   └── seed_all.py           # Master seed script
│
├── documents/                # Project documentation
├── data/                     # Data files (BeerXML, etc.)
├── .github/workflows/        # GitHub Actions CI/CD
├── docker-compose.yml        # Development orchestration
├── .env.example              # Environment template
└── makefile                  # Development commands
```

## Core Domain Models

### Recipes
The foundation of the brewing process. Contains:
- Recipe metadata (name, brewer, style, dates)
- Ingredients (fermentables, hops, yeasts, miscs)
- Process parameters (batch size, efficiency, OG/FG)
- Calculated values (ABV, IBU, SRM color)

### Batches
Production instances of recipes. Tracks:
- Reference to source recipe
- Brew dates and brewer information
- Actual measurements (vs. predicted)
- Production status (planned, brewing, fermenting, etc.)
- Inventory snapshots (ingredients used)

### Inventory
Stock management for ingredients:
- **Fermentables**: Grains, malts, sugars
- **Hops**: Varieties, alpha acids, forms
- **Yeasts**: Strains, temperatures, attenuation
- **Miscs**: Additives, finings, spices

Each type tracks:
- Current stock levels
- Costs (in EUR)
- Suppliers and lot numbers
- Expiration dates

### References & Styles
Supporting data:
- **Style Guidelines**: BJCP style specifications
- **Styles**: Target style profiles for recipes
- **References**: External brewing resources

### Profiles
Configuration entities:
- **Equipment Profiles**: Brew system specifications
- **Mash Profiles**: Temperature step schedules
- **Water Profiles**: Water chemistry targets

## API Design

### RESTful Conventions
All endpoints follow REST principles:
- `GET /resource` - List all
- `GET /resource/{id}` - Get one
- `POST /resource` - Create
- `PUT /resource/{id}` - Update
- `DELETE /resource/{id}` - Delete

### Response Format
Standard JSON responses with consistent structure:
```json
{
  "data": { /* resource or array */ },
  "meta": { "timestamp": "ISO-8601" },
  "errors": [ /* if applicable */ ]
}
```

### Authentication & Authorization
**Current State**: Not implemented  
**Planned**: 
- JWT-based OAuth2 with password flow
- Role-based access control (RBAC)
- User registration and profile management

## Data Flow

### Recipe Creation Flow
1. User designs recipe in frontend
2. Frontend validates inputs and calculates estimates
3. POST request to `/recipes` endpoint
4. Backend validates with Pydantic schemas
5. SQLAlchemy persists to PostgreSQL
6. Response includes calculated values and ID
7. Frontend updates UI with new recipe

### Batch Creation Flow
1. User selects recipe and creates batch
2. POST to `/batches` with recipe ID
3. Backend:
   - Clones recipe with `is_batch=true`
   - Creates batch record linked to clone
   - Copies ingredients to inventory tables
   - Returns batch with all relationships
4. Frontend displays batch details

## Deployment

### Development
```bash
# Start all services
docker-compose up -d

# Backend available at http://localhost:8000
# Frontend available at http://localhost:3000
# Database available at localhost:5432
```

### Production Considerations
- Remove `--reload` from uvicorn in production
- Use proper secrets management (not .env files)
- Enable PostgreSQL SSL connections
- Configure CORS for specific origins
- Set up backup/restore procedures
- Implement rate limiting
- Add logging aggregation

## Testing Strategy

### Backend Testing
- **Unit Tests**: Business logic and utilities
- **Integration Tests**: API endpoints with test database
- **Contract Tests**: Validate request/response schemas
- **Current Coverage**: Partial (expanding)

### Frontend Testing
- **Planned**: Component tests with Vitest
- **Planned**: E2E tests with Playwright
- **Current**: Manual testing only

## Known Technical Debt

### High Priority
- [ ] Implement authentication and authorization
- [ ] Add comprehensive error handling
- [ ] Expand test coverage (backend < 50%)
- [ ] Add frontend test infrastructure

### Medium Priority
- [ ] Implement proper logging/monitoring
- [ ] Add API versioning
- [ ] Optimize database queries (N+1 issues)
- [ ] Add request rate limiting

### Low Priority
- [ ] Add caching layer (Redis)
- [ ] Implement WebSocket for real-time updates
- [ ] Add GraphQL alternative to REST
- [ ] Support multi-tenancy

## Future Enhancements

### Phase 1 (Current)
- Stabilize core CRUD operations
- Fix database relationships
- Improve error handling
- Expand test coverage

### Phase 2
- Implement authentication
- Add batch workflow states
- Fermentation tracking
- Inventory integration with batches

### Phase 3
- BeerXML import/export
- Beer style scraping automation
- Hardware integrations (Tilt, iSpindel)

### Phase 4
- Advanced analytics
- Multi-user collaboration
- Public recipe sharing
- Mobile app (PWA or native)

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Development setup
- Coding standards
- Pull request process
- Testing requirements

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Nuxt 3 Documentation](https://nuxt.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/)
- [BJCP Style Guidelines](https://www.bjcp.org/style/)
