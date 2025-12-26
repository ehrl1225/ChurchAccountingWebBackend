from fastapi.testclient import TestClient
from fastapi import status
from common_test.security import login
from domain.member.dto import LoginFormDTO
from domain.organization.organization.dto import OrganizationRequestDto


def test_create_organization(client: TestClient):
    login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = client.post("/organization", json=OrganizationRequestDto(
        name="organization1",
        description="description1",
        start_year=2020,
        end_year=2020
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED


def test_update_organization(client: TestClient):
    login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = client.put("/organization/1", json=OrganizationRequestDto(
        name="organization-1",
        description="description-1",
        start_year=2020,
        end_year=2020
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_202_ACCEPTED

def test_delete_organization(client: TestClient):
    login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = client.delete("/organization/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
