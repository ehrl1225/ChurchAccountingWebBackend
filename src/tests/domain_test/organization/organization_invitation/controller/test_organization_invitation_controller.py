from fastapi.testclient import TestClient
from fastapi import status

from common_test.security import login
from domain.member.dto import LoginFormDTO
from domain.organization.organization_invitation.dto import CreateOrganizationInvitationDto


def test_create_organization_invitation(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/organization-invitation", json=CreateOrganizationInvitationDto(
        organization_id=1,
        email="admin@admin.com"
    ).model_dump())
    assert response.status_code == status.HTTP_201_CREATED

def test_update_organization_invitation(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.put("/organization-invitation/4/{status}?status_literal=accept")
    assert response.status_code == status.HTTP_200_OK

def test_get_organization_invitation(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.get("/organization-invitation")
    assert response.status_code == status.HTTP_200_OK