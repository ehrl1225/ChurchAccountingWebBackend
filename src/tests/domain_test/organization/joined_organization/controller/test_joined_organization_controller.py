from fastapi.testclient import TestClient
from fastapi import status

from common.database import MemberRole
from common_test.security import login
from domain.member.dto import LoginFormDTO
from domain.organization.joined_organization.dto import ChangeRoleDto

"""
성공 케이스
"""

def test_change_role(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/joined-organization/1", json=ChangeRoleDto(
        member_id=3,
        member_role=MemberRole.ADMIN,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_200_OK

def test_get_all(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/joined-organization")
    assert response.status_code == status.HTTP_200_OK

def test_delete_joined_organization(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/joined-organization", params={
        "organization_id": 1,
        "joined_organization_id": 2,
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

"""
실패 케이스
"""

# changing to OWNER is forbidden
def test_change_role_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/joined-organization/1", json=ChangeRoleDto(
        member_id=3,
        member_role=MemberRole.OWNER,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# changing not exist member
def test_change_role_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/joined-organization/1", json=ChangeRoleDto(
        member_id=100,
        member_role=MemberRole.READ_ONLY,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# changing OWNER to other is forbidden
def test_change_role_fail3(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/joined-organization/1", json=ChangeRoleDto(
        member_id=2,
        member_role=MemberRole.READ_ONLY,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# wrong organization
def test_delete_joined_organization_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user3@user.com", password="password"))
    response = client.delete("/joined-organization", params={
        "organization_id": 1,
        "joined_organization_id": 2,
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

# wrong joined organization
def test_delete_joined_organization_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/joined-organization", params={
        "organization_id": 1,
        "joined_organization_id": 12,
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN