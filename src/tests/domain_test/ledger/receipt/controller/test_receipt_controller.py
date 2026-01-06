from httpx import AsyncClient
from fastapi import status
from datetime import date
import pytest

from common.database import TxType
from common_test.security import login
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.dto.request.edit_receipt_dto import EditReceiptDto
from domain.member.dto import LoginFormDTO

@pytest.mark.anyio
async def test_create_receipt(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/", json=CreateReceiptDto(
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

@pytest.mark.anyio
async def test_get_all_receipts(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/receipt/all", params={
        "organization_id": 1,
        "year": 2025
    })
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_update_receipt(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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

@pytest.mark.anyio
async def test_delete_receipt(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/receipt/", params={
        "organization_id": 1,
        "receipt_id": 1,
    })
    assert response.status_code == status.HTTP_200_OK

# not exist organization
@pytest.mark.anyio
async def test_create_receipt_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/", json=CreateReceiptDto(
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
@pytest.mark.anyio
async def test_create_receipt_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/", json=CreateReceiptDto(
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
@pytest.mark.anyio
async def test_create_receipt_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/", json=CreateReceiptDto(
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
@pytest.mark.anyio
async def test_create_receipt_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/", json=CreateReceiptDto(
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
@pytest.mark.anyio
async def test_create_receipt_fail5(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/", json=CreateReceiptDto(
        receipt_image_url=None,
        paper_date=date(year=2025, month=1, day=1),
        actual_date=None,
        name="receipt",
        tx_type=TxType.OUTCOME,
        amount=-100,
        category_id=1,
        item_id=1,
        event_id=1,
        etc=None,
        organization_id=1,
        year=2025
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# wrong year
@pytest.mark.anyio
async def test_create_receipt_fail6(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/", json=CreateReceiptDto(
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
@pytest.mark.anyio
async def test_create_receipt_fail7(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/", json=CreateReceiptDto(
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
@pytest.mark.anyio
async def test_create_receipt_fail8(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/", json=CreateReceiptDto(
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
@pytest.mark.anyio
async def test_create_receipt_fail9(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# item not belong to category
@pytest.mark.anyio
async def test_create_receipt_fail10(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/receipt/", json=CreateReceiptDto(
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
@pytest.mark.anyio
async def test_get_all_receipts_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.get("/ledger/receipt/all", params={
        "organization_id": 1,
        "year": 2025
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

# wrong year
@pytest.mark.anyio
async def test_get_all_receipts_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/receipt/all", params={
        "organization_id": 1,
        "year": 2020
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not exist organization
@pytest.mark.anyio
async def test_get_all_receipts_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/receipt/all", params={
        "organization_id": 100,
        "year": 2025
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# no data
@pytest.mark.anyio
async def test_get_all_receipts_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/receipt/all")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization
@pytest.mark.anyio
async def test_update_receipt_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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
@pytest.mark.anyio
async def test_update_receipt_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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
@pytest.mark.anyio
async def test_update_receipt_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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
@pytest.mark.anyio
async def test_update_receipt_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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
@pytest.mark.anyio
async def test_update_receipt_fail5(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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
@pytest.mark.anyio
async def test_update_receipt_fail6(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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
@pytest.mark.anyio
async def test_update_receipt_fail7(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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
@pytest.mark.anyio
async def test_update_receipt_fail8(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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
@pytest.mark.anyio
async def test_update_receipt_fail9(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not authorized user
@pytest.mark.anyio
async def test_update_receipt_fail10(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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

@pytest.mark.anyio
async def test_update_receipt_fail11(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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

@pytest.mark.anyio
async def test_update_receipt_fail12(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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

@pytest.mark.anyio
async def test_update_receipt_fail13(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/receipt/", json=EditReceiptDto(
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
@pytest.mark.anyio
async def test_delete_receipt_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/receipt/", params={
        "organization_id": 100,
        "receipt_id": 1,
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist receipt
@pytest.mark.anyio
async def test_delete_receipt_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/receipt/", params={
        "organization_id": 1,
        "receipt_id": 100,
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not authorized user
@pytest.mark.anyio
async def test_delete_receipt_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.delete("/ledger/receipt/", params={
        "organization_id": 1,
        "receipt_id": 1,
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

# no data
@pytest.mark.anyio
async def test_delete_receipt_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/receipt/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# wrong receipt
@pytest.mark.anyio
async def test_delete_receipt_fail5(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/receipt/", params={
        "organization_id": 2,
        "receipt_id": 1,
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
