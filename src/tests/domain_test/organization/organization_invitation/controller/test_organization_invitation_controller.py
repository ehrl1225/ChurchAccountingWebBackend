from httpx import AsyncClient
from fastapi import status
import pytest

from common_test.security import login
from domain.member.dto import LoginFormDTO
from domain.organization.organization_invitation.dto import CreateOrganizationInvitationDto

"""
성공 케이스
"""
@pytest.mark.asyncio
async def test_create_organization_invitation(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/organization-invitation/", json=CreateOrganizationInvitationDto(
        organization_id=1,
        email="admin@admin.com"
    ).model_dump())
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_update_organization_invitation(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.put("/organization-invitation/4/{status}?status_literal=accept")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_get_organization_invitation(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.get("/organization-invitation/")
    assert response.status_code == status.HTTP_200_OK

"""
실패 케이스
"""

# not exist email
@pytest.mark.asyncio
async def test_create_organization_invitation_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/organization-invitation/", json=CreateOrganizationInvitationDto(
        organization_id=1,
        email="admin123@admin123.com"
    ).model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist organization id
@pytest.mark.asyncio
async def test_create_organization_invitation_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/organization-invitation/", json=CreateOrganizationInvitationDto(
        organization_id=10,
        email="admin@admin.com"
    ).model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# no data
@pytest.mark.asyncio
async def test_create_organization_invitation_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/organization-invitation/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# inviting self is forbidden
@pytest.mark.asyncio
async def test_create_organization_invitation_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/organization-invitation/", json=CreateOrganizationInvitationDto(
        organization_id=1,
        email="test_user0@user.com"
    ).model_dump())
    assert response.status_code == status.HTTP_403_FORBIDDEN

# wrong data
@pytest.mark.asyncio
async def test_update_organization_invitation_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.put("/organization-invitation/4/{status}?status_literal=aaa")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# wrong invitation_code
@pytest.mark.asyncio
async def test_update_organization_invitation_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.put("/organization-invitation/5/{status}?status_literal=accept")
    assert response.status_code == status.HTTP_403_FORBIDDEN
