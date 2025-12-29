from fastapi.testclient import TestClient
from fastapi import status

from common_test.security import login
from domain.ledger.category.item.dto import CreateItemDto, EditItemDto
from domain.member.dto import LoginFormDTO

"""
성공 케이스
"""

def test_create_item(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.post("/ledger/item", json=CreateItemDto(
        category_id=1,
        item_name='Test Item',
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

def test_update_item(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.put("/ledger/item", json=EditItemDto(
        organization_id=1,
        category_id=1,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_200_OK

def test_delete_item(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.delete("/ledger/item", params={
        "organization_id":1,
        "category_id":1,
        "item_id":3
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

"""
실패 케이스
"""

# not joined organization
def test_create_item_fail1(client: TestClient):
    login(client, LoginFormDTO(email='test_user6@user.com', password='password'))
    response = client.post("/ledger/item", json=CreateItemDto(
        category_id=1,
        item_name='Test Item',
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# not related category_id
def test_create_item_fail2(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.post("/ledger/item", json=CreateItemDto(
        category_id=5,
        item_name='Test Item',
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# no data
def test_create_item_fail3(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.post("/ledger/item")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization
def test_create_item_fail4(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.post("/ledger/item", json=CreateItemDto(
        category_id=1,
        item_name='Test Item',
        organization_id=100,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist category
def test_create_item_fail5(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.post("/ledger/item", json=CreateItemDto(
        category_id=100,
        item_name='Test Item',
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist item id
def test_update_item_fail1(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.put("/ledger/item", json=EditItemDto(
        organization_id=1,
        category_id=1,
        item_id=100,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist organization id
def test_update_item_fail2(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.put("/ledger/item", json=EditItemDto(
        organization_id=100,
        category_id=1,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist category id
def test_update_item_fail3(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.put("/ledger/item", json=EditItemDto(
        organization_id=1,
        category_id=100,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong organization id
def test_update_item_fail4(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.put("/ledger/item", json=EditItemDto(
        organization_id=2,
        category_id=1,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong category id
def test_update_item_fail5(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.put("/ledger/item", json=EditItemDto(
        organization_id=1,
        category_id=2,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong item id
def test_update_item_fail6(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.put("/ledger/item", json=EditItemDto(
        organization_id=1,
        category_id=1,
        item_id=4,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# no data
def test_update_item_fail7(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.put("/ledger/item", json=EditItemDto(
        organization_id=1,
        category_id=1,
        item_id=4,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not allowed user
def test_update_item_fail8(client: TestClient):
    login(client, LoginFormDTO(email='test_user4@user.com', password='password'))
    response = client.put("/ledger/item", json=EditItemDto(
        organization_id=1,
        category_id=1,
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# delete item that has receipts
def test_delete_item_fail1(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.delete("/ledger/item", params={
        "organization_id":1,
        "category_id":1,
        "item_id":1
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not exist organization
def test_delete_item_fail2(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.delete("/ledger/item", params={
        "organization_id":100,
        "category_id":1,
        "item_id":1
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist category
def test_delete_item_fail3(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.delete("/ledger/item", params={
        "organization_id":1,
        "category_id":100,
        "item_id":1
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist item
def test_delete_item_fail4(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.delete("/ledger/item", params={
        "organization_id":1,
        "category_id":1,
        "item_id":100
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# no data
def test_delete_item_fail5(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.delete("/ledger/item")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not allowed user
def test_delete_item_fail6(client: TestClient):
    login(client, LoginFormDTO(email='test_user4@user.com', password='password'))
    response = client.delete("/ledger/item", params={
        "organization_id":1,
        "category_id":1,
        "item_id":1
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN