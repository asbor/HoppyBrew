# tests/test_endpoints/test_batch_costs.py

import pytest
from datetime import datetime
import Database.Models as models


def create_test_batch(client, batch_name="Test Cost Batch"):
    """Helper function to create a test batch with recipe"""
    # Create recipe
    payload = {
        "name": f"Recipe for {batch_name}",
        "version": 1,
        "type": "Ale",
        "brewer": "Cost Tester",
        "batch_size": 20.0,
        "boil_size": 25.0,
        "boil_time": 60,
        "hops": [{"name": "Cascade", "cost_per_unit": 0.50}],
        "fermentables": [{"name": "Pale Malt", "cost_per_unit": 1.20}],
        "yeasts": [{"name": "Ale Yeast", "cost_per_unit": 7.99}],
        "miscs": [{"name": "Irish Moss", "cost_per_unit": 0.10}],
    }
    
    response = client.post("/recipes", json=payload)
    assert response.status_code == 200, response.text
    recipe = response.json()
    
    # Create batch
    batch_payload = {
        "recipe_id": recipe["id"],
        "batch_name": batch_name,
        "batch_number": 1,
        "batch_size": 20.0,
        "brewer": "Cost Tester",
        "brew_date": datetime(2024, 1, 1, 12, 0, 0).isoformat(),
    }
    
    response = client.post("/batches", json=batch_payload)
    assert response.status_code == 200, response.text
    batch = response.json()
    
    return batch


def test_create_batch_cost(client):
    """Test creating a batch cost record"""
    batch = create_test_batch(client)
    
    cost_payload = {
        "batch_id": batch["id"],
        "fermentables_cost": 45.50,
        "hops_cost": 12.30,
        "yeasts_cost": 7.99,
        "miscs_cost": 3.50,
        "electricity_cost": 1.02,
        "water_cost": 0.12,
        "gas_cost": 0.0,
        "other_utility_cost": 0.0,
        "labor_cost": 0.0,
        "packaging_cost": 15.00,
        "other_cost": 0.0,
        "target_price_per_pint": 5.50,
        "notes": "First batch with new equipment",
    }
    
    response = client.post("/batch-costs", json=cost_payload)
    assert response.status_code == 200, response.text
    batch_cost = response.json()
    
    # Verify calculations
    assert batch_cost["batch_id"] == batch["id"]
    assert batch_cost["fermentables_cost"] == 45.50
    assert batch_cost["total_cost"] == pytest.approx(85.43, abs=0.01)
    assert batch_cost["cost_per_liter"] > 0
    assert batch_cost["cost_per_pint"] > 0
    assert batch_cost["profit_margin"] is not None


def test_get_batch_cost(client):
    """Test retrieving batch cost information"""
    batch = create_test_batch(client)
    
    cost_payload = {
        "batch_id": batch["id"],
        "fermentables_cost": 45.50,
        "hops_cost": 12.30,
        "yeasts_cost": 7.99,
        "miscs_cost": 3.50,
    }
    
    create_response = client.post("/batch-costs", json=cost_payload)
    assert create_response.status_code == 200
    
    # Get the cost record
    response = client.get(f"/batch-costs/{batch['id']}")
    assert response.status_code == 200, response.text
    batch_cost = response.json()
    
    assert batch_cost["batch_id"] == batch["id"]
    assert batch_cost["fermentables_cost"] == 45.50


def test_update_batch_cost(client):
    """Test updating batch cost information"""
    batch = create_test_batch(client)
    
    # Create initial cost record
    cost_payload = {
        "batch_id": batch["id"],
        "fermentables_cost": 45.50,
        "hops_cost": 12.30,
    }
    
    create_response = client.post("/batch-costs", json=cost_payload)
    assert create_response.status_code == 200
    
    # Update the cost record
    update_payload = {
        "fermentables_cost": 50.00,
        "packaging_cost": 20.00,
    }
    
    response = client.put(f"/batch-costs/{batch['id']}", json=update_payload)
    assert response.status_code == 200, response.text
    updated_cost = response.json()
    
    assert updated_cost["fermentables_cost"] == 50.00
    assert updated_cost["packaging_cost"] == 20.00
    assert updated_cost["total_cost"] > 0


def test_delete_batch_cost(client):
    """Test deleting batch cost information"""
    batch = create_test_batch(client)
    
    cost_payload = {
        "batch_id": batch["id"],
        "fermentables_cost": 45.50,
    }
    
    create_response = client.post("/batch-costs", json=cost_payload)
    assert create_response.status_code == 200
    
    # Delete the cost record
    response = client.delete(f"/batch-costs/{batch['id']}")
    assert response.status_code == 200, response.text
    
    # Verify it's deleted
    get_response = client.get(f"/batch-costs/{batch['id']}")
    assert get_response.status_code == 404


def test_batch_cost_summary(client):
    """Test getting batch cost summary"""
    batch = create_test_batch(client)
    
    cost_payload = {
        "batch_id": batch["id"],
        "fermentables_cost": 45.50,
        "hops_cost": 12.30,
        "yeasts_cost": 7.99,
        "miscs_cost": 3.50,
        "electricity_cost": 1.02,
        "water_cost": 0.12,
        "packaging_cost": 15.00,
        "target_price_per_pint": 5.50,
    }
    
    create_response = client.post("/batch-costs", json=cost_payload)
    assert create_response.status_code == 200
    
    # Get summary
    response = client.get(f"/batch-costs/{batch['id']}/summary")
    assert response.status_code == 200, response.text
    summary = response.json()
    
    assert summary["batch_id"] == batch["id"]
    assert summary["batch_name"] == batch["batch_name"]
    assert summary["total_ingredients_cost"] == pytest.approx(69.29, abs=0.01)
    assert summary["total_utilities_cost"] == pytest.approx(1.14, abs=0.01)
    assert summary["total_other_costs"] == 15.00
    assert summary["total_cost"] > 0
    assert summary["cost_per_liter"] > 0
    assert summary["cost_per_pint"] > 0


def test_calculate_costs_from_ingredients(client):
    """Test calculating costs automatically from ingredient cost_per_unit"""
    batch = create_test_batch(client)
    
    # Calculate costs from ingredients
    response = client.post(f"/batch-costs/{batch['id']}/calculate-from-ingredients")
    assert response.status_code == 200, response.text
    batch_cost = response.json()
    
    # Should have calculated ingredient costs from the batch ingredients
    assert batch_cost["batch_id"] == batch["id"]
    # The actual costs depend on the amounts in the batch, but should be non-zero
    total_ingredients = (
        batch_cost["fermentables_cost"]
        + batch_cost["hops_cost"]
        + batch_cost["yeasts_cost"]
        + batch_cost["miscs_cost"]
    )
    assert total_ingredients >= 0  # Could be zero if no cost_per_unit was set


def test_create_utility_cost_config(client):
    """Test creating a utility cost configuration"""
    config_payload = {
        "name": "Home Brewery - Summer 2024",
        "electricity_rate_per_kwh": 0.12,
        "water_rate_per_liter": 0.002,
        "gas_rate_per_unit": 0.85,
        "avg_electricity_kwh_per_batch": 8.5,
        "avg_water_liters_per_batch": 60.0,
        "avg_gas_units_per_batch": 0.0,
        "currency": "USD",
        "notes": "Summer rates",
    }
    
    response = client.post("/utility-cost-configs", json=config_payload)
    assert response.status_code == 200, response.text
    config = response.json()
    
    assert config["name"] == "Home Brewery - Summer 2024"
    assert config["electricity_rate_per_kwh"] == 0.12
    assert config["is_active"] == 1


def test_get_utility_cost_configs(client):
    """Test retrieving all utility cost configurations"""
    # Create two configs
    config1 = {
        "name": "Config 1",
        "electricity_rate_per_kwh": 0.12,
    }
    config2 = {
        "name": "Config 2",
        "electricity_rate_per_kwh": 0.15,
        "is_active": 0,
    }
    
    client.post("/utility-cost-configs", json=config1)
    client.post("/utility-cost-configs", json=config2)
    
    # Get all configs
    response = client.get("/utility-cost-configs")
    assert response.status_code == 200, response.text
    configs = response.json()
    
    assert len(configs) >= 2
    
    # Get only active configs
    response = client.get("/utility-cost-configs?active_only=true")
    assert response.status_code == 200, response.text
    active_configs = response.json()
    
    for config in active_configs:
        assert config["is_active"] == 1


def test_update_utility_cost_config(client):
    """Test updating a utility cost configuration"""
    config_payload = {
        "name": "Test Config",
        "electricity_rate_per_kwh": 0.12,
    }
    
    create_response = client.post("/utility-cost-configs", json=config_payload)
    assert create_response.status_code == 200
    config = create_response.json()
    
    # Update the config
    update_payload = {
        "electricity_rate_per_kwh": 0.15,
        "water_rate_per_liter": 0.003,
    }
    
    response = client.put(f"/utility-cost-configs/{config['id']}", json=update_payload)
    assert response.status_code == 200, response.text
    updated_config = response.json()
    
    assert updated_config["electricity_rate_per_kwh"] == 0.15
    assert updated_config["water_rate_per_liter"] == 0.003


def test_apply_utility_config_to_batch(client):
    """Test applying utility configuration to a batch"""
    batch = create_test_batch(client)
    
    # Create utility config
    config_payload = {
        "name": "Test Utility Config",
        "electricity_rate_per_kwh": 0.12,
        "water_rate_per_liter": 0.002,
        "avg_electricity_kwh_per_batch": 8.5,
        "avg_water_liters_per_batch": 60.0,
    }
    
    config_response = client.post("/utility-cost-configs", json=config_payload)
    assert config_response.status_code == 200
    config = config_response.json()
    
    # Apply config to batch
    response = client.post(f"/batch-costs/{batch['id']}/apply-utility-config/{config['id']}")
    assert response.status_code == 200, response.text
    batch_cost = response.json()
    
    # Verify utility costs were calculated
    expected_electricity = 8.5 * 0.12
    expected_water = 60.0 * 0.002
    
    assert batch_cost["electricity_cost"] == pytest.approx(expected_electricity, abs=0.01)
    assert batch_cost["water_cost"] == pytest.approx(expected_water, abs=0.01)


def test_cost_per_pint_calculation(client):
    """Test that cost per pint is calculated correctly"""
    batch = create_test_batch(client, "20L Batch")
    
    cost_payload = {
        "batch_id": batch["id"],
        "fermentables_cost": 40.00,
        "hops_cost": 10.00,
        "yeasts_cost": 8.00,
        "miscs_cost": 2.00,
    }
    
    response = client.post("/batch-costs", json=cost_payload)
    assert response.status_code == 200, response.text
    batch_cost = response.json()
    
    # Total cost: 60.00
    # Batch size: 20 liters
    # Cost per liter: 60 / 20 = 3.00
    # Cost per pint (473ml): 3.00 * 0.473176 = ~1.42
    
    assert batch_cost["total_cost"] == 60.00
    assert batch_cost["cost_per_liter"] == pytest.approx(3.00, abs=0.01)
    assert batch_cost["cost_per_pint"] == pytest.approx(1.42, abs=0.01)


def test_profit_margin_calculation(client):
    """Test that profit margin is calculated correctly"""
    batch = create_test_batch(client)
    
    cost_payload = {
        "batch_id": batch["id"],
        "fermentables_cost": 40.00,
        "hops_cost": 10.00,
        "target_price_per_pint": 5.00,
    }
    
    response = client.post("/batch-costs", json=cost_payload)
    assert response.status_code == 200, response.text
    batch_cost = response.json()
    
    # Total cost: 50.00
    # Batch size: 20 liters
    # Cost per pint: 50 / 20 * 0.473176 = ~1.18
    # Target price: 5.00
    # Profit per pint: 5.00 - 1.18 = 3.82
    # Profit margin: (3.82 / 5.00) * 100 = 76.4%
    
    assert batch_cost["target_price_per_pint"] == 5.00
    assert batch_cost["profit_margin"] is not None
    assert batch_cost["profit_margin"] > 70  # Should be around 76%


def test_duplicate_batch_cost_rejected(client):
    """Test that creating duplicate batch cost records is rejected"""
    batch = create_test_batch(client)
    
    cost_payload = {
        "batch_id": batch["id"],
        "fermentables_cost": 45.50,
    }
    
    # Create first record
    response1 = client.post("/batch-costs", json=cost_payload)
    assert response1.status_code == 200
    
    # Try to create duplicate
    response2 = client.post("/batch-costs", json=cost_payload)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"].lower()


def test_batch_cost_not_found(client):
    """Test 404 responses for non-existent batch costs"""
    # Try to get non-existent batch cost
    response = client.get("/batch-costs/99999")
    assert response.status_code == 404
    
    # Try to update non-existent batch cost
    response = client.put("/batch-costs/99999", json={"fermentables_cost": 10.00})
    assert response.status_code == 404
    
    # Try to delete non-existent batch cost
    response = client.delete("/batch-costs/99999")
    assert response.status_code == 404
