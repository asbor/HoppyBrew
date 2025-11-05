def build_inventory_payload(overrides=None):
    payload = {
        "name": "Test Yeast",
        "type": "Ale",
        "form": "Dry",
        "amount": 1.5,
        "amount_is_weight": False,
        "laboratory": "Test Lab",
        "product_id": "123",
        "min_temperature": 18.0,
        "max_temperature": 24.0,
        "flocculation": "Medium",
        "attenuation": 75.0,
        "notes": "Clean profile",
        "best_for": "Pale ales",
        "times_cultured": 2,
        "max_reuse": 5,
        "add_to_secondary": False,
    }
    if overrides:
        payload.update(overrides)
    return payload


def test_inventory_yeast_crud_flow(client):
    create_resp = client.post("/inventory/yeasts", json=build_inventory_payload())
    assert create_resp.status_code == 200
    created = create_resp.json()

    detail_resp = client.get(f"/inventory/yeasts/{created['id']}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["name"] == "Test Yeast"

    list_resp = client.get("/inventory/yeasts")
    assert list_resp.status_code == 200
    assert any(item["id"] == created["id"] for item in list_resp.json())

    update_resp = client.put(
        f"/inventory/yeasts/{created['id']}",
        json=build_inventory_payload({"name": "Updated Yeast"}),
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Updated Yeast"

    delete_resp = client.delete(f"/inventory/yeasts/{created['id']}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["name"] == "Updated Yeast"

    missing = client.get(f"/inventory/yeasts/{created['id']}")
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Yeast not found"


def test_get_inventory_yeast_not_found_returns_404(client):
    response = client.get("/inventory/yeasts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Yeast not found"
