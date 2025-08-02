import re
from app.main import app
import pytest

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_shorten_valid_url(client):
    resp = client.post("/api/shorten", json={"url": "https://example.com/foo"})
    assert resp.status_code == 201, resp.data
    body = resp.get_json()
    assert "short_code" in body and "short_url" in body
    code = body["short_code"]
    assert len(code) == 6 and re.fullmatch(r"[A-Za-z0-9]{6}", code)

def test_shorten_invalid_url(client):
    resp = client.post("/api/shorten", json={"url": "not-a-url"})
    assert resp.status_code == 400
