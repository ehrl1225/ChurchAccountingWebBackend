from fastapi.testclient import TestClient
from common.env import settings


def test_read_root(client:TestClient):
    response = client.get("/")
    assert settings.PROFILE == "test"
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}