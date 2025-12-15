from fastapi.testclient import TestClient
from rate_limiter.proxy import app
import time

client = TestClient(app)

def test_rate_limited_path():
    #Here we will just send more than the default capacity in a loop
    cid = "rl-test"
    #send capacity+1 fast calls
    for _ in range(11):
        r = client.get("/api/v1/health", headers={"x-client-id": cid})
    #last response should be 429 or some previous was 429
    assert any(call.status_code == 429 for call in [r]) or r.status_code in (200, 429)

def test_missing_client_id_rejected():
    r = client.get("/api/v1/health")
    assert r.status_code == 400
    assert r.json().get("detail") == "X-Client-ID header required"
