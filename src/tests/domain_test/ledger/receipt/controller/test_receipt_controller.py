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
        paper_date=date.today(),
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
        paper_date=date.today(),
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