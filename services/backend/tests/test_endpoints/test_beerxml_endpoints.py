"""
Tests for BeerXML import/export API endpoints
"""

import pytest
import io


# Sample BeerXML for testing
SAMPLE_BEERXML = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPES>
<RECIPE>
 <NAME>API Test IPA</NAME>
 <VERSION>1</VERSION>
 <TYPE>All Grain</TYPE>
 <BREWER>Test Brewer</BREWER>
 <BATCH_SIZE>20.0</BATCH_SIZE>
 <BOIL_SIZE>25.0</BOIL_SIZE>
 <BOIL_TIME>60</BOIL_TIME>
 <EFFICIENCY>75.0</EFFICIENCY>
 <HOPS>
  <HOP>
   <NAME>Cascade</NAME>
   <VERSION>1</VERSION>
   <ALPHA>5.5</ALPHA>
   <AMOUNT>0.0283</AMOUNT>
   <USE>Boil</USE>
   <TIME>60.0</TIME>
   <FORM>Pellet</FORM>
  </HOP>
 </HOPS>
 <FERMENTABLES>
  <FERMENTABLE>
   <NAME>Pale Malt</NAME>
   <VERSION>1</VERSION>
   <TYPE>Grain</TYPE>
   <AMOUNT>4.5</AMOUNT>
   <YIELD>80.0</YIELD>
   <COLOR>2.5</COLOR>
  </FERMENTABLE>
 </FERMENTABLES>
 <YEASTS>
  <YEAST>
   <NAME>US-05</NAME>
   <VERSION>1</VERSION>
   <TYPE>Ale</TYPE>
   <FORM>Dry</FORM>
   <ATTENUATION>75.0</ATTENUATION>
  </YEAST>
 </YEASTS>
 <MISCS>
  <MISC>
   <NAME>Irish Moss</NAME>
   <VERSION>1</VERSION>
   <TYPE>Fining</TYPE>
   <USE>Boil</USE>
   <TIME>10.0</TIME>
  </MISC>
 </MISCS>
 <NOTES>A test IPA recipe</NOTES>
 <OG>1.055</OG>
 <FG>1.012</FG>
 <IBU>45.0</IBU>
</RECIPE>
</RECIPES>
"""


def test_import_beerxml_success(client, db_session):
    """Test successful BeerXML import"""
    files = {
        "file": ("test_recipe.xml", io.BytesIO(SAMPLE_BEERXML), "application/xml")
    }

    response = client.post("/api/recipes/import/beerxml", files=files)

    assert response.status_code == 200
    data = response.json()

    assert data["imported_count"] == 1
    assert data["skipped_count"] == 0
    assert len(data["errors"]) == 0
    assert len(data["recipe_ids"]) == 1
    assert "Import completed" in data["message"]

    # Verify recipe was created in database
    recipe_id = data["recipe_ids"][0]
    response = client.get(f"/api/recipes/{recipe_id}")
    assert response.status_code == 200

    recipe = response.json()
    assert recipe["name"] == "API Test IPA"
    assert recipe["type"] == "All Grain"
    assert recipe["brewer"] == "Test Brewer"
    assert recipe["batch_size"] == 20.0
    assert len(recipe["hops"]) == 1
    assert len(recipe["fermentables"]) == 1
    assert len(recipe["yeasts"]) == 1
    assert len(recipe["miscs"]) == 1


def test_import_beerxml_invalid_xml(client):
    """Test importing invalid XML returns error"""
    invalid_xml = b"<INVALID>Not valid XML"
    files = {
        "file": ("invalid.xml", io.BytesIO(invalid_xml), "application/xml")
    }

    response = client.post("/api/recipes/import/beerxml", files=files)

    assert response.status_code == 400
    assert "Invalid XML format" in response.json()["detail"]


def test_import_beerxml_empty_recipes(client):
    """Test importing XML with no recipes returns error"""
    empty_xml = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPES>
</RECIPES>
"""
    files = {
        "file": ("empty.xml", io.BytesIO(empty_xml), "application/xml")
    }

    response = client.post("/api/recipes/import/beerxml", files=files)

    assert response.status_code == 400
    assert "Invalid BeerXML" in response.json()["detail"]


def test_import_beerxml_multiple_recipes(client, db_session):
    """Test importing multiple recipes"""
    multi_recipe_xml = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPES>
<RECIPE>
 <NAME>Recipe 1</NAME>
 <VERSION>1</VERSION>
 <TYPE>All Grain</TYPE>
 <BATCH_SIZE>20.0</BATCH_SIZE>
</RECIPE>
<RECIPE>
 <NAME>Recipe 2</NAME>
 <VERSION>1</VERSION>
 <TYPE>Extract</TYPE>
 <BATCH_SIZE>19.0</BATCH_SIZE>
</RECIPE>
</RECIPES>
"""

    files = {
        "file": ("multi.xml", io.BytesIO(multi_recipe_xml), "application/xml")
    }

    response = client.post("/api/recipes/import/beerxml", files=files)

    assert response.status_code == 200
    data = response.json()

    assert data["imported_count"] == 2
    assert len(data["recipe_ids"]) == 2


def test_export_single_recipe_beerxml(client, db_session, sample_recipe):
    """Test exporting a single recipe to BeerXML"""
    recipe_id = sample_recipe["id"]

    response = client.get(f"/api/recipes/{recipe_id}/export/beerxml")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml; charset=utf-8"
    assert "attachment" in response.headers["content-disposition"]

    # Verify XML is valid and contains recipe data
    xml_content = response.content
    assert b"<RECIPES>" in xml_content
    assert b"<RECIPE>" in xml_content
    assert b"<NAME>" in xml_content
    assert sample_recipe["name"].encode() in xml_content


def test_export_nonexistent_recipe(client):
    """Test exporting non-existent recipe returns 404"""
    response = client.get("/api/recipes/99999/export/beerxml")

    assert response.status_code == 404
    assert "Recipe not found" in response.json()["detail"]


def test_export_multiple_recipes_beerxml(client, db_session, sample_recipe):
    """Test exporting multiple recipes to BeerXML"""
    # Create a second recipe
    recipe_data = {
        "name": "Second Recipe",
        "version": 1,
        "type": "Extract",
        "batch_size": 19.0,
        "hops": [],
        "fermentables": [],
        "yeasts": [],
        "miscs": [],
    }

    create_response = client.post("/api/recipes", json=recipe_data)
    assert create_response.status_code == 200
    second_recipe_id = create_response.json()["id"]

    # Export both recipes
    recipe_ids = [sample_recipe["id"], second_recipe_id]
    response = client.post("/api/recipes/export/beerxml", json=recipe_ids)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml; charset=utf-8"

    # Verify both recipes are in the XML
    xml_content = response.content
    assert b"<RECIPES>" in xml_content
    assert sample_recipe["name"].encode() in xml_content
    assert b"Second Recipe" in xml_content


def test_export_multiple_recipes_empty_list(client):
    """Test exporting with empty recipe list returns error"""
    response = client.post("/api/recipes/export/beerxml", json=[])

    assert response.status_code == 400
    assert "No recipe IDs provided" in response.json()["detail"]


def test_export_multiple_recipes_invalid_ids(client):
    """Test exporting with all invalid IDs returns error"""
    response = client.post("/api/recipes/export/beerxml", json=[99998, 99999])

    assert response.status_code == 404
    assert "No recipes found" in response.json()["detail"]


def test_roundtrip_import_export(client, db_session):
    """Test importing a recipe and then exporting it maintains data integrity"""
    # Import a recipe
    files = {
        "file": ("test_recipe.xml", io.BytesIO(SAMPLE_BEERXML), "application/xml")
    }

    import_response = client.post("/api/recipes/import/beerxml", files=files)
    assert import_response.status_code == 200

    recipe_id = import_response.json()["recipe_ids"][0]

    # Export the same recipe
    export_response = client.get(f"/api/recipes/{recipe_id}/export/beerxml")
    assert export_response.status_code == 200

    exported_xml = export_response.content

    # Re-import the exported XML
    files2 = {
        "file": ("reimport.xml", io.BytesIO(exported_xml), "application/xml")
    }

    reimport_response = client.post("/api/recipes/import/beerxml", files=files2)
    assert reimport_response.status_code == 200

    reimport_data = reimport_response.json()
    assert reimport_data["imported_count"] == 1

    # Verify the re-imported recipe has the same data
    new_recipe_id = reimport_data["recipe_ids"][0]
    original_recipe = client.get(f"/api/recipes/{recipe_id}").json()
    new_recipe = client.get(f"/api/recipes/{new_recipe_id}").json()

    # Compare key fields (excluding IDs and auto-generated fields)
    assert original_recipe["name"] == new_recipe["name"]
    assert original_recipe["type"] == new_recipe["type"]
    assert original_recipe["brewer"] == new_recipe["brewer"]
    assert original_recipe["batch_size"] == new_recipe["batch_size"]
    assert len(original_recipe["hops"]) == len(new_recipe["hops"])
    assert len(original_recipe["fermentables"]) == len(new_recipe["fermentables"])


def test_import_beerxml_with_special_characters(client, db_session):
    """Test importing recipes with special characters in names and notes"""
    special_chars_xml = b"""<?xml version="1.0" encoding="utf-8"?>
<RECIPE>
 <NAME>Recipe with &amp; Special &lt;Characters&gt;</NAME>
 <VERSION>1</VERSION>
 <BATCH_SIZE>20.0</BATCH_SIZE>
 <NOTES>Notes with "quotes" and 'apostrophes'</NOTES>
</RECIPE>
"""

    files = {
        "file": ("special.xml", io.BytesIO(special_chars_xml), "application/xml")
    }

    response = client.post("/api/recipes/import/beerxml", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["imported_count"] == 1

    recipe_id = data["recipe_ids"][0]
    recipe = client.get(f"/api/recipes/{recipe_id}").json()

    assert "Special <Characters>" in recipe["name"]
    assert "quotes" in recipe["notes"]


@pytest.fixture
def sample_recipe(client, db_session):
    """Create a sample recipe for testing export"""
    recipe_data = {
        "name": "Test Export Recipe",
        "version": 1,
        "type": "All Grain",
        "brewer": "Test Brewer",
        "batch_size": 20.0,
        "boil_size": 25.0,
        "boil_time": 60,
        "efficiency": 75.0,
        "hops": [
            {
                "name": "Cascade",
                "alpha": 5.5,
                "amount": 1.5,
                "use": "Boil",
                "time": 60,
                "form": "Pellet",
            }
        ],
        "fermentables": [
            {
                "name": "Pale Malt",
                "type": "Grain",
                "amount": 5.0,
                "yield_": 78.0,
                "color": 2.5,
            }
        ],
        "yeasts": [
            {
                "name": "US-05",
                "type": "Ale",
                "form": "Dry",
                "attenuation": 75.0,
            }
        ],
        "miscs": [
            {
                "name": "Irish Moss",
                "type": "Fining",
                "use": "Boil",
                "time": 10,
            }
        ],
    }

    response = client.post("/api/recipes", json=recipe_data)
    assert response.status_code == 200
    return response.json()
