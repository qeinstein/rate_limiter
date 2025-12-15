from fastapi.testclient import TestClient
from rate_limiter.proxy import app

client = TestClient(app)

def test_health():
    r = client.get("/api/v1/health", headers={"x-client-id": "t"})
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_items_crud_and_validation():
    #start empty
    r = client.get("/api/v1/items", headers={"x-client-id": "t"})
    assert r.status_code == 200
    assert r.json() == []

    #invalid post (price <= 0)
    r = client.post("/api/v1/items", json={"name": "a", "price": 0}, headers={"x-client-id": "t"})
    assert r.status_code == 422

    #valid post
    r = client.post("/api/v1/items", json={"name": "widget", "price": 9.99}, headers={"x-client-id": "t"})
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "widget"
    assert "id" in body
    assert "created_at" in body

    #list now has one
    r = client.get("/api/v1/items", headers={"x-client-id": "t"})
    assert r.status_code == 200
    arr = r.json()
    assert len(arr) >= 1
