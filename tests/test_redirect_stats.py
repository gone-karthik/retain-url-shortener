import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_redirect_and_stats(client):
    resp1 = client.post("/api/shorten", json={"url": "http://example.com"})
    code = resp1.get_json()["short_code"]

    resp2 = client.get(f"/{code}")
    assert resp2.status_code in (301, 302)

    resp3 = client.get(f"/{code}", follow_redirects=True)
    assert b"example.com" in resp3.data

    resp4 = client.get(f"/api/stats/{code}")
    stats = resp4.get_json()
    assert stats["url"] == "http://example.com"
    assert stats["clicks"] == 1
    assert "created_at" in stats

def test_stats_unknown_code(client):
    resp = client.get("/api/stats/xxxxxx")
    assert resp.status_code == 404
