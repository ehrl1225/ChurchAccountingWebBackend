from fastapi.testclient import TestClient
from starlette import status

from domain.member.dto import LoginFormDTO


def login(client: TestClient, login_form:LoginFormDTO):
    response = client.post("/member/login", json=login_form.model_dump())
    assert response.status_code == status.HTTP_200_OK
    client.cookies.set("access_token", response.cookies["access_token"])
    client.cookies.set("refresh_token", response.cookies["refresh_token"])
    return response