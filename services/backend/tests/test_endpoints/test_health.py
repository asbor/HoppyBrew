def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "ok"
    assert "detail" in response_data  # May contain additional health info
