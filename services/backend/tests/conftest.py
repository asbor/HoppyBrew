import Database.Models
from database import Base, get_db
from main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
import pkgutil
import importlib
import logging
import pytest
import os

# Set environment variable for testing BEFORE any other imports
os.environ["TESTING"] = "1"


# Ensure the model package and its submodules load so Base.metadata sees every table
def _import_all_model_modules(package):
    for _, module_name, _ in pkgutil.walk_packages(
        package.__path__, package.__name__ + "."
    ):
        importlib.import_module(module_name)


_import_all_model_modules(Database.Models)

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Environment variable TESTING set to: {os.environ['TESTING']}")

# Database setup for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
logger.debug(f"SQLALCHEMY_DATABASE_URL set to: {SQLALCHEMY_DATABASE_URL}")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Mock authentication for tests
def override_get_current_active_user():
    """Override get_current_active_user for testing"""
    from Database.Models.users import Users, UserRole
    # Create a mock user for testing
    db = TestingSessionLocal()
    try:
        # Try to get or create test user
        user = db.query(Users).filter(Users.username == "testuser").first()
        if not user:
            user = Users(
                id=1,
                username="testuser",
                email="test@example.com",
                hashed_password="$2b$12$test",
                is_active=True,
                role=UserRole.brewer,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    finally:
        db.close()


# Import auth functions and override them
try:
    from auth import get_current_active_user
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
except ImportError:
    pass


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    logger.debug("Creating test database")
    Base.metadata.create_all(bind=engine)
    yield
    logger.debug("Dropping test database")
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
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


@pytest.fixture()
def sample_batch(client, db_session):
    """Create a sample batch for testing"""
    from Database.Models.recipes import Recipes
    from Database.Models.batches import Batches
    from datetime import datetime

    # Create a recipe first
    recipe = Recipes(
        name="Test IPA",
        version=1,
        type="All Grain",
        brewer="Test Brewer",
        batch_size=20.0,
        boil_size=25.0,
        boil_time=60,
        efficiency=75.0,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)

    # Create a batch
    batch = Batches(
        recipe_id=recipe.id,
        batch_name="Test Batch IPA",
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)

    return {
        "id": batch.id,
        "recipe_id": recipe.id,
        "batch_name": batch.batch_name,
        "batch_number": batch.batch_number,
    }
