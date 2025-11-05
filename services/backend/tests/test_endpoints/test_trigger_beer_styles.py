def test_trigger_beer_styles_runs_background_task(client, monkeypatch):
    calls = {"count": 0}

    def fake_scrape():
        calls["count"] += 1

    monkeypatch.setattr(
        "api.endpoints.trigger_beer_styles_processing.scrape_and_process_beer_styles",
        fake_scrape,
    )

    response = client.post("/refresh-beer-styles")
    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert "task_id" in response_data  # Task ID is now returned
    assert calls["count"] == 1
