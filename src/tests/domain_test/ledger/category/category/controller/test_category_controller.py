from fastapi.testclient import TestClient
from fastapi import status

from common.database import TxType
from common_test.security import login
from domain.ledger.category.category.dto import CreateCategoryDTO, DeleteCategoryParams
from domain.ledger.category.category.dto.edit_category_dto import EditCategoryDto
from domain.member.dto import LoginFormDTO


def test_create_category(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/category", json=CreateCategoryDTO(
        category_name="Test",
        item_name=None,
        tx_type=TxType.INCOME,
        organization_id=1,
        year=2020
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

def test_get_categories(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/ledger/category/",params={
        "organization_id": 1,
        "year": 2025,
        "tx_type": TxType.INCOME.value,
    })
    assert response.status_code == status.HTTP_200_OK

def test_update_category(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/category",json=EditCategoryDto(
        organization_id=1,
        category_id=1,
        category_name="test_category"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_202_ACCEPTED

def test_delete_category(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/category", params={
        "organization_id": 1,
        "category_id": 4,
    })
    assert response.status_code == status.HTTP_202_ACCEPTED
