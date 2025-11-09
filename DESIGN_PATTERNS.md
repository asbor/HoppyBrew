# Design Patterns in HoppyBrew

This document describes the design patterns implemented in the HoppyBrew application to improve code quality, maintainability, and performance.

## Overview

The HoppyBrew application uses several design patterns to ensure clean architecture and proper separation of concerns:

1. **Singleton Pattern** - For logger configuration
2. **Lazy Initialization** - For database connections
3. **Dependency Injection** - For database sessions in API endpoints
4. **Context Manager** - For application lifecycle management

## 1. Singleton Pattern (Logger)

### Location
`services/backend/logger_config.py`

### Purpose
Ensures that logging is configured only once, even when the module is imported multiple times.

### Implementation
```python
class LoggerManager:
    """Thread-safe Singleton logger manager"""
    _instance = None
    _lock = threading.Lock()
    _configured = False
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

### Benefits
- **Thread Safety**: Uses double-checked locking pattern
- **No Duplication**: Logger handlers are not duplicated across imports
- **Single Configuration**: Logging is configured once and reused
- **Performance**: Avoids repeated initialization overhead

### Usage
```python
from logger_config import get_logger

logger = get_logger("my_module")
logger.info("This message uses the singleton logger")
```

## 2. Lazy Initialization (Database)

### Location
`services/backend/database.py`

### Purpose
Delays database connection until it's actually needed, avoiding premature initialization during module imports.

### Implementation
```python
class _DatabaseManager:
    """Singleton database manager with lazy initialization"""
    
    def __init__(self):
        self._engine = None
        self._SessionLocal = None
        self._initialized = False
    
    @property
    def engine(self):
        """Get engine, initializing if necessary"""
        if not self._initialized:
            self.initialize()
        return self._engine
```

### Benefits
- **Faster Imports**: Modules can be imported without triggering database connections
- **Better Testing**: Tests can import modules without needing a real database
- **Resource Efficiency**: Database resources are only allocated when needed
- **Cleaner Logs**: No database connection logs during module imports

### Usage
```python
# Import doesn't initialize database
from database import SessionLocal, engine

# First access triggers initialization
session = SessionLocal()  # Database initializes here
```

## 3. Dependency Injection (API Endpoints)

### Location
`services/backend/api/endpoints/*.py`

### Purpose
Provides database sessions to API endpoints in a clean, testable way.

### Implementation
```python
from typing import Annotated
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session

# Define the dependency type
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/items")
async def get_items(db: db_dependency):
    """Endpoint receives database session via dependency injection"""
    return db.query(models.Item).all()
```

### Benefits
- **Testability**: Easy to mock database sessions in tests
- **Resource Management**: Sessions are automatically closed after use
- **Clean Code**: No manual session creation/cleanup in endpoints
- **Separation of Concerns**: Database logic separated from business logic

### Anti-Patterns to Avoid
❌ **Don't do this** (module-level session creation):
```python
# BAD: Creates session at import time
from database import SessionLocal
db = SessionLocal()  # Anti-pattern!
```

✅ **Do this instead** (use dependency injection):
```python
# GOOD: Use dependency injection
from database import get_db
from fastapi import Depends

@router.get("/items")
async def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()
```

## 4. Context Manager (Application Lifecycle)

### Location
`services/backend/main.py`

### Purpose
Manages application startup and shutdown events properly.

### Implementation
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting application")
    initialize_database()
    Base.metadata.create_all(bind=engine)
    
    yield  # Application runs
    
    # Shutdown
    logger.info("Shutting down application")

app = FastAPI(lifespan=lifespan)
```

### Benefits
- **Proper Initialization**: Database and other resources initialized at startup
- **Clean Shutdown**: Resources cleaned up properly on shutdown
- **Lifecycle Hooks**: Clear separation of startup/shutdown logic
- **Better Logging**: Initialization logs appear at appropriate times

## Migration Guide

### Before (Anti-Patterns)

```python
# database.py - OLD (executed at import time)
logger.info("Connecting to database...")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
logger.info("Database ready")

# main.py - OLD
from database import engine, Base
Base.metadata.create_all(bind=engine)  # Executed at import

# styles.py - OLD (anti-pattern)
from database import SessionLocal
db = SessionLocal()  # Module-level session
```

### After (Design Patterns)

```python
# database.py - NEW (lazy initialization)
class _DatabaseManager:
    def initialize(self):
        if not self._initialized:
            logger.info("Initializing database")
            self._engine = create_engine(DATABASE_URL)
            # ... initialization code

# main.py - NEW (lifespan management)
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    initialize_database()
    Base.metadata.create_all(bind=engine)
    yield

# styles.py - NEW (dependency injection)
@router.get("/styles")
async def get_styles(db: Session = Depends(get_db)):
    return db.query(models.Style).all()
```

## Testing

### Example Test
```python
def test_lazy_initialization():
    """Test that database is not initialized on import"""
    import database
    
    # Module imported but database not initialized
    assert not database._db_manager._initialized
    
    # First access triggers initialization
    session = database.SessionLocal()
    assert database._db_manager._initialized
```

## Performance Impact

### Before
- Module imports triggered full database initialization
- Logger configured multiple times on repeated imports
- Resources allocated even when not needed

### After
- Module imports are fast (no initialization)
- Logger configured once (Singleton pattern)
- Resources allocated only when first accessed
- Cleaner logs with appropriate lifecycle events

## Best Practices

1. **Use Lazy Initialization** for expensive resources (database, external APIs)
2. **Use Singleton Pattern** for shared configuration (logging, settings)
3. **Use Dependency Injection** for testable components
4. **Avoid Module-Level Initialization** of stateful objects
5. **Use Context Managers** for lifecycle management

## References

- [Singleton Pattern](https://refactoring.guru/design-patterns/singleton)
- [Lazy Initialization](https://en.wikipedia.org/wiki/Lazy_initialization)
- [Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)

## Changelog

### 2025-11-09
- Implemented Singleton pattern for logger configuration
- Implemented lazy initialization for database connections
- Refactored API endpoints to use dependency injection
- Added lifespan management for proper startup/shutdown
- Removed module-level initialization anti-patterns
