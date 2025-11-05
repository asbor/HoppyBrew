import Database.Models as models


def build_guideline_payload(overrides=None):
    payload = {
        "block_heading": "Amber Ale",
        "circle_image": "http://example.com/image.png",
        "category": "Ale",
        "color": "Amber",
        "clarity": "Clear",
        "perceived_malt_and_aroma": "Malty aroma",
        "perceived_hop_and_aroma": "Balanced hops",
        "perceived_bitterness": "Moderate",
        "fermentation_characteristics": "Clean",
        "body": "Medium",
        "additional_notes": "Serve cold",
        "og": "1.050",
        "fg": "1.010",
        "abv": "5.5%",
        "ibu": "30",
        "ebc": "15",
    }
    if overrides:
        payload.update(overrides)
    return payload


def test_style_guideline_crud_flow(client, db_session):
    create_resp = client.post("/style_guidelines", json=build_guideline_payload())
    assert create_resp.status_code == 200, create_resp.text

    guideline = db_session.query(models.StyleGuidelines).one()
    guideline_id = guideline.id

    list_resp = client.get("/style_guidelines")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    detail_resp = client.get(f"/style_guidelines/{guideline_id}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["category"] == "Ale"

    update_resp = client.put(
        f"/style_guidelines/{guideline_id}",
        json=build_guideline_payload({"category": "Updated"}),
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["category"] == "Updated"

    delete_resp = client.delete(f"/style_guidelines/{guideline_id}")
    assert delete_resp.status_code == 200

    missing = client.get(f"/style_guidelines/{guideline_id}")
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Style Guideline not found"


def test_style_guideline_not_found_returns_404(client):
    response = client.get("/style_guidelines/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Style Guideline not found"
