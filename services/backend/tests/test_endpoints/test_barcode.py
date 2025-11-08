# tests/test_endpoints/test_barcode.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
import Database.Models as models

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_barcode.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Create tables and clean up after test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_hop(setup_database):
    """Create a sample hop with a barcode"""
    db = TestingSessionLocal()
    hop = models.InventoryHop(
        name="Test Cascade",
        origin="USA",
        alpha=5.5,
        barcode="HOP-001"
    )
    db.add(hop)
    db.commit()
    db.refresh(hop)
    db.close()
    return hop


@pytest.fixture
def sample_fermentable(setup_database):
    """Create a sample fermentable with a barcode"""
    db = TestingSessionLocal()
    fermentable = models.InventoryFermentable(
        name="Test Pilsner Malt",
        type="Grain",
        barcode="FERM-001"
    )
    db.add(fermentable)
    db.commit()
    db.refresh(fermentable)
    db.close()
    return fermentable


def test_lookup_hop_by_barcode(sample_hop):
    """Test looking up a hop by barcode"""
    response = client.get(f"/inventory/barcode/{sample_hop.barcode}")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "hop"
    assert data["item"]["name"] == "Test Cascade"
    assert data["item"]["barcode"] == "HOP-001"


def test_lookup_fermentable_by_barcode(sample_fermentable):
    """Test looking up a fermentable by barcode"""
    response = client.get(f"/inventory/barcode/{sample_fermentable.barcode}")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "fermentable"
    assert data["item"]["name"] == "Test Pilsner Malt"
    assert data["item"]["barcode"] == "FERM-001"


def test_lookup_nonexistent_barcode(setup_database):
    """Test looking up a barcode that doesn't exist"""
    response = client.get("/inventory/barcode/NONEXISTENT")
    assert response.status_code == 404
    assert "No inventory item found" in response.json()["detail"]


def test_update_hop_barcode(sample_hop):
    """Test updating a hop's barcode"""
    new_barcode = "HOP-002"
    response = client.put(
        f"/inventory/hop/{sample_hop.id}/barcode",
        params={"barcode": new_barcode}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["barcode"] == new_barcode

    # Verify the barcode was updated
    lookup_response = client.get(f"/inventory/barcode/{new_barcode}")
    assert lookup_response.status_code == 200


def test_remove_barcode(sample_hop):
    """Test removing a barcode by setting it to null"""
    response = client.put(
        f"/inventory/hop/{sample_hop.id}/barcode",
        params={"barcode": None}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["barcode"] is None


def test_duplicate_barcode_prevention(sample_hop, sample_fermentable):
    """Test that duplicate barcodes are prevented across different inventory types"""
    # Try to set fermentable barcode to same as hop
    response = client.put(
        f"/inventory/fermentable/{sample_fermentable.id}/barcode",
        params={"barcode": sample_hop.barcode}
    )
    assert response.status_code == 400
    assert "already in use" in response.json()["detail"]


def test_update_nonexistent_item(setup_database):
    """Test updating barcode for non-existent item"""
    response = client.put(
        "/inventory/hop/99999/barcode",
        params={"barcode": "TEST"}
    )
    assert response.status_code == 404


def test_invalid_item_type(setup_database):
    """Test updating barcode with invalid item type"""
    response = client.put(
        "/inventory/invalid_type/1/barcode",
        params={"barcode": "TEST"}
    )
    assert response.status_code == 400
    assert "Invalid item_type" in response.json()["detail"]
