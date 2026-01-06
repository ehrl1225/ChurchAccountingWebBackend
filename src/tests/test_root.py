from fastapi.testclient import TestClient
from httpx import AsyncClient

from common.env import settings
import pytest


@pytest.mark.anyio
async def test_read_root(client:AsyncClient):
    response = await client.get("/")
    assert settings.PROFILE == "test"
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}