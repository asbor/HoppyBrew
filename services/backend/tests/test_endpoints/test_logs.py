from unittest.mock import mock_open, patch


def test_get_logs_returns_file_contents(client):
    with patch(
        "api.endpoints.logs.open", mock_open(read_data="log entry"), create=True
    ):
        response = client.get("/api/logs")

    assert response.status_code == 200
    assert response.json() == {"log_content": "log entry"}


def test_get_logs_missing_file_returns_500(client):
    with patch(
        "api.endpoints.logs.open",
        side_effect=FileNotFoundError("missing"),
        create=True,
    ):
        response = client.get("/api/logs")

    assert response.status_code == 500
    assert "Failed to read log file" in response.json()["detail"]
