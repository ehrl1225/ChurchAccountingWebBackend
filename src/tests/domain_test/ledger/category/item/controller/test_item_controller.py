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
        item_id=1,
        item_name='Test Item',
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_200_OK

def test_delete_item(client: TestClient):
    login(client, LoginFormDTO(email='test_user0@user.com', password='password'))
    response = client.delete("/ledger/item", params={
        "organization_id":1,
        "item_id":3
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

"""
실패 케이스
"""

