import Database.Models as models


def test_styles_endpoint_returns_seeded_style(client, db_session):
    style = models.Styles(
        name="Test Style",
        category="Test Category",
        type="Ale",
    )
    db_session.add(style)
    db_session.commit()
    db_session.refresh(style)

    response = client.get("/styles")
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, list)
    assert any(
        item["id"] == style.id and item["name"] == "Test Style" for item in payload
    )
