from fastapi import status
from httpx import AsyncClient

from common_test.security import login
from domain.ledger.category.item.dto import CreateItemDto, EditItemDto
from domain.member.dto import LoginFormDTO
import pytest

"""
성공 케이스
"""

@pytest.mark.anyio
async def test_create_item(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.post("/ledger/item/", json=CreateItemDto(
        category_id=1,
        item_name='Test Item',
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.anyio
async def test_update_item(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.put("/ledger/item/", json=EditItemDto(
        organization_id=1,
        category_id=1,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_delete_item(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.delete("/ledger/item/", params={
        "organization_id":1,
        "category_id":1,
        "item_id":3
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

"""
실패 케이스
"""

# not joined organization
@pytest.mark.anyio
async def test_create_item_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user6@user.com', password='password'))
    response = await client.post("/ledger/item/", json=CreateItemDto(
        category_id=1,
        item_name='Test Item',
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# not related category_id
@pytest.mark.anyio
async def test_create_item_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.post("/ledger/item/", json=CreateItemDto(
        category_id=5,
        item_name='Test Item',
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# no data
@pytest.mark.anyio
async def test_create_item_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.post("/ledger/item/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization
@pytest.mark.anyio
async def test_create_item_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.post("/ledger/item/", json=CreateItemDto(
        category_id=1,
        item_name='Test Item',
        organization_id=100,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist category
@pytest.mark.anyio
async def test_create_item_fail5(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.post("/ledger/item/", json=CreateItemDto(
        category_id=100,
        item_name='Test Item',
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong year
@pytest.mark.anyio
async def test_create_item_fail6(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.post("/ledger/item/", json=CreateItemDto(
        category_id=100,
        item_name='Test Item',
        organization_id=1,
        year=2000
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not exist item id
@pytest.mark.anyio
async def test_update_item_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.put("/ledger/item/", json=EditItemDto(
        organization_id=1,
        category_id=1,
        item_id=100,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist organization id
@pytest.mark.anyio
async def test_update_item_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.put("/ledger/item/", json=EditItemDto(
        organization_id=100,
        category_id=1,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist category id
@pytest.mark.anyio
async def test_update_item_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.put("/ledger/item/", json=EditItemDto(
        organization_id=1,
        category_id=100,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong organization id
@pytest.mark.anyio
async def test_update_item_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.put("/ledger/item/", json=EditItemDto(
        organization_id=2,
        category_id=1,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong category id
@pytest.mark.anyio
async def test_update_item_fail5(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.put("/ledger/item/", json=EditItemDto(
        organization_id=1,
        category_id=2,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong item id
@pytest.mark.anyio
async def test_update_item_fail6(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.put("/ledger/item/", json=EditItemDto(
        organization_id=1,
        category_id=1,
        item_id=4,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# no data
@pytest.mark.anyio
async def test_update_item_fail7(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.put("/ledger/item/", json=EditItemDto(
        organization_id=1,
        category_id=1,
        item_id=4,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not allowed user
@pytest.mark.anyio
async def test_update_item_fail8(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user4@user.com', password='password'))
    response = await client.put("/ledger/item/", json=EditItemDto(
        organization_id=1,
        category_id=1,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# delete item that has receipts
@pytest.mark.anyio
async def test_delete_item_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.delete("/ledger/item/", params={
        "organization_id":1,
        "category_id":1,
        "item_id":1
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not exist organization
@pytest.mark.anyio
async def test_delete_item_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.delete("/ledger/item/", params={
        "organization_id":100,
        "category_id":1,
        "item_id":1
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist category
@pytest.mark.anyio
async def test_delete_item_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.delete("/ledger/item/", params={
        "organization_id":1,
        "category_id":100,
        "item_id":1
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist item
@pytest.mark.anyio
async def test_delete_item_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.delete("/ledger/item/", params={
        "organization_id":1,
        "category_id":1,
        "item_id":100
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# no data
@pytest.mark.anyio
async def test_delete_item_fail5(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = await client.delete("/ledger/item/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not allowed user
@pytest.mark.anyio
async def test_delete_item_fail6(client: AsyncClient):
    await login(client, LoginFormDTO(email='test_user4@user.com', password='password'))
    response = await client.delete("/ledger/item/", params={
        "organization_id":1,
        "category_id":1,
        "item_id":1
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN