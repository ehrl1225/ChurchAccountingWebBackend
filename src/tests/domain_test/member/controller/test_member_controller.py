from httpx import AsyncClient
from fastapi import status
import pytest
from domain.member.dto import RegisterFormDTO, LoginFormDTO

"""
성공 케이스
"""

@pytest.mark.asyncio
async def test_register_member(client: AsyncClient):
    response = await client.post("/member/register", json=RegisterFormDTO(
        name="user1",
        email="user1@user.com",
        password="password",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_login_member(client: AsyncClient):
    response = await client.post("/member/login", json=LoginFormDTO(
        email="admin@admin.com",
        password="password"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    response = await client.post("/member/register", json=RegisterFormDTO(
        name="user1",
        email="user1@user.com",
        password="password",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED
    response = await client.post("/member/login", json=LoginFormDTO(
        email="user1@user.com",
        password="password"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_me(client: AsyncClient):
    response = await client.post("/member/login", json=LoginFormDTO(
        email="admin@admin.com",
        password="password"
    ).model_dump(mode="json"))
    cookies = response.cookies
    client.cookies.set("refresh_token", cookies["refresh_token"])
    response = await client.get("/member/me")
    assert response.status_code == status.HTTP_200_OK

"""
실패 케이스
"""

# not email type
@pytest.mark.asyncio
async def test_register_fail1(client: AsyncClient):
    response = await client.post("/member/register", json={
        "name": "user1",
        "email": "user1",
        "password": "password"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# no data
@pytest.mark.asyncio
async def test_register_fail2(client: AsyncClient):
    response = await client.post("/member/register", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# already exist account
@pytest.mark.asyncio
async def test_register_fail3(client: AsyncClient):
    response = await client.post("/member/register", json=RegisterFormDTO(
        name="admin",
        email="admin@admin.com",
        password="password"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not exist account
@pytest.mark.asyncio
async def test_login_fail1(client: AsyncClient):
    response = await client.post("/member/login", json=LoginFormDTO(
        email="user1",
        password="password"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Incorrect email or password"

# no data
@pytest.mark.asyncio
async def test_login_fail2(client: AsyncClient):
    response = await client.post("/member/login", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# wrong password
@pytest.mark.asyncio
async def test_login_fail3(client: AsyncClient):
    response = await client.post("/member/login", json=LoginFormDTO(
        email="admin@admin.com",
        password="password2"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST