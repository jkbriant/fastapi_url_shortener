import pytest
from fastapi.testclient import TestClient
from main import app, url_mapping, url_reverse_mapping

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_mappings():
    url_mapping.clear()
    url_reverse_mapping.clear()

class TestShortenURL:
    def test_shorten_url(self, test_link: str):
        short_url_length = 6
        response = client.post("/api/shorten", json={"url": test_link})
        data = response.json()

        assert response.status_code == 201 # Created
        assert "short_url" in data
        assert data["long_url"] == test_link
        assert len(data["short_url"]) >= short_url_length