from fastapi.testclient import TestClient
from fastapi import status
from datetime import date

from common.database import TxType
from common_test.security import login
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.dto.edit_receipt_dto import EditReceiptDto
from domain.member.dto import LoginFormDTO


def test_create_receipt(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        name="receipt",
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        event_id=None,
        etc=None,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

def test_get_all_receipts(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/ledger/receipt/all", params={
        "organization_id": 1,
        "year": 2025
    })
    assert response.status_code == status.HTTP_200_OK

def test_update_receipt(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_200_OK

def test_delete_receipt(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/receipt", params={
        "organization_id": 1,
        "receipt_id": 1,
    })
    assert response.status_code == status.HTTP_200_OK

# not exist organization
def test_create_receipt_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        name="receipt",
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        event_id=None,
        etc=None,
        organization_id=100,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist category
def test_create_receipt_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        name="receipt",
        tx_type=TxType.INCOME,
        amount=100,
        category_id=100,
        item_id=1,
        event_id=None,
        etc=None,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist item
def test_create_receipt_fail3(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        name="receipt",
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=100,
        event_id=None,
        etc=None,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong amount for income
def test_create_receipt_fail4(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        name="receipt",
        tx_type=TxType.INCOME,
        amount=-100,
        category_id=1,
        item_id=1,
        event_id=1,
        etc=None,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# wrong amount outcome
def test_create_receipt_fail5(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        name="receipt",
        tx_type=TxType.OUTCOME,
        amount=100,
        category_id=1,
        item_id=1,
        event_id=1,
        etc=None,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# wrong year
def test_create_receipt_fail6(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        name="receipt",
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        event_id=None,
        etc=None,
        organization_id=1,
        year=2020
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# wrong paper date year
def test_create_receipt_fail7(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2023, month=1, day=1),
        actual_date=None,
        name="receipt",
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        event_id=None,
        etc=None,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# wrong actual date year
def test_create_receipt_fail8(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=date(year=2026, month=1, day=1),
        name="receipt",
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        event_id=None,
        etc=None,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# no data
def test_create_receipt_fail9(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# item not belong to category
def test_create_receipt_fail10(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/receipt", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        name="receipt",
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=4,
        event_id=None,
        etc=None,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not authorized user
def test_get_all_receipts_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.get("/ledger/receipt/all", params={
        "organization_id": 1,
        "year": 2025
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

# wrong year
def test_get_all_receipts_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/ledger/receipt/all", params={
        "organization_id": 1,
        "year": 2020
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not exist organization
def test_get_all_receipts_fail3(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/ledger/receipt/all", params={
        "organization_id": 100,
        "year": 2025
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# no data
def test_get_all_receipts_fail4(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/ledger/receipt/all")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization
def test_update_receipt_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=100,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist category
def test_update_receipt_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=100,
        category_id=100,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist item
def test_update_receipt_fail3(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=100,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist receipt
def test_update_receipt_fail4(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=100,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# wrong paper date year
def test_update_receipt_fail5(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2024, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# wrong actual date year
def test_update_receipt_fail6(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=date(year=2026, month=1, day=1),
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# wrong income amount
def test_update_receipt_fail7(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=-100,
        category_id=1,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# wrong outcome amount
def test_update_receipt_fail8(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.OUTCOME,
        amount=100,
        category_id=1,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# no data
def test_update_receipt_fail9(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not authorized user
def test_update_receipt_fail10(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_update_receipt_fail11(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=2,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_receipt_fail12(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=1,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=4,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_receipt_fail13(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/receipt", json=EditReceiptDto(
        organization_id=1,
        receipt_id=2,
        name="receipt",
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        tx_type=TxType.INCOME,
        amount=100,
        category_id=1,
        item_id=1,
        etc=None,
        event_id=None,
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not exist organization
def test_delete_receipt_fail1(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/receipt", params={
        "organization_id": 100,
        "receipt_id": 1,
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist receipt
def test_delete_receipt_fail2(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/receipt", params={
        "organization_id": 1,
        "receipt_id": 100,
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not authorized user
def test_delete_receipt_fail3(client: TestClient):
    login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = client.delete("/ledger/receipt", params={
        "organization_id": 1,
        "receipt_id": 1,
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

# no data
def test_delete_receipt_fail4(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/receipt")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# wrong receipt
def test_delete_receipt_fail5(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/receipt", params={
        "organization_id": 2,
        "receipt_id": 1,
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
