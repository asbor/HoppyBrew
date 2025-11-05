import pytest
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_create_fermentable(client):
    response = client.post(
        "/inventory/fermentables",
        json={
            "name": "Test Fermentable",
            "type": "Grain",
            "yield_": 75.0,
            "color": 10,
            "origin": "USA",
            "supplier": "Test Supplier",
            "notes": "Test Notes",
            "potential": 1.037,
            "amount": 5.0,
            "cost_per_unit": 1.5,
            "manufacturing_date": "2024-01-01",
            "expiry_date": "2025-01-01",
            "lot_number": "12345",
            "exclude_from_total": False,
            "not_fermentable": False,
            "description": "Test Description",
            "substitutes": "Test Substitutes",
            "used_in": "Test Used In",
        },
    )

    # Print the response for debugging
    print(response.json())

    assert response.status_code == 200, f'''
    Unexpected status code: {response.status_code},
    response: {response.json()}'''

    fermentable = response.json()
    assert fermentable["name"] == "Test Fermentable"
    assert fermentable["type"] == "Grain"
    assert fermentable["yield_"] == 75.0
    assert fermentable["color"] == 10
    assert fermentable["origin"] == "USA"
    assert fermentable["supplier"] == "Test Supplier"
    assert fermentable["notes"] == "Test Notes"
    # Allowing a small margin for float comparison
    assert fermentable["potential"] == pytest.approx(1.037, abs=1e-3)
