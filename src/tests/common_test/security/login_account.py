from fastapi.testclient import TestClient
from httpx import AsyncClient
from starlette import status
import pytest

from domain.member.dto import LoginFormDTO

async def login(client: AsyncClient, login_form:LoginFormDTO):
    response = await client.post("/member/login", json=login_form.model_dump(mode="json"))
    assert response.status_code == status.HTTP_200_OK
    client.cookies.set("access_token", response.cookies["access_token"])
    client.cookies.set("refresh_token", response.cookies["refresh_token"])
    return response