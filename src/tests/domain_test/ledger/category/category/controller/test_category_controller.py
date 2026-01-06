import pytest
from fastapi import status
from httpx import AsyncClient

from common.database import TxType
from common_test.security import login
from domain.ledger.category.category.dto import CreateCategoryDTO, DeleteCategoryParams
from domain.ledger.category.category.dto.edit_category_dto import EditCategoryDto
from domain.member.dto import LoginFormDTO

"""
성공 케이스
"""

@pytest.mark.asyncio
async def test_create_category(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/category/", json=CreateCategoryDTO(
        category_name="Test",
        item_name=None,
        tx_type=TxType.INCOME,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_create_category_and_item(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/category/", json=CreateCategoryDTO(
        category_name="Test",
        item_name="Test Item",
        tx_type=TxType.INCOME,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/category/",params={
        "organization_id": 1,
        "year": 2025,
        "tx_type": TxType.INCOME.value,
    })
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_update_category(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/category/",json=EditCategoryDto(
        organization_id=1,
        category_id=1,
        category_name="test_category"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_202_ACCEPTED

@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/category/", params={
        "organization_id": 1,
        "category_id": 4,
    })
    assert response.status_code == status.HTTP_202_ACCEPTED

@pytest.mark.asyncio
async def test_delete_category_and_item(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/category/", params={
        "organization_id": 1,
        "category_id": 3,
    })
    assert response.status_code == status.HTTP_202_ACCEPTED

"""
실패 케이스
"""

# not exist organization_id
@pytest.mark.asyncio
async def test_create_category_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/category/", json=CreateCategoryDTO(
        category_name="Test",
        item_name=None,
        tx_type=TxType.INCOME,
        organization_id=100,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not own organization
@pytest.mark.asyncio
async def test_create_category_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.post("/ledger/category/", json=CreateCategoryDTO(
        category_name="Test",
        item_name=None,
        tx_type=TxType.INCOME,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# not available year
@pytest.mark.asyncio
async def test_create_category_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/category/", json=CreateCategoryDTO(
        category_name="Test",
        item_name=None,
        tx_type=TxType.INCOME,
        organization_id=1,
        year=2020
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# no data
@pytest.mark.asyncio
async def test_create_category_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/category/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# no data
@pytest.mark.asyncio
async def test_get_categories_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/category/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization id
@pytest.mark.asyncio
async def test_get_categories_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/category/",params={
        "organization_id": 100,
        "year": 2025,
        "tx_type": TxType.INCOME.value,
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not own organization
@pytest.mark.asyncio
async def test_get_categories_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.get("/ledger/category/",params={
        "organization_id": 1,
        "year": 2025,
        "tx_type": TxType.INCOME.value,
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

# not exist TX type
@pytest.mark.asyncio
async def test_get_categories_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/category/",params={
        "organization_id": 1,
        "year": 2025,
        "tx_type": "wrong",
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# no data
@pytest.mark.asyncio
async def test_update_category_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/category/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization_id
@pytest.mark.asyncio
async def test_update_category_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/category/", json=EditCategoryDto(
        organization_id=100,
        category_id=1,
        category_name="test_category"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong organization id
@pytest.mark.asyncio
async def test_update_category_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.put("/ledger/category/", json=EditCategoryDto(
        organization_id=1,
        category_id=1,
        category_name="test_category"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# not exist category id
@pytest.mark.asyncio
async def test_update_category_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/category/", json=EditCategoryDto(
        organization_id=1,
        category_id=12,
        category_name="test_category"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong organization id
@pytest.mark.asyncio
async def test_update_category_fail5(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.put("/ledger/category/", json=EditCategoryDto(
        organization_id=1,
        category_id=1,
        category_name="test_category"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# can't delete category with receipts
@pytest.mark.asyncio
async def test_delete_category_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/category/", params={
        "organization_id": 1,
        "category_id": 1,
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# no data
@pytest.mark.asyncio
async def test_delete_category_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/category/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not own category
@pytest.mark.asyncio
async def test_delete_category_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response =await client.delete("/ledger/category/", params={
        "organization_id": 2,
        "category_id": 3,
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND