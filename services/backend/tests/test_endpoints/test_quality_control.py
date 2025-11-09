import pytest
from datetime import datetime
import Database.Models as models


def create_base_recipe(client, db_session, name="Test Recipe"):
    """Helper to create a recipe for testing"""
    payload = {
        "name": name,
        "version": 1,
        "type": "Ale",
        "brewer": "Tester",
        "batch_size": 20.0,
        "boil_size": 25.0,
        "boil_time": 60,
        "hops": [{"name": "Cascade"}],
        "fermentables": [{"name": "Pale Malt"}],
        "yeasts": [{"name": "Ale Yeast"}],
        "miscs": [{"name": "Irish Moss"}],
    }

    response = client.post("/recipes", json=payload)
    assert response.status_code == 200, response.text

    recipe = db_session.query(models.Recipes).filter(models.Recipes.name == name).one()
    return recipe.id


def create_batch(client, recipe_id):
    """Helper to create a batch for testing"""
    payload = {
        "recipe_id": recipe_id,
        "batch_name": "Test Batch",
        "batch_number": 1,
        "batch_size": 18.5,
        "brewer": "Test Brewer",
        "brew_date": datetime(2024, 1, 1, 12, 0, 0).isoformat(),
    }
    response = client.post("/batches", json=payload)
    assert response.status_code == 200, response.text
    return response.json()


def test_calculate_bjcp_score(client):
    """Test BJCP score calculation"""
    score_input = {
        "aroma": 10.0,
        "appearance": 2.5,
        "flavor": 18.0,
        "mouthfeel": 4.0,
        "overall_impression": 8.0,
    }
    
    response = client.post("/bjcp-score", json=score_input)
    assert response.status_code == 200, response.text
    
    result = response.json()
    assert result["total_score"] == 42.5
    assert result["rating"] == "Excellent"  # 38-44 range
    assert result["aroma"] == 10.0
    assert result["appearance"] == 2.5
    assert result["flavor"] == 18.0
    assert result["mouthfeel"] == 4.0
    assert result["overall_impression"] == 8.0


def test_calculate_bjcp_score_outstanding(client):
    """Test BJCP score calculation for outstanding rating"""
    score_input = {
        "aroma": 11.5,
        "appearance": 3.0,
        "flavor": 19.5,
        "mouthfeel": 5.0,
        "overall_impression": 9.5,
    }
    
    response = client.post("/bjcp-score", json=score_input)
    assert response.status_code == 200
    
    result = response.json()
    assert result["total_score"] == 48.5
    assert result["rating"] == "Outstanding"  # 45-50 range


def test_create_quality_control_test(client, db_session):
    """Test creating a quality control test"""
    # Create a batch first
    recipe_id = create_base_recipe(client, db_session)
    batch = create_batch(client, recipe_id)
    
    qc_data = {
        "batch_id": batch["id"],
        "test_date": datetime(2024, 2, 1, 10, 0, 0).isoformat(),
        "final_gravity": 1.012,
        "abv_actual": 5.2,
        "color": "Golden",
        "clarity": "Clear",
        "taste_notes": "Crisp and refreshing with subtle hop notes",
        "score": 42.5,
    }
    
    response = client.post("/quality-control-tests", json=qc_data)
    assert response.status_code == 200, response.text
    
    qc_test = response.json()
    assert qc_test["batch_id"] == batch["id"]
    assert qc_test["final_gravity"] == 1.012
    assert qc_test["abv_actual"] == 5.2
    assert qc_test["color"] == "Golden"
    assert qc_test["clarity"] == "Clear"
    assert qc_test["score"] == 42.5
    assert "id" in qc_test


def test_create_qc_test_batch_not_found(client):
    """Test creating QC test for non-existent batch"""
    qc_data = {
        "batch_id": 99999,
        "test_date": datetime.now().isoformat(),
        "final_gravity": 1.012,
    }
    
    response = client.post("/quality-control-tests", json=qc_data)
    assert response.status_code == 404
    assert "Batch not found" in response.json()["detail"]


def test_get_quality_control_test(client, db_session):
    """Test retrieving a quality control test"""
    recipe_id = create_base_recipe(client, db_session)
    batch = create_batch(client, recipe_id)
    
    # Create QC test
    qc_data = {
        "batch_id": batch["id"],
        "test_date": datetime.now().isoformat(),
        "final_gravity": 1.010,
        "score": 40.0,
    }
    create_response = client.post("/quality-control-tests", json=qc_data)
    qc_test_id = create_response.json()["id"]
    
    # Get QC test
    response = client.get(f"/quality-control-tests/{qc_test_id}")
    assert response.status_code == 200
    
    qc_test = response.json()
    assert qc_test["id"] == qc_test_id
    assert qc_test["final_gravity"] == 1.010


def test_get_batch_quality_control_tests(client, db_session):
    """Test retrieving all QC tests for a batch"""
    recipe_id = create_base_recipe(client, db_session)
    batch = create_batch(client, recipe_id)
    
    # Create multiple QC tests
    for i in range(3):
        qc_data = {
            "batch_id": batch["id"],
            "test_date": datetime(2024, 2, i + 1, 10, 0, 0).isoformat(),
            "score": 40.0 + i,
        }
        client.post("/quality-control-tests", json=qc_data)
    
    # Get all QC tests for batch
    response = client.get(f"/batches/{batch['id']}/quality-control-tests")
    assert response.status_code == 200
    
    qc_tests = response.json()
    assert len(qc_tests) == 3
    # Should be ordered by test_date descending
    assert qc_tests[0]["score"] == 42.0
    assert qc_tests[1]["score"] == 41.0
    assert qc_tests[2]["score"] == 40.0


def test_update_quality_control_test(client, db_session):
    """Test updating a quality control test"""
    recipe_id = create_base_recipe(client, db_session)
    batch = create_batch(client, recipe_id)
    
    # Create QC test
    qc_data = {
        "batch_id": batch["id"],
        "test_date": datetime.now().isoformat(),
        "final_gravity": 1.010,
        "score": 40.0,
    }
    create_response = client.post("/quality-control-tests", json=qc_data)
    qc_test_id = create_response.json()["id"]
    
    # Update QC test
    update_data = {
        "score": 45.0,
        "taste_notes": "Updated notes",
        "clarity": "Brilliant",
    }
    response = client.put(f"/quality-control-tests/{qc_test_id}", json=update_data)
    assert response.status_code == 200
    
    updated_qc = response.json()
    assert updated_qc["score"] == 45.0
    assert updated_qc["taste_notes"] == "Updated notes"
    assert updated_qc["clarity"] == "Brilliant"
    assert updated_qc["final_gravity"] == 1.010  # Unchanged field


def test_delete_quality_control_test(client, db_session):
    """Test deleting a quality control test"""
    recipe_id = create_base_recipe(client, db_session)
    batch = create_batch(client, recipe_id)
    
    # Create QC test
    qc_data = {
        "batch_id": batch["id"],
        "test_date": datetime.now().isoformat(),
        "score": 40.0,
    }
    create_response = client.post("/quality-control-tests", json=qc_data)
    qc_test_id = create_response.json()["id"]
    
    # Delete QC test
    response = client.delete(f"/quality-control-tests/{qc_test_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/quality-control-tests/{qc_test_id}")
    assert get_response.status_code == 404


def test_export_qc_test_pdf(client, db_session):
    """Test exporting QC test as PDF"""
    recipe_id = create_base_recipe(client, db_session)
    batch = create_batch(client, recipe_id)
    
    # Create QC test
    qc_data = {
        "batch_id": batch["id"],
        "test_date": datetime.now().isoformat(),
        "final_gravity": 1.012,
        "abv_actual": 5.2,
        "color": "Golden",
        "clarity": "Clear",
        "taste_notes": "Excellent beer with balanced flavors",
        "score": 45.0,
    }
    create_response = client.post("/quality-control-tests", json=qc_data)
    qc_test_id = create_response.json()["id"]
    
    # Export as PDF
    response = client.get(f"/quality-control-tests/{qc_test_id}/export-pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    assert len(response.content) > 0  # PDF has content


def test_bjcp_score_validation(client):
    """Test BJCP score validation"""
    # Test exceeding max for aroma
    invalid_score = {
        "aroma": 13.0,  # Max is 12
        "appearance": 3.0,
        "flavor": 20.0,
        "mouthfeel": 5.0,
        "overall_impression": 10.0,
    }
    
    response = client.post("/bjcp-score", json=invalid_score)
    assert response.status_code == 422  # Validation error


def test_qc_test_score_validation(client, db_session):
    """Test QC test score validation"""
    recipe_id = create_base_recipe(client, db_session)
    batch = create_batch(client, recipe_id)
    
    # Test score exceeding max
    qc_data = {
        "batch_id": batch["id"],
        "test_date": datetime.now().isoformat(),
        "score": 51.0,  # Max is 50
    }
    
    response = client.post("/quality-control-tests", json=qc_data)
    assert response.status_code == 422  # Validation error
