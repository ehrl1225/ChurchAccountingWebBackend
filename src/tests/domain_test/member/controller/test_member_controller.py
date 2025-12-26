from fastapi.testclient import TestClient
from fastapi import status

from domain.member.dto import RegisterFormDTO, LoginFormDTO

"""
성공 케이스
"""

def test_register_member(client: TestClient):
    response = client.post("/member/register", json=RegisterFormDTO(
        name="user1",
        email="user1@user.com",
        password="password",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

def test_login_member(client: TestClient):
    response = client.post("/member/login", json=LoginFormDTO(
        email="admin@admin.com",
        password="password"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_200_OK

def test_register_and_login(client: TestClient):
    response = client.post("/member/register", json=RegisterFormDTO(
        name="user1",
        email="user1@user.com",
        password="password",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post("/member/login", json=LoginFormDTO(
        email="user1@user.com",
        password="password"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_200_OK

def test_me(client: TestClient):
    response = client.post("/member/login", json=LoginFormDTO(
        email="admin@admin.com",
        password="password"
    ).model_dump(mode="json"))
    cookies = response.cookies
    client.cookies.set("refresh_token", cookies["refresh_token"])
    response = client.get("/member/me")
    assert response.status_code == status.HTTP_200_OK

"""
실패 케이스
"""

# not email type
def test_register_fail1(client: TestClient):
    response = client.post("/member/register", json={
        "name": "user1",
        "email": "user1",
        "password": "password"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# no data
def test_register_fail2(client: TestClient):
    response = client.post("/member/register", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# already exist account
def test_register_fail3(client: TestClient):
    response = client.post("/member/register", json=RegisterFormDTO(
        name="admin",
        email="admin@admin.com",
        password="password"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not exist account
def test_login_fail1(client: TestClient):
    response = client.post("/member/login", json=LoginFormDTO(
        email="user1",
        password="password"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Incorrect email or password"

# no data
def test_login_fail2(client: TestClient):
    response = client.post("/member/login", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# wrong password
def test_login_fail3(client: TestClient):
    response = client.post("/member/login", json=LoginFormDTO(
        email="admin@admin.com",
        password="password2"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST