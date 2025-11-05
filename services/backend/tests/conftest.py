import os

# Set environment variable for testing BEFORE any other imports
os.environ["TESTING"] = "1"

import pytest
import logging
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import all models to ensure they're registered with Base.metadata
import Database.Models  # noqa: F401

# Import database components AFTER setting TESTING env var
from database import Base, get_db, engine as db_engine
from main import app

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Environment variable TESTING set to: {os.environ['TESTING']}")

# Use the same engine that database.py created
engine = db_engine
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    logger.debug("Creating test database tables")
    Base.metadata.create_all(bind=engine)
    yield
    logger.debug("Cleaning test database tables")
    # Instead of dropping tables, just delete all rows
    # This is faster and avoids connection pool issues
    with engine.begin() as connection:
        # For SQLite, disable foreign key checks during cleanup
        if engine.dialect.name == 'sqlite':
            connection.exec_driver_sql('PRAGMA foreign_keys=OFF')
        
        # Delete in reverse topological order to respect foreign keys
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())
        
        # Re-enable foreign key checks for SQLite
        if engine.dialect.name == 'sqlite':
            connection.exec_driver_sql('PRAGMA foreign_keys=ON')


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
