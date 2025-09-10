from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_crud_flow():
    # Initially empty
    resp = client.get("/api/items/")
    assert resp.status_code == 200
    assert resp.json() == []

    # Create item
    payload = {"name": "Sample", "description": "Test item"}
    resp = client.post("/api/items/", json=payload)
    assert resp.status_code == 201
    created = resp.json()
    assert created["id"] >= 1
    assert created["name"] == payload["name"]
    assert created["description"] == payload["description"]

    item_id = created["id"]

    # Get item
    resp = client.get(f"/api/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json() == created

    # Update item
    update_payload = {"description": "Updated"}
    resp = client.patch(f"/api/items/{item_id}", json=update_payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["description"] == "Updated"

    # Delete item
    resp = client.delete(f"/api/items/{item_id}")
    assert resp.status_code == 204

    # Not found after delete
    resp = client.get(f"/api/items/{item_id}")
    assert resp.status_code == 404
