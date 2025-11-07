import pytest
from datetime import datetime
import Database.Models as models


def create_base_recipe(client, db_session, name="Test Recipe"):
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

    recipe = (
        db_session.query(models.Recipes)
        .filter(models.Recipes.name == name)
        .one()
    )
    return recipe.id


def build_batch_payload(recipe_id, suffix="001"):
    return {
        "recipe_id": recipe_id,
        "batch_name": f"Batch {suffix}",
        "batch_number": int(suffix),
        "batch_size": 18.5,
        "brewer": "Batch Brewer",
        "brew_date": datetime(2024, 1, 1, 12, 0, 0).isoformat(),
    }


def test_create_batch_copies_recipe_inventory(client, db_session):
    recipe_id = create_base_recipe(client, db_session)

    response = client.post("/batches", json=build_batch_payload(recipe_id))
    assert response.status_code == 200, response.text
    batch = response.json()

    assert batch["batch_name"] == "Batch 001"
    assert batch["recipe_id"] != recipe_id  # cloned recipe

    detail = client.get(f"/batches/{batch['id']}")
    assert detail.status_code == 200, detail.text
    payload = detail.json()

    assert len(payload["inventory_hops"]) == 1
    assert len(payload["inventory_fermentables"]) == 1
    assert len(payload["inventory_miscs"]) == 1
    assert len(payload["inventory_yeasts"]) == 1


def test_create_batch_with_unknown_recipe_returns_404(client):
    response = client.post("/batches", json=build_batch_payload(999))
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_update_batch_persists_changes(client, db_session):
    recipe_id = create_base_recipe(client, db_session, name="Update Recipe")

    create_resp = client.post("/batches", json=build_batch_payload(recipe_id))
    batch_id = create_resp.json()["id"]

    update_payload = {
        "batch_name": "Batch Updated",
        "batch_number": 42,
        "batch_size": 20.5,
        "brewer": "Updated Brewer",
        "brew_date": datetime(2024, 2, 2, 10, 30, 0).isoformat(),
    }
    response = client.put(f"/batches/{batch_id}", json=update_payload)
    assert response.status_code == 200, response.text

    updated = response.json()
    assert updated["batch_name"] == "Batch Updated"
    assert updated["batch_number"] == 42
    assert updated["batch_size"] == pytest.approx(20.5)
    assert updated["brewer"] == "Updated Brewer"


def test_delete_batch_removes_inventory(client, db_session):
    recipe_id = create_base_recipe(client, db_session, name="Delete Recipe")
    create_resp = client.post("/batches", json=build_batch_payload(recipe_id))
    batch_id = create_resp.json()["id"]

    response = client.delete(f"/batches/{batch_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Batch deleted successfully"}

    missing = client.get(f"/batches/{batch_id}")
    assert missing.status_code == 404

    assert (
        db_session.query(models.InventoryHop).filter_by(batch_id=batch_id).count()
        == 0
    )
    assert (
        db_session.query(models.InventoryFermentable)
        .filter_by(batch_id=batch_id)
        .count()
        == 0
    )
    assert (
        db_session.query(models.InventoryMisc).filter_by(batch_id=batch_id).count()
        == 0
    )
    assert (
        db_session.query(models.InventoryYeast).filter_by(batch_id=batch_id).count()
        == 0
    )


def test_get_all_batches_returns_empty_list_when_no_batches(client):
    response = client.get("/batches")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_batches_returns_list_with_inventory(client, db_session):
    recipe_id = create_base_recipe(client, db_session, name="List Recipe")
    client.post("/batches", json=build_batch_payload(recipe_id, "001"))
    client.post("/batches", json=build_batch_payload(recipe_id, "002"))

    response = client.get("/batches")
    assert response.status_code == 200
    batches = response.json()
    
    assert len(batches) == 2
    
    # Verify each batch has the required inventory relationships loaded
    for batch in batches:
        assert "inventory_hops" in batch
        assert "inventory_fermentables" in batch
        assert "inventory_miscs" in batch
        assert "inventory_yeasts" in batch
        assert isinstance(batch["inventory_hops"], list)
        assert isinstance(batch["inventory_fermentables"], list)
        assert isinstance(batch["inventory_miscs"], list)
        assert isinstance(batch["inventory_yeasts"], list)
