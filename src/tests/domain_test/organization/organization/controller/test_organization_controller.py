from httpx import AsyncClient
from fastapi import status
from common_test.security import login
from domain.member.dto import LoginFormDTO
from domain.organization.organization.dto import OrganizationRequestDto
import pytest

"""
성공 케이스
"""
@pytest.mark.asyncio
async def test_create_organization(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = await client.post("/organization/", json=OrganizationRequestDto(
        name="organization1",
        description="description1",
        start_year=2020,
        end_year=2020
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_update_organization(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = await client.put("/organization/1", json=OrganizationRequestDto(
        name="organization-1",
        description="description-1",
        start_year=2020,
        end_year=2020
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_202_ACCEPTED

@pytest.mark.asyncio
async def test_delete_organization(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = await client.delete("/organization/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

"""
실패 케이스
"""

# wrong year
@pytest.mark.asyncio
async def test_create_organization_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = await client.post("/organization/", json=OrganizationRequestDto(
        name="organization1",
        description="description1",
        start_year=2020,
        end_year=2019
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# no data
@pytest.mark.asyncio
async def test_create_organization_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = await client.post("/organization/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization_id
@pytest.mark.asyncio
async def test_update_organization_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = await client.put("/organization/100", json=OrganizationRequestDto(
        name="organization-1",
        description="description-1",
        start_year=2020,
        end_year=2020
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong year
@pytest.mark.asyncio
async def test_update_organization_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = await client.put("/organization/1", json=OrganizationRequestDto(
        name="organization-1",
        description="description-1",
        start_year=2020,
        end_year=2019
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# wrong organization id
@pytest.mark.asyncio
async def test_update_organization_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user4@user.com',
        password='password'
    ))
    response = await client.put("/organization/1", json=OrganizationRequestDto(
        name="organization-1",
        description="description-1",
        start_year=2020,
        end_year=2020
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# no data
@pytest.mark.asyncio
async def test_update_organization_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user4@user.com',
        password='password'
    ))
    response = await client.put("/organization/1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# wrong organization id
@pytest.mark.asyncio
async def test_delete_organization_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user4@user.com',
        password='password'
    ))
    response = await client.delete("/organization/1")
    assert response.status_code == status.HTTP_403_FORBIDDEN

# not exist organization id
@pytest.mark.asyncio
async def test_delete_organization_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(
        email='test_user0@user.com',
        password='password'
    ))
    response = await client.delete("/organization/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND