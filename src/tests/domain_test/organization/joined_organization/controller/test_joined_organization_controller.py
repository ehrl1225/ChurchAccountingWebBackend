from fastapi.testclient import TestClient
from fastapi import status

from common.database import MemberRole
from common_test.security import login
from domain.member.dto import LoginFormDTO
from domain.member.entity import Member
from domain.organization.joined_organization.dto import ChangeRoleDto


def test_change_role(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/joined-organization/1", json=ChangeRoleDto(
        member_id=3,
        member_role=MemberRole.ADMIN,
    ).model_dump())
    assert response.status_code == status.HTTP_200_OK

def test_get_all(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/joined-organization")
    assert response.status_code == status.HTTP_200_OK