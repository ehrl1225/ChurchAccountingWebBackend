from fastapi.testclient import TestClient
from fastapi import status

from common_test.security import login
from domain.member.dto import LoginFormDTO
from domain.organization.organization_invitation.dto import CreateOrganizationInvitationDto

"""
성공 케이스
"""

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

"""
실패 케이스
"""

# not exist email
def test_create_organization_invitation_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/organization-invitation", json=CreateOrganizationInvitationDto(
        organization_id=1,
        email="admin123@admin123.com"
    ).model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist organization id
def test_create_organization_invitation_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/organization-invitation", json=CreateOrganizationInvitationDto(
        organization_id=10,
        email="admin@admin.com"
    ).model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# no data
def test_create_organization_invitation_fail3(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/organization-invitation")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# inviting self is forbidden
def test_create_organization_invitation_fail4(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/organization-invitation", json=CreateOrganizationInvitationDto(
        organization_id=1,
        email="test_user0@user.com"
    ).model_dump())
    assert response.status_code == status.HTTP_403_FORBIDDEN

# wrong data
def test_update_organization_invitation_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.put("/organization-invitation/4/{status}?status_literal=aaa")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# wrong invitation_code
def test_update_organization_invitation_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.put("/organization-invitation/5/{status}?status_literal=accept")
    assert response.status_code == status.HTTP_403_FORBIDDEN
