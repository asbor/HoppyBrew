"""
API endpoint tests for yeast management features.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
import Database.Models as models

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_yeast_management.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override the get_db dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Setup test database before tests"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Create a fresh database session for each test"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_yeast_strain(db_session):
    """Create a sample yeast strain for testing"""
    strain = models.YeastStrain(
        name="SafAle US-05",
        laboratory="Fermentis",
        product_id="US-05",
        type="Ale",
        form="Dry",
        min_temperature=15.0,
        max_temperature=24.0,
        flocculation="Medium",
        attenuation_min=78.0,
        attenuation_max=82.0,
        alcohol_tolerance=12.0,
        best_for="American Pale Ales and IPAs",
        max_reuse=5,
        viability_days_dry=1095
    )
    db_session.add(strain)
    db_session.commit()
    db_session.refresh(strain)
    return strain


class TestYeastStrainEndpoints:
    """Test yeast strain CRUD endpoints"""

    def test_create_yeast_strain(self):
        """Test creating a new yeast strain"""
        strain_data = {
            "name": "White Labs WLP001",
            "laboratory": "White Labs",
            "product_id": "WLP001",
            "type": "Ale",
            "form": "Liquid",
            "min_temperature": 18.0,
            "max_temperature": 22.0,
            "flocculation": "Medium",
            "attenuation_min": 73.0,
            "attenuation_max": 77.0,
            "alcohol_tolerance": 10.0,
            "best_for": "American ales",
            "max_reuse": 5
        }

        response = client.post("/yeast-strains", json=strain_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == strain_data["name"]
        assert data["laboratory"] == strain_data["laboratory"]
        assert data["product_id"] == strain_data["product_id"]
        assert "id" in data
        assert "created_at" in data

    def test_get_yeast_strains(self, sample_yeast_strain):
        """Test getting all yeast strains"""
        response = client.get("/yeast-strains")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(s["id"] == sample_yeast_strain.id for s in data)

    def test_get_yeast_strain_by_id(self, sample_yeast_strain):
        """Test getting a specific yeast strain"""
        response = client.get(f"/yeast-strains/{sample_yeast_strain.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_yeast_strain.id
        assert data["name"] == sample_yeast_strain.name

    def test_get_nonexistent_yeast_strain(self):
        """Test getting a yeast strain that doesn't exist"""
        response = client.get("/yeast-strains/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_yeast_strain(self, sample_yeast_strain):
        """Test updating a yeast strain"""
        update_data = {
            "notes": "Updated notes for testing",
            "max_reuse": 10
        }

        response = client.put(f"/yeast-strains/{sample_yeast_strain.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["notes"] == update_data["notes"]
        assert data["max_reuse"] == update_data["max_reuse"]
        assert data["name"] == sample_yeast_strain.name  # Unchanged fields remain

    def test_delete_yeast_strain(self, db_session):
        """Test deleting a yeast strain"""
        # Create a strain to delete
        strain = models.YeastStrain(
            name="Test Delete Strain",
            laboratory="Test Lab"
        )
        db_session.add(strain)
        db_session.commit()
        db_session.refresh(strain)
        strain_id = strain.id

        response = client.delete(f"/yeast-strains/{strain_id}")
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()

        # Verify it's deleted
        response = client.get(f"/yeast-strains/{strain_id}")
        assert response.status_code == 404

    def test_filter_yeast_strains_by_laboratory(self, sample_yeast_strain):
        """Test filtering yeast strains by laboratory"""
        response = client.get(f"/yeast-strains?laboratory={sample_yeast_strain.laboratory}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(s["laboratory"] == sample_yeast_strain.laboratory for s in data if s["laboratory"])

    def test_filter_yeast_strains_by_type(self, sample_yeast_strain):
        """Test filtering yeast strains by type"""
        response = client.get(f"/yeast-strains?yeast_type={sample_yeast_strain.type}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1


class TestYeastHarvestEndpoints:
    """Test yeast harvest CRUD endpoints"""

    def test_create_yeast_harvest(self, sample_yeast_strain):
        """Test creating a new yeast harvest"""
        harvest_data = {
            "yeast_strain_id": sample_yeast_strain.id,
            "generation": 1,
            "quantity_harvested": 200.0,
            "unit": "ml",
            "viability_at_harvest": 95.0,
            "storage_method": "refrigerated",
            "storage_temperature": 4.0,
            "status": "active",
            "notes": "Harvested from top cropping"
        }

        response = client.post("/yeast-harvests", json=harvest_data)
        assert response.status_code == 201
        data = response.json()
        assert data["yeast_strain_id"] == harvest_data["yeast_strain_id"]
        assert data["generation"] == harvest_data["generation"]
        assert data["quantity_harvested"] == harvest_data["quantity_harvested"]
        assert "id" in data
        assert "harvest_date" in data

    def test_create_harvest_invalid_strain(self):
        """Test creating a harvest with invalid strain ID"""
        harvest_data = {
            "yeast_strain_id": 99999,
            "generation": 1,
            "quantity_harvested": 200.0,
            "unit": "ml"
        }

        response = client.post("/yeast-harvests", json=harvest_data)
        assert response.status_code == 404
        assert "strain not found" in response.json()["detail"].lower()

    def test_get_yeast_harvests(self, sample_yeast_strain, db_session):
        """Test getting all yeast harvests"""
        # Create a harvest
        harvest = models.YeastHarvest(
            yeast_strain_id=sample_yeast_strain.id,
            generation=1,
            quantity_harvested=200.0,
            unit="ml"
        )
        db_session.add(harvest)
        db_session.commit()

        response = client.get("/yeast-harvests")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_filter_harvests_by_strain(self, sample_yeast_strain, db_session):
        """Test filtering harvests by yeast strain"""
        # Create a harvest
        harvest = models.YeastHarvest(
            yeast_strain_id=sample_yeast_strain.id,
            generation=1,
            quantity_harvested=200.0,
            unit="ml"
        )
        db_session.add(harvest)
        db_session.commit()

        response = client.get(f"/yeast-harvests?yeast_strain_id={sample_yeast_strain.id}")
        assert response.status_code == 200
        data = response.json()
        assert all(h["yeast_strain_id"] == sample_yeast_strain.id for h in data)

    def test_update_harvest_status(self, sample_yeast_strain, db_session):
        """Test updating harvest status"""
        # Create a harvest
        harvest = models.YeastHarvest(
            yeast_strain_id=sample_yeast_strain.id,
            generation=1,
            quantity_harvested=200.0,
            unit="ml",
            status="active"
        )
        db_session.add(harvest)
        db_session.commit()
        db_session.refresh(harvest)

        update_data = {
            "status": "used",
            "notes": "Used in batch #123"
        }

        response = client.put(f"/yeast-harvests/{harvest.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "used"
        assert data["notes"] == update_data["notes"]


class TestViabilityCalculator:
    """Test viability calculator endpoints"""

    def test_calculate_viability_dry_yeast(self):
        """Test viability calculation for dry yeast"""
        calculation_data = {
            "yeast_form": "Dry",
            "manufacture_date": (datetime.now() - timedelta(days=30)).isoformat(),
            "initial_viability": 100.0,
            "storage_temperature": 4.0,
            "generation": 0
        }

        response = client.post("/yeasts/calculate-viability", json=calculation_data)
        assert response.status_code == 200
        data = response.json()
        assert "current_viability" in data
        assert "viability_status" in data
        assert "recommendation" in data
        assert data["current_viability"] >= 99.0  # Fresh dry yeast

    def test_calculate_viability_liquid_yeast(self):
        """Test viability calculation for liquid yeast"""
        calculation_data = {
            "yeast_form": "Liquid",
            "manufacture_date": (datetime.now() - timedelta(days=90)).isoformat(),
            "initial_viability": 100.0,
            "storage_temperature": 4.0,
            "generation": 0
        }

        response = client.post("/yeasts/calculate-viability", json=calculation_data)
        assert response.status_code == 200
        data = response.json()
        assert data["current_viability"] < 100.0  # Some degradation
        assert data["days_since_manufacture"] == 90

    def test_calculate_viability_with_generation(self):
        """Test viability calculation with generation loss"""
        calculation_data = {
            "yeast_form": "Liquid",
            "manufacture_date": (datetime.now() - timedelta(days=30)).isoformat(),
            "initial_viability": 100.0,
            "storage_temperature": 4.0,
            "generation": 3
        }

        response = client.post("/yeasts/calculate-viability", json=calculation_data)
        assert response.status_code == 200
        data = response.json()
        # Should have significant viability loss from generations
        assert data["current_viability"] < 75.0

    def test_calculate_viability_high_temperature(self):
        """Test viability calculation with high storage temperature"""
        calculation_data = {
            "yeast_form": "Liquid",
            "manufacture_date": (datetime.now() - timedelta(days=60)).isoformat(),
            "initial_viability": 100.0,
            "storage_temperature": 20.0,  # Room temperature
            "generation": 0
        }

        response = client.post("/yeasts/calculate-viability", json=calculation_data)
        assert response.status_code == 200
        data = response.json()
        # Higher temperature should cause more degradation
        assert data["current_viability"] < 90.0


class TestHarvestGenealogy:
    """Test harvest genealogy endpoint"""

    def test_get_harvest_genealogy(self, sample_yeast_strain, db_session):
        """Test getting harvest genealogy tree"""
        # Create a parent harvest
        parent = models.YeastHarvest(
            yeast_strain_id=sample_yeast_strain.id,
            generation=1,
            quantity_harvested=200.0,
            unit="ml"
        )
        db_session.add(parent)
        db_session.commit()
        db_session.refresh(parent)

        # Create a child harvest
        child = models.YeastHarvest(
            yeast_strain_id=sample_yeast_strain.id,
            generation=2,
            parent_harvest_id=parent.id,
            quantity_harvested=150.0,
            unit="ml"
        )
        db_session.add(child)
        db_session.commit()
        db_session.refresh(child)

        response = client.get(f"/yeast-harvests/{child.id}/genealogy")
        assert response.status_code == 200
        data = response.json()
        assert "current" in data
        assert "ancestors" in data
        assert "descendants" in data
        assert data["current"]["id"] == child.id
        assert len(data["ancestors"]) == 1
        assert data["ancestors"][0]["id"] == parent.id
