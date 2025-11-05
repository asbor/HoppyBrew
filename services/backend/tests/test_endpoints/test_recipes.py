from copy import deepcopy

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

    assert (
        db_session.query(models.RecipeHop)
        .filter(models.RecipeHop.recipe_id == recipe_id)
        .count()
        == len(payload["hops"])
    )
    assert (
        db_session.query(models.RecipeFermentable)
        .filter(models.RecipeFermentable.recipe_id == recipe_id)
        .count()
        == len(payload["fermentables"])
    )
    assert (
        db_session.query(models.RecipeMisc)
        .filter(models.RecipeMisc.recipe_id == recipe_id)
        .count()
        == len(payload["miscs"])
    )
    assert (
        db_session.query(models.RecipeYeast)
        .filter(models.RecipeYeast.recipe_id == recipe_id)
        .count()
        == len(payload["yeasts"])
    )


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
        db_session.query(models.Recipes)
        .filter(models.Recipes.id == recipe_id)
        .count()
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
