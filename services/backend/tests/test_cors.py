"""
Test CORS headers are present in responses, including error responses.
"""


def test_cors_headers_on_successful_request(client):
    """Test that CORS headers are present on successful requests"""
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_cors_headers_on_404_error(client):
    """Test that CORS headers are present on 404 errors"""
    response = client.get(
        "/nonexistent-endpoint", headers={"Origin": "http://localhost:3000"}
    )
    assert response.status_code == 404
    # CORS middleware should add headers even for 404 errors
    assert "access-control-allow-origin" in response.headers


def test_cors_headers_not_added_for_unknown_origin(client):
    """Test that CORS headers are not added for origins not in the allowlist"""
    response = client.get("/", headers={"Origin": "http://evil-site.com"})
    assert response.status_code == 200
    # Origin not in the allowed list, so no CORS header should be present
    # or it should be different
    if "access-control-allow-origin" in response.headers:
        assert response.headers["access-control-allow-origin"] != "http://evil-site.com"


def test_preflight_cors_request(client):
    """Test that preflight OPTIONS requests are handled correctly"""
    response = client.options(
        "/batches",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
