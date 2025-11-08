import pytest
from datetime import datetime
import Database.Models as models
import Database.Schemas as schemas


def create_recipe_with_ingredients(client, db_session):
    """Helper to create a recipe with ingredients"""
    payload = {
        "name": "Test Recipe for Inventory",
        "version": 1,
        "type": "Ale",
        "brewer": "Tester",
        "batch_size": 20.0,
        "boil_size": 25.0,
        "boil_time": 60,
        "hops": [{"name": "Cascade", "amount": 0.5}],
        "fermentables": [{"name": "Pale Malt", "amount": 5.0}],
        "yeasts": [{"name": "Ale Yeast", "amount": 11.5}],
        "miscs": [{"name": "Irish Moss", "amount": 10.0}],
    }
    
    response = client.post("/recipes", json=payload)
    assert response.status_code == 200, response.text
    
    recipe = db_session.query(models.Recipes).filter(
        models.Recipes.name == "Test Recipe for Inventory"
    ).one()
    return recipe.id


def create_batch_with_inventory(client, db_session):
    """Helper to create a batch and set up inventory items"""
    recipe_id = create_recipe_with_ingredients(client, db_session)
    
    # Create batch
    batch_payload = {
        "recipe_id": recipe_id,
        "batch_name": "Test Batch",
        "batch_number": 1,
        "batch_size": 18.5,
        "brewer": "Test Brewer",
        "brew_date": datetime(2024, 1, 1, 12, 0, 0).isoformat(),
    }
    
    response = client.post("/batches", json=batch_payload)
    assert response.status_code == 200, response.text
    batch = response.json()
    
    # Get the created inventory items (linked to batch)
    inventory_hops = db_session.query(models.InventoryHop).filter(
        models.InventoryHop.batch_id == batch['id']
    ).all()
    inventory_fermentables = db_session.query(models.InventoryFermentable).filter(
        models.InventoryFermentable.batch_id == batch['id']
    ).all()
    
    # Set inventory levels
    for hop in inventory_hops:
        hop.inventory = 10.0  # 10 kg available
        hop.amount = 0.5  # Recipe needs 0.5 kg
    
    for ferm in inventory_fermentables:
        ferm.inventory = 50.0  # 50 kg available
        ferm.amount = 5.0  # Recipe needs 5 kg
    
    db_session.commit()
    
    return batch['id'], inventory_hops, inventory_fermentables


def test_consume_ingredients_success(client, db_session):
    """Test successful ingredient consumption"""
    batch_id, inventory_hops, inventory_fermentables = create_batch_with_inventory(client, db_session)
    
    # Prepare consumption request
    consume_request = {
        "ingredients": [
            {
                "batch_id": batch_id,
                "inventory_item_id": inventory_hops[0].id,
                "inventory_item_type": "hop",
                "quantity_used": 0.5,
                "unit": "kg"
            },
            {
                "batch_id": batch_id,
                "inventory_item_id": inventory_fermentables[0].id,
                "inventory_item_type": "fermentable",
                "quantity_used": 5.0,
                "unit": "kg"
            }
        ]
    }
    
    response = client.post(f"/batches/{batch_id}/consume-ingredients", json=consume_request)
    assert response.status_code == 200, response.text
    
    result = response.json()
    assert result["batch_id"] == batch_id
    assert result["consumed_count"] == 2
    assert result["transactions_created"] == 2
    
    # Verify batch_ingredients were created
    batch_ingredients = db_session.query(models.BatchIngredient).filter(
        models.BatchIngredient.batch_id == batch_id
    ).all()
    assert len(batch_ingredients) == 2
    
    # Verify inventory was updated
    db_session.refresh(inventory_hops[0])
    # inventory field is stored as String, so compare as float
    assert float(inventory_hops[0].inventory) == pytest.approx(9.5)  # 10 - 0.5
    
    db_session.refresh(inventory_fermentables[0])
    assert float(inventory_fermentables[0].inventory) == pytest.approx(45.0)  # 50 - 5.0
    
    # Verify transactions were created
    transactions = db_session.query(models.InventoryTransaction).filter(
        models.InventoryTransaction.reference_type == 'batch',
        models.InventoryTransaction.reference_id == batch_id
    ).all()
    assert len(transactions) == 2
    
    # Check transaction details
    hop_transaction = [t for t in transactions if t.inventory_item_type == 'hop'][0]
    assert hop_transaction.transaction_type == 'consumption'
    assert hop_transaction.quantity_change == -0.5
    assert hop_transaction.quantity_before == 10.0
    assert hop_transaction.quantity_after == 9.5


def test_consume_ingredients_insufficient_stock(client, db_session):
    """Test consumption fails when insufficient stock"""
    batch_id, inventory_hops, _ = create_batch_with_inventory(client, db_session)
    
    # Set low stock
    inventory_hops[0].inventory = 0.2
    db_session.commit()
    
    # Try to consume more than available
    consume_request = {
        "ingredients": [
            {
                "batch_id": batch_id,
                "inventory_item_id": inventory_hops[0].id,
                "inventory_item_type": "hop",
                "quantity_used": 0.5,
                "unit": "kg"
            }
        ]
    }
    
    response = client.post(f"/batches/{batch_id}/consume-ingredients", json=consume_request)
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]


def test_consume_ingredients_invalid_batch(client, db_session):
    """Test consumption fails for non-existent batch"""
    consume_request = {
        "ingredients": [
            {
                "batch_id": 9999,
                "inventory_item_id": 1,
                "inventory_item_type": "hop",
                "quantity_used": 0.5,
                "unit": "kg"
            }
        ]
    }
    
    response = client.post("/batches/9999/consume-ingredients", json=consume_request)
    assert response.status_code == 404
    assert "Batch not found" in response.json()["detail"]


def test_get_ingredient_tracking(client, db_session):
    """Test retrieving ingredient tracking for a batch"""
    batch_id, inventory_hops, inventory_fermentables = create_batch_with_inventory(client, db_session)
    
    # Consume ingredients first
    consume_request = {
        "ingredients": [
            {
                "batch_id": batch_id,
                "inventory_item_id": inventory_hops[0].id,
                "inventory_item_type": "hop",
                "quantity_used": 0.5,
                "unit": "kg"
            }
        ]
    }
    
    consume_response = client.post(f"/batches/{batch_id}/consume-ingredients", json=consume_request)
    assert consume_response.status_code == 200
    
    # Get tracking
    response = client.get(f"/batches/{batch_id}/ingredient-tracking")
    assert response.status_code == 200, response.text
    
    tracking = response.json()
    assert tracking["batch_id"] == batch_id
    assert tracking["batch_name"] == "Test Batch"
    assert len(tracking["consumed_ingredients"]) == 1
    assert len(tracking["transactions"]) == 1
    
    # Verify consumed ingredient details
    consumed = tracking["consumed_ingredients"][0]
    assert consumed["inventory_item_type"] == "hop"
    assert consumed["quantity_used"] == 0.5
    assert consumed["unit"] == "kg"


def test_get_ingredient_tracking_empty_batch(client, db_session):
    """Test tracking for batch with no consumed ingredients"""
    batch_id, _, _ = create_batch_with_inventory(client, db_session)
    
    response = client.get(f"/batches/{batch_id}/ingredient-tracking")
    assert response.status_code == 200, response.text
    
    tracking = response.json()
    assert tracking["batch_id"] == batch_id
    assert len(tracking["consumed_ingredients"]) == 0
    assert len(tracking["transactions"]) == 0


def test_get_ingredient_tracking_invalid_batch(client, db_session):
    """Test tracking fails for non-existent batch"""
    response = client.get("/batches/9999/ingredient-tracking")
    assert response.status_code == 404
    assert "Batch not found" in response.json()["detail"]


def test_check_inventory_availability(client, db_session):
    """Test checking inventory availability for a recipe"""
    recipe_id = create_recipe_with_ingredients(client, db_session)
    
    response = client.get(f"/batches/check-inventory-availability/{recipe_id}")
    assert response.status_code == 200, response.text
    
    availability = response.json()
    assert len(availability) > 0
    
    # Check structure of availability items
    for item in availability:
        assert "inventory_item_id" in item
        assert "inventory_item_type" in item
        assert "name" in item
        assert "available_quantity" in item
        assert "required_quantity" in item
        assert "unit" in item
        assert "is_available" in item


def test_check_inventory_availability_invalid_recipe(client, db_session):
    """Test availability check fails for non-existent recipe"""
    response = client.get("/batches/check-inventory-availability/9999")
    assert response.status_code == 404
    assert "Recipe not found" in response.json()["detail"]


def test_batch_deletion_removes_batch_ingredients(client, db_session):
    """Test that deleting a batch also removes batch_ingredients"""
    batch_id, inventory_hops, _ = create_batch_with_inventory(client, db_session)
    
    # Consume ingredients
    consume_request = {
        "ingredients": [
            {
                "batch_id": batch_id,
                "inventory_item_id": inventory_hops[0].id,
                "inventory_item_type": "hop",
                "quantity_used": 0.5,
                "unit": "kg"
            }
        ]
    }
    
    client.post(f"/batches/{batch_id}/consume-ingredients", json=consume_request)
    
    # Verify batch_ingredients exist
    batch_ingredients = db_session.query(models.BatchIngredient).filter(
        models.BatchIngredient.batch_id == batch_id
    ).all()
    assert len(batch_ingredients) > 0
    
    # Delete batch
    response = client.delete(f"/batches/{batch_id}")
    assert response.status_code == 200
    
    # Verify batch_ingredients were deleted (cascade)
    batch_ingredients = db_session.query(models.BatchIngredient).filter(
        models.BatchIngredient.batch_id == batch_id
    ).all()
    assert len(batch_ingredients) == 0
