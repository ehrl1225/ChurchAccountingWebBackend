from fastapi.testclient import TestClient
from fastapi import status

# 성공 케이스

def test_register_member(client: TestClient):
    response = client.post("/member/register", json={
        "name": "user1",
        "email": "user1@user.com",
        "password": "password",
    })
    assert response.status_code == status.HTTP_201_CREATED

def test_login_member(client: TestClient):
    response = client.post("/member/login", json={
        "email": "admin@admin.com",
        "password": "password",
    })
    assert response.status_code == status.HTTP_200_OK

# 실패 케이스

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
    response = client.post("/member/register", json={
        "name": "admin",
        "email": "admin@admin.com",
        "password": "password"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not exist account
def test_login_fail1(client: TestClient):
    response = client.post("/member/login", json={
        "email": "user1",
        "password": "password"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Incorrect email or password"

# no data
def test_login_fail2(client: TestClient):
    response = client.post("/member/login", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# wrong password
def test_login_fail3(client: TestClient):
    response = client.post("/member/login", json={
        "email": "admin@admin.com",
        "password": "password2"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST