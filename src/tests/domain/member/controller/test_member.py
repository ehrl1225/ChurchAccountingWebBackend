from fastapi.testclient import TestClient
from fastapi import status

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

