from httpx import AsyncClient
from fastapi import status
from datetime import timedelta

from pydantic.types import date
import pytest

from common_test.security import login
from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.dto.edit_event_dto import EditEventDto
from domain.member.dto import LoginFormDTO

"""
성공 케이스
"""
@pytest.mark.anyio
async def test_create_event(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/event/", json=CreateEventDTO(
        organization_id=1,
        year=2025,
        name="test_event",
        start_date=date(year=2025, month=1, day=1),
        end_date=date(year=2025, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.anyio
async def test_get_events(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/event/", params={
        "organization_id": 1,
        "year": 2025,
    })
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_update_event(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/event/", json=EditEventDto(
        event_id=1,
        organization_id=1,
        event_name="test_event",
        start_date=date(year=2025, month=1, day=1),
        end_date=date(year=2025, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_202_ACCEPTED

@pytest.mark.anyio
async def test_delete_event(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/event/",params={
        "organization_id": 1,
        "event_id": 1
    })
    assert response.status_code == status.HTTP_200_OK

"""
실패 케이스
"""

# no data
@pytest.mark.anyio
async def test_create_event_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/event/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization id
@pytest.mark.anyio
async def test_create_event_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/event/", json=CreateEventDTO(
        organization_id=100,
        year=2025,
        name="test_event",
        start_date=date(year=2025, month=1, day=1),
        end_date=date(year=2025, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not available year
@pytest.mark.anyio
async def test_create_event_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/event/", json=CreateEventDTO(
        organization_id=1,
        year=2020,
        name="test_event",
        start_date=date(year=2020, month=1, day=1),
        end_date=date(year=2020, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not authorized user
@pytest.mark.anyio
async def test_create_event_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.post("/ledger/event/", json=CreateEventDTO(
        organization_id=1,
        year=2025,
        name="test_event",
        start_date=date(year=2025, month=1, day=1),
        end_date=date(year=2025, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# year and start date not match
@pytest.mark.anyio
async def test_create_event_fail5(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/event/", json=CreateEventDTO(
        organization_id=1,
        year=2025,
        name="test_event",
        start_date=date(year=2021, month=1, day=1),
        end_date=date(year=2025, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# year and end date not match
@pytest.mark.anyio
async def test_create_event_fail6(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/event/", json=CreateEventDTO(
        organization_id=1,
        year=2025,
        name="test_event",
        start_date=date(year=2025, month=1, day=1),
        end_date=date(year=2030, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# end date before start date
@pytest.mark.anyio
async def test_create_event_fail7(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.post("/ledger/event/", json=CreateEventDTO(
        organization_id=1,
        year=2025,
        name="test_event",
        start_date=date(year=2025, month=1, day=2),
        end_date=date(year=2025, month=1, day=1),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not exist organization
@pytest.mark.anyio
async def test_get_events_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/event/", params={
        "organization_id": 100,
        "year": 2025,
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not available year
@pytest.mark.anyio
async def test_get_events_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.get("/ledger/event/", params={
        "organization_id": 1,
        "year": 2020,
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not authorized user
@pytest.mark.anyio
async def test_get_events_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.get("/ledger/event/", params={
        "organization_id": 1,
        "year": 2025,
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

# no data
@pytest.mark.anyio
async def test_get_events_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.get("/ledger/event/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization
@pytest.mark.anyio
async def test_update_event_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/event/", json=EditEventDto(
        event_id=1,
        organization_id=100,
        event_name="test_event",
        start_date=date(year=2025, month=1, day=1),
        end_date=date(year=2025, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist event
@pytest.mark.anyio
async def test_update_event_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/event/", json=EditEventDto(
        event_id=100,
        organization_id=1,
        event_name="test_event",
        start_date=date(year=2025, month=1, day=1),
        end_date=date(year=2025, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not available start date year
@pytest.mark.anyio
async def test_update_event_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/event/", json=EditEventDto(
        event_id=1,
        organization_id=1,
        event_name="test_event",
        start_date=date(year=2024, month=1, day=1),
        end_date=date(year=2025, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# not available end date year
@pytest.mark.anyio
async def test_update_event_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/event/", json=EditEventDto(
        event_id=1,
        organization_id=1,
        event_name="test_event",
        start_date=date(year=2025, month=1, day=1),
        end_date=date(year=2026, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# no data
@pytest.mark.anyio
async def test_update_event_fail5(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/event/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not authorized user
@pytest.mark.anyio
async def test_update_event_fail6(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user4@user.com", password="password"))
    response = await client.put("/ledger/event/", json=EditEventDto(
        event_id=1,
        organization_id=1,
        event_name="test_event",
        start_date=date(year=2025, month=1, day=1),
        end_date=date(year=2026, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_403_FORBIDDEN

# wrong event id
@pytest.mark.anyio
async def test_update_event_fail7(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.put("/ledger/event/", json=EditEventDto(
        event_id=3,
        organization_id=1,
        event_name="test_event",
        start_date=date(year=2025, month=1, day=1),
        end_date=date(year=2026, month=1, day=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# no data
@pytest.mark.anyio
async def test_delete_event_fail1(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/event/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# not exist organization
@pytest.mark.anyio
async def test_delete_event_fail2(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/event/",params={
        "organization_id": 100,
        "event_id": 1
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

# not exist event
@pytest.mark.anyio
async def test_delete_event_fail3(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/event/",params={
        "organization_id": 1,
        "event_id": 100
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_delete_event_fail4(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/event/",params={
        "organization_id": 3,
        "event_id": 1
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_delete_event_fail5(client: AsyncClient):
    await login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = await client.delete("/ledger/event/", params={
        "organization_id": 1,
        "event_id": 4
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND