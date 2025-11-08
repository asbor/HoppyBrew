from copy import deepcopy

import pytest
import Database.Models as models


BASE_RECIPE_PAYLOAD = {
    "name": "Test Recipe",
    "version": 1,
    "type": "Ale",
    "brewer": "Test Brewer",
    "batch_size": 20.5,
    "boil_size": 25.0,
    "boil_time": 60,
    "notes": "Testing recipe creation flow",
    "hops": [
        {
            "name": "Cascade",
            "use": "Boil",
            "time": 60,
            "amount": 1.5,
            "display_amount": "1.5 oz",
        }
    ],
    "fermentables": [
        {
            "name": "Pale Malt",
            "amount": 5.0,
            "yield_": 78.0,
            "type": "Grain",
        }
    ],
    "yeasts": [
        {
            "name": "Ale Yeast",
            "type": "Ale",
            "attenuation": 75.0,
        }
    ],
    "miscs": [
        {
            "name": "Irish Moss",
            "type": "Fining",
            "use": "Boil",
            "time": 15,
        }
    ],
}


def build_recipe_payload(**overrides):
    payload = deepcopy(BASE_RECIPE_PAYLOAD)
    relationship_fields = {"hops", "fermentables", "yeasts", "miscs"}

    for key, value in overrides.items():
        if key in relationship_fields:
            payload[key] = value
        else:
            payload[key] = value

    return payload


def create_recipe(client, **overrides):
    payload = build_recipe_payload(**overrides)
    response = client.post("/recipes", json=payload)
    assert response.status_code == 200, response.text
    recipe = response.json()
    return recipe, payload


def test_get_recipes_returns_empty_list(client):
    response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []


def test_create_recipe_persists_related_ingredients(client, db_session):
    created, payload = create_recipe(client)
    recipe_id = created["id"]

    assert created["name"] == payload["name"]

    assert db_session.query(models.RecipeHop).filter(
        models.RecipeHop.recipe_id == recipe_id
    ).count() == len(payload["hops"])
    assert db_session.query(models.RecipeFermentable).filter(
        models.RecipeFermentable.recipe_id == recipe_id
    ).count() == len(payload["fermentables"])
    assert db_session.query(models.RecipeMisc).filter(
        models.RecipeMisc.recipe_id == recipe_id
    ).count() == len(payload["miscs"])
    assert db_session.query(models.RecipeYeast).filter(
        models.RecipeYeast.recipe_id == recipe_id
    ).count() == len(payload["yeasts"])


def test_get_recipe_by_id_returns_full_payload(client):
    created, payload = create_recipe(client)
    recipe_id = created["id"]

    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    recipe = response.json()

    assert recipe["id"] == recipe_id
    assert recipe["name"] == payload["name"]
    assert len(recipe["hops"]) == len(payload["hops"])
    assert len(recipe["fermentables"]) == len(payload["fermentables"])
    assert len(recipe["yeasts"]) == len(payload["yeasts"])
    assert len(recipe["miscs"]) == len(payload["miscs"])


def test_get_recipe_by_id_missing_returns_404(client):
    response = client.get("/recipes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_duplicate_recipe_name_rejected(client):
    name = "Duplicate Recipe"
    create_recipe(client, name=name)

    response = client.post("/recipes", json=build_recipe_payload(name=name))
    assert response.status_code == 400
    assert response.json()["detail"] == "Recipe with this name already exists"


def test_update_recipe_replaces_ingredients(client, db_session):
    created, _ = create_recipe(client, name="Update Recipe")
    recipe_id = created["id"]

    updated_payload = build_recipe_payload(
        name="Updated Recipe",
        hops=[
            {
                "name": "Saaz",
                "use": "Dry Hop",
                "time": 3,
                "amount": 0.75,
                "display_amount": "0.75 oz",
            }
        ],
        fermentables=[
            {
                "name": "Munich Malt",
                "amount": 4.2,
                "yield_": 80.0,
                "type": "Grain",
            }
        ],
        yeasts=[
            {
                "name": "Lager Yeast",
                "type": "Lager",
                "attenuation": 78.0,
            }
        ],
        miscs=[
            {
                "name": "Whirlfloc Tablet",
                "type": "Fining",
                "use": "Boil",
                "time": 5,
            }
        ],
    )

    response = client.put(f"/recipes/{recipe_id}", json=updated_payload)
    assert response.status_code == 200, response.text
    updated = response.json()

    assert updated["name"] == "Updated Recipe"
    assert [hop["name"] for hop in updated["hops"]] == ["Saaz"]
    assert [ferm["name"] for ferm in updated["fermentables"]] == ["Munich Malt"]
    assert [yeast["name"] for yeast in updated["yeasts"]] == ["Lager Yeast"]
    assert [misc["name"] for misc in updated["miscs"]] == ["Whirlfloc Tablet"]

    assert (
        db_session.query(models.RecipeHop)
        .filter(models.RecipeHop.recipe_id == recipe_id)
        .count()
        == 1
    )


def test_update_missing_recipe_returns_404(client):
    response = client.put("/recipes/4242", json=build_recipe_payload(name="Missing"))
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_delete_recipe_removes_related_rows(client, db_session):
    created, _ = create_recipe(client, name="Delete Recipe")
    recipe_id = created["id"]

    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe deleted successfully"}

    missing = client.get(f"/recipes/{recipe_id}")
    assert missing.status_code == 404

    assert (
        db_session.query(models.Recipes).filter(models.Recipes.id == recipe_id).count()
        == 0
    )
    assert (
        db_session.query(models.RecipeHop)
        .filter(models.RecipeHop.recipe_id == recipe_id)
        .count()
        == 0
    )
    assert (
        db_session.query(models.RecipeFermentable)
        .filter(models.RecipeFermentable.recipe_id == recipe_id)
        .count()
        == 0
    )
    assert (
        db_session.query(models.RecipeMisc)
        .filter(models.RecipeMisc.recipe_id == recipe_id)
        .count()
        == 0
    )
    assert (
        db_session.query(models.RecipeYeast)
        .filter(models.RecipeYeast.recipe_id == recipe_id)
        .count()
        == 0
    )


def test_scale_recipe_endpoint_returns_scaled_payload(client):
    created, payload = create_recipe(client, name="Scalable Recipe")
    recipe_id = created["id"]

    original_batch = payload["batch_size"]
    target_batch_size = original_batch * 1.5

    response = client.post(
        f"/recipes/{recipe_id}/scale",
        json={"target_batch_size": target_batch_size},
    )

    assert response.status_code == 200, response.text

    data = response.json()
    assert data["original_batch_size"] == pytest.approx(original_batch)
    assert data["target_batch_size"] == pytest.approx(target_batch_size)
    assert data["scale_factor"] == pytest.approx(target_batch_size / original_batch)

    scaled_recipe = data["scaled_recipe"]
    assert scaled_recipe["batch_size"] == pytest.approx(target_batch_size)
    assert scaled_recipe["boil_size"] == pytest.approx(
        payload["boil_size"] * (target_batch_size / original_batch)
    )

    original_hop_amount = payload["hops"][0]["amount"]
    scaled_hop_amount = scaled_recipe["hops"][0]["amount"]
    assert scaled_hop_amount == pytest.approx(
        original_hop_amount * (target_batch_size / original_batch)
    )

    original_fermentable_amount = payload["fermentables"][0]["amount"]
    scaled_fermentable_amount = scaled_recipe["fermentables"][0]["amount"]
    assert scaled_fermentable_amount == pytest.approx(
        original_fermentable_amount * (target_batch_size / original_batch)
    )


def test_scale_recipe_to_equipment_endpoint(client, db_session):
    """Test scaling a recipe to match an equipment profile's batch size"""
    # Create a recipe
    created, payload = create_recipe(client, name="Test Recipe For Equipment")
    recipe_id = created["id"]
    original_batch = payload["batch_size"]

    # Create an equipment profile
    equipment_data = {
        "name": "Test Brewing System",
        "version": 1,
        "batch_size": 40,
        "boil_size": 50,
        "boil_time": 60,
    }
    equipment_response = client.post("/equipment", json=equipment_data)
    assert equipment_response.status_code == 201, equipment_response.text
    equipment = equipment_response.json()
    equipment_id = int(equipment["id"])

    # Scale the recipe to the equipment
    response = client.post(f"/recipes/{recipe_id}/scale-to-equipment/{equipment_id}")
    assert response.status_code == 200, response.text

    data = response.json()
    
    # Verify scaling results
    assert data["original_batch_size"] == pytest.approx(original_batch)
    assert data["target_batch_size"] == pytest.approx(equipment_data["batch_size"])
    assert data["scale_factor"] == pytest.approx(
        equipment_data["batch_size"] / original_batch
    )
    
    # Verify equipment profile info is included
    assert data["equipment_profile_id"] == equipment_id
    assert data["equipment_profile_name"] == equipment_data["name"]

    # Verify scaled recipe has equipment's batch and boil sizes
    scaled_recipe = data["scaled_recipe"]
    assert scaled_recipe["batch_size"] == pytest.approx(equipment_data["batch_size"])
    assert scaled_recipe["boil_size"] == pytest.approx(equipment_data["boil_size"])

    # Verify ingredients are scaled correctly
    scale_factor = equipment_data["batch_size"] / original_batch
    original_hop_amount = payload["hops"][0]["amount"]
    scaled_hop_amount = scaled_recipe["hops"][0]["amount"]
    assert scaled_hop_amount == pytest.approx(original_hop_amount * scale_factor)

    original_fermentable_amount = payload["fermentables"][0]["amount"]
    scaled_fermentable_amount = scaled_recipe["fermentables"][0]["amount"]
    assert scaled_fermentable_amount == pytest.approx(
        original_fermentable_amount * scale_factor
    )


def test_scale_recipe_to_equipment_with_missing_equipment_batch_size(client, db_session):
    """Test that equipment without batch_size returns error"""
    created, _ = create_recipe(client, name="Test Recipe")
    recipe_id = created["id"]

    # Create equipment without batch_size
    equipment_data = {
        "name": "Incomplete Equipment",
        "version": 1,
        "boil_time": 60,
    }
    equipment_response = client.post("/equipment", json=equipment_data)
    assert equipment_response.status_code == 201
    equipment_id = int(equipment_response.json()["id"])

    response = client.post(f"/recipes/{recipe_id}/scale-to-equipment/{equipment_id}")
    assert response.status_code == 400
    assert "missing batch_size" in response.json()["detail"].lower()


def test_scale_recipe_to_equipment_with_missing_recipe(client, db_session):
    """Test that missing recipe returns 404"""
    # Create equipment
    equipment_data = {"name": "Test Equipment", "batch_size": 30, "boil_size": 40}
    equipment_response = client.post("/equipment", json=equipment_data)
    equipment_id = int(equipment_response.json()["id"])

    response = client.post(f"/recipes/999999/scale-to-equipment/{equipment_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_scale_recipe_to_equipment_with_missing_equipment(client):
    """Test that missing equipment profile returns 404"""
    created, _ = create_recipe(client, name="Test Recipe")
    recipe_id = created["id"]

    response = client.post(f"/recipes/{recipe_id}/scale-to-equipment/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Equipment profile not found"


    metrics = data["metrics"]
    assert set(metrics.keys()) == {"abv", "ibu", "srm"}


# Tests for individual ingredient CRUD operations


def test_add_hop_to_recipe(client):
    """Test adding a hop ingredient to a recipe"""
    created, _ = create_recipe(client, name="Test Hop Addition")
    recipe_id = created["id"]

    new_hop = {
        "name": "Centennial",
        "alpha": 9.5,
        "amount": 1.0,
        "use": "Boil",
        "time": 30,
        "stage": "boil",
        "duration": 30,
        "notes": "For bitterness and aroma",
    }

    response = client.post(f"/recipes/{recipe_id}/ingredients/hops", json=new_hop)
    assert response.status_code == 200
    hop = response.json()
    assert hop["name"] == "Centennial"
    assert hop["alpha"] == 9.5
    assert hop["stage"] == "boil"
    assert hop["duration"] == 30


def test_update_hop_in_recipe(client):
    """Test updating a hop ingredient in a recipe"""
    created, _ = create_recipe(client, name="Test Hop Update")
    recipe_id = created["id"]
    hop_id = created["hops"][0]["id"]

    updated_hop = {
        "name": "Cascade Updated",
        "alpha": 6.0,
        "amount": 2.0,
        "use": "Dry Hop",
        "time": 7,
        "stage": "fermentation",
        "duration": 10080,
        "notes": "Updated for dry hopping",
    }

    response = client.put(
        f"/recipes/{recipe_id}/ingredients/hops/{hop_id}", json=updated_hop
    )
    assert response.status_code == 200
    hop = response.json()
    assert hop["name"] == "Cascade Updated"
    assert hop["alpha"] == 6.0
    assert hop["stage"] == "fermentation"
    assert hop["duration"] == 10080


def test_delete_hop_from_recipe(client):
    """Test deleting a hop ingredient from a recipe"""
    created, _ = create_recipe(client, name="Test Hop Deletion")
    recipe_id = created["id"]
    hop_id = created["hops"][0]["id"]

    response = client.delete(f"/recipes/{recipe_id}/ingredients/hops/{hop_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Hop ingredient deleted successfully"

    # Verify hop was deleted
    recipe_response = client.get(f"/recipes/{recipe_id}")
    recipe = recipe_response.json()
    assert len(recipe["hops"]) == 0


def test_add_fermentable_to_recipe(client):
    """Test adding a fermentable ingredient to a recipe"""
    created, _ = create_recipe(client, name="Test Fermentable Addition")
    recipe_id = created["id"]

    new_fermentable = {
        "name": "Munich Malt",
        "type": "Grain",
        "amount": 2.0,
        "yield_": 78.0,
        "color": 9,
        "stage": "mash",
        "duration": 60,
        "notes": "For maltiness",
    }

    response = client.post(
        f"/recipes/{recipe_id}/ingredients/fermentables", json=new_fermentable
    )
    assert response.status_code == 200
    fermentable = response.json()
    assert fermentable["name"] == "Munich Malt"
    assert fermentable["stage"] == "mash"
    assert fermentable["duration"] == 60


def test_update_fermentable_in_recipe(client):
    """Test updating a fermentable ingredient in a recipe"""
    created, _ = create_recipe(client, name="Test Fermentable Update")
    recipe_id = created["id"]
    fermentable_id = created["fermentables"][0]["id"]

    updated_fermentable = {
        "name": "Pale Malt Updated",
        "type": "Grain",
        "amount": 6.0,
        "yield_": 80.0,
        "color": 3,
        "stage": "mash",
        "duration": 75,
        "notes": "Updated base malt",
    }

    response = client.put(
        f"/recipes/{recipe_id}/ingredients/fermentables/{fermentable_id}",
        json=updated_fermentable,
    )
    assert response.status_code == 200
    fermentable = response.json()
    assert fermentable["name"] == "Pale Malt Updated"
    assert fermentable["amount"] == 6.0
    assert fermentable["duration"] == 75


def test_delete_fermentable_from_recipe(client):
    """Test deleting a fermentable ingredient from a recipe"""
    created, _ = create_recipe(client, name="Test Fermentable Deletion")
    recipe_id = created["id"]
    fermentable_id = created["fermentables"][0]["id"]

    response = client.delete(
        f"/recipes/{recipe_id}/ingredients/fermentables/{fermentable_id}"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Fermentable ingredient deleted successfully"

    # Verify fermentable was deleted
    recipe_response = client.get(f"/recipes/{recipe_id}")
    recipe = recipe_response.json()
    assert len(recipe["fermentables"]) == 0


def test_add_yeast_to_recipe(client):
    """Test adding a yeast ingredient to a recipe"""
    created, _ = create_recipe(client, name="Test Yeast Addition")
    recipe_id = created["id"]

    new_yeast = {
        "name": "WLP001",
        "type": "Ale",
        "form": "Liquid",
        "amount": 100.0,
        "attenuation": 77.0,
        "stage": "fermentation",
        "duration": 10080,
        "notes": "California Ale Yeast",
    }

    response = client.post(f"/recipes/{recipe_id}/ingredients/yeasts", json=new_yeast)
    assert response.status_code == 200
    yeast = response.json()
    assert yeast["name"] == "WLP001"
    assert yeast["stage"] == "fermentation"
    assert yeast["duration"] == 10080


def test_update_yeast_in_recipe(client):
    """Test updating a yeast ingredient in a recipe"""
    created, _ = create_recipe(client, name="Test Yeast Update")
    recipe_id = created["id"]
    yeast_id = created["yeasts"][0]["id"]

    updated_yeast = {
        "name": "US-05 Updated",
        "type": "Ale",
        "form": "Dry",
        "amount": 11.5,
        "attenuation": 80.0,
        "stage": "fermentation",
        "duration": 14400,
        "notes": "Updated yeast info",
    }

    response = client.put(
        f"/recipes/{recipe_id}/ingredients/yeasts/{yeast_id}", json=updated_yeast
    )
    assert response.status_code == 200
    yeast = response.json()
    assert yeast["name"] == "US-05 Updated"
    assert yeast["attenuation"] == 80.0
    assert yeast["duration"] == 14400


def test_delete_yeast_from_recipe(client):
    """Test deleting a yeast ingredient from a recipe"""
    created, _ = create_recipe(client, name="Test Yeast Deletion")
    recipe_id = created["id"]
    yeast_id = created["yeasts"][0]["id"]

    response = client.delete(f"/recipes/{recipe_id}/ingredients/yeasts/{yeast_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Yeast ingredient deleted successfully"

    # Verify yeast was deleted
    recipe_response = client.get(f"/recipes/{recipe_id}")
    recipe = recipe_response.json()
    assert len(recipe["yeasts"]) == 0


def test_add_misc_to_recipe(client):
    """Test adding a misc ingredient to a recipe"""
    created, _ = create_recipe(client, name="Test Misc Addition")
    recipe_id = created["id"]

    new_misc = {
        "name": "Whirlfloc",
        "type": "Fining",
        "use": "Boil",
        "amount": 1,
        "time": 5,
        "stage": "boil",
        "duration": 5,
        "notes": "For clarity",
    }

    response = client.post(f"/recipes/{recipe_id}/ingredients/miscs", json=new_misc)
    assert response.status_code == 200
    misc = response.json()
    assert misc["name"] == "Whirlfloc"
    assert misc["stage"] == "boil"
    assert misc["duration"] == 5


def test_update_misc_in_recipe(client):
    """Test updating a misc ingredient in a recipe"""
    created, _ = create_recipe(client, name="Test Misc Update")
    recipe_id = created["id"]
    misc_id = created["miscs"][0]["id"]

    updated_misc = {
        "name": "Irish Moss Updated",
        "type": "Fining",
        "use": "Boil",
        "amount": 2,
        "time": 10,
        "stage": "boil",
        "duration": 10,
        "notes": "Updated fining agent",
    }

    response = client.put(
        f"/recipes/{recipe_id}/ingredients/miscs/{misc_id}", json=updated_misc
    )
    assert response.status_code == 200
    misc = response.json()
    assert misc["name"] == "Irish Moss Updated"
    assert misc["amount"] == 2
    assert misc["duration"] == 10


def test_delete_misc_from_recipe(client):
    """Test deleting a misc ingredient from a recipe"""
    created, _ = create_recipe(client, name="Test Misc Deletion")
    recipe_id = created["id"]
    misc_id = created["miscs"][0]["id"]

    response = client.delete(f"/recipes/{recipe_id}/ingredients/miscs/{misc_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Misc ingredient deleted successfully"

    # Verify misc was deleted
    recipe_response = client.get(f"/recipes/{recipe_id}")
    recipe = recipe_response.json()
    assert len(recipe["miscs"]) == 0


def test_ingredient_not_found_returns_404(client):
    """Test that accessing non-existent ingredients returns 404"""
    created, _ = create_recipe(client, name="Test 404")
    recipe_id = created["id"]

    response = client.get(f"/recipes/{recipe_id}/ingredients/hops/9999")
    # Note: This endpoint doesn't exist in our implementation, but testing DELETE
    response = client.delete(f"/recipes/{recipe_id}/ingredients/hops/9999")
    assert response.status_code == 404


# Tests for recipe versioning


def test_create_recipe_version(client):
    """Test creating a version snapshot of a recipe"""
    created, _ = create_recipe(client, name="Test Recipe Versioning")
    recipe_id = created["id"]

    version_data = {
        "version_name": "v1.0 - Initial Release",
        "notes": "First version of the recipe",
    }

    response = client.post(f"/recipes/{recipe_id}/version", json=version_data)
    assert response.status_code == 200
    version = response.json()
    assert version["recipe_id"] == recipe_id
    assert version["version_number"] == 1
    assert version["version_name"] == "v1.0 - Initial Release"
    assert version["notes"] == "First version of the recipe"
    assert "recipe_snapshot" in version
    assert "created_at" in version


def test_create_multiple_recipe_versions(client):
    """Test creating multiple versions of a recipe"""
    created, _ = create_recipe(client, name="Test Multiple Versions")
    recipe_id = created["id"]

    # Create first version
    version1_data = {
        "version_name": "v1.0",
        "notes": "Initial version",
    }
    response1 = client.post(f"/recipes/{recipe_id}/version", json=version1_data)
    assert response1.status_code == 200
    version1 = response1.json()
    assert version1["version_number"] == 1

    # Create second version
    version2_data = {
        "version_name": "v1.1",
        "notes": "Minor update",
    }
    response2 = client.post(f"/recipes/{recipe_id}/version", json=version2_data)
    assert response2.status_code == 200
    version2 = response2.json()
    assert version2["version_number"] == 2


def test_get_recipe_versions(client):
    """Test retrieving version history for a recipe"""
    created, _ = create_recipe(client, name="Test Version History")
    recipe_id = created["id"]

    # Create a couple of versions
    client.post(
        f"/recipes/{recipe_id}/version",
        json={"version_name": "v1.0", "notes": "First version"},
    )
    client.post(
        f"/recipes/{recipe_id}/version",
        json={"version_name": "v1.1", "notes": "Second version"},
    )

    # Get version history
    response = client.get(f"/recipes/{recipe_id}/versions")
    assert response.status_code == 200
    versions = response.json()
    assert len(versions) == 2
    # Versions should be in descending order
    assert versions[0]["version_number"] == 2
    assert versions[1]["version_number"] == 1


def test_get_versions_for_nonexistent_recipe_returns_404(client):
    """Test that getting versions for a non-existent recipe returns 404"""
    response = client.get("/recipes/9999/versions")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_create_version_for_nonexistent_recipe_returns_404(client):
    """Test that creating a version for a non-existent recipe returns 404"""
    version_data = {
        "version_name": "v1.0",
        "notes": "Test",
    }
    response = client.post("/recipes/9999/version", json=version_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"
