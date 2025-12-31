from fastapi.testclient import TestClient
from fastapi import status

from common.database import TxType
from common_test.security import login
from domain.ledger.category.category.dto import CreateCategoryDTO, DeleteCategoryParams
from domain.ledger.category.category.dto.edit_category_dto import EditCategoryDto
from domain.member.dto import LoginFormDTO

"""
성공 케이스
"""

def test_create_category(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/category", json=CreateCategoryDTO(
        category_name="Test",
        item_name=None,
        tx_type=TxType.INCOME,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

def test_create_category_and_item(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/category", json=CreateCategoryDTO(
        category_name="Test",
        item_name="Test Item",
        tx_type=TxType.INCOME,
        organization_id=1,
        year=2025
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

def test_delete_category_and_item(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/category", params={
        "organization_id": 1,
        "category_id": 3,
    })
    assert response.status_code == status.HTTP_202_ACCEPTED

"""
실패 케이스
"""

# not exist organization_id
def test_create_category_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/category", json=CreateCategoryDTO(
        category_name="Test",
        item_name=None,
        tx_type=TxType.INCOME,
        organization_id=100,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not own organization
def test_create_category_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.post("/ledger/category", json=CreateCategoryDTO(
        category_name="Test",
        item_name=None,
        tx_type=TxType.INCOME,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# not available year
def test_create_category_fail3(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/category", json=CreateCategoryDTO(
        category_name="Test",
        item_name=None,
        tx_type=TxType.INCOME,
        organization_id=1,
        year=2020
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# no data
def test_create_category_fail4(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/category")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# no data
def test_get_categories_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/ledger/category/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization id
def test_get_categories_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/ledger/category/",params={
        "organization_id": 100,
        "year": 2025,
        "tx_type": TxType.INCOME.value,
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not own organization
def test_get_categories_fail3(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.get("/ledger/category/",params={
        "organization_id": 1,
        "year": 2025,
        "tx_type": TxType.INCOME.value,
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

# not exist TX type
def test_get_categories_fail4(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/ledger/category/",params={
        "organization_id": 1,
        "year": 2025,
        "tx_type": "wrong",
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# no data
def test_update_category_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/category")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization_id
def test_update_category_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/category", json=EditCategoryDto(
        organization_id=100,
        category_id=1,
        category_name="test_category"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong organization id
def test_update_category_fail3(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.put("/ledger/category", json=EditCategoryDto(
        organization_id=1,
        category_id=1,
        category_name="test_category"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# not exist category id
def test_update_category_fail4(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/category", json=EditCategoryDto(
        organization_id=1,
        category_id=12,
        category_name="test_category"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong organization id
def test_update_category_fail5(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.put("/ledger/category", json=EditCategoryDto(
        organization_id=1,
        category_id=1,
        category_name="test_category"
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# can't delete category with receipts
def test_delete_category_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/category", params={
        "organization_id": 1,
        "category_id": 1,
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# no data
def test_delete_category_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/category")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not own category
def test_delete_category_fail3(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/category", params={
        "organization_id": 2,
        "category_id": 3,
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND