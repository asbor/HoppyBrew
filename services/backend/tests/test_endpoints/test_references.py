import io
import Database.Models as models


def mock_favicon_url(url):
    return "http://mock.local/favicon.ico"


def test_create_and_get_reference(client, monkeypatch):
    monkeypatch.setattr("api.endpoints.references.fetch_favicon", mock_favicon_url)
    payload = {
        "name": "Example Reference",
        "url": "http://example.com",
        "description": "Sample description",
        "category": "Docs",
    }
    create_resp = client.post("/references", json=payload)
    assert create_resp.status_code == 200, create_resp.text
    created = create_resp.json()

    assert created["favicon_url"] == "http://mock.local/favicon.ico"

    detail_resp = client.get(f"/references/{created['id']}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["name"] == "Example Reference"


def test_import_references_creates_records(client, db_session, monkeypatch):
    monkeypatch.setattr("api.endpoints.references.fetch_favicon", mock_favicon_url)
    xml_content = b"""
        <references>
            <reference>
                <name>Imported Ref</name>
                <url>http://imported.com</url>
                <description>Imported description</description>
                <category>Brew</category>
            </reference>
        </references>
    """
    files = {"file": ("refs.xml", io.BytesIO(xml_content), "application/xml")}

    response = client.post("/references/import", files=files)
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data["message"] == "References imported successfully"
    assert "imported_records" in response_data
    assert "skipped_records" in response_data

    stored = db_session.query(models.References).all()
    assert len(stored) == 1
    assert stored[0].name == "Imported Ref"
    assert stored[0].favicon_url == "http://mock.local/favicon.ico"


def test_export_references_returns_xml(client, monkeypatch):
    monkeypatch.setattr("api.endpoints.references.fetch_favicon", mock_favicon_url)
    client.post(
        "/references",
        json={
            "name": "Export Ref",
            "url": "http://export.com",
            "description": "Exportable",
            "category": "Docs",
        },
    )

    response = client.get("/references/export")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"] == "attachment; filename=references.xml"
    )

    xml_text = response.content.decode("utf-8")
    assert "<name>Export Ref</name>" in xml_text
    assert "<url>http://export.com</url>" in xml_text


def test_reference_not_found_returns_404(client):
    response = client.get("/references/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Reference not found"
