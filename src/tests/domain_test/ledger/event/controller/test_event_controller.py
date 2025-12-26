from fastapi.testclient import TestClient
from fastapi import status
from datetime import timedelta

from pydantic.types import date

from common_test.security import login
from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.dto.edit_event_dto import EditEventDto
from domain.member.dto import LoginFormDTO


def test_create_event(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.post("/ledger/event", json=CreateEventDTO(
        organization_id=1,
        year=2025,
        name="test_event",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=1),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_201_CREATED

def test_get_events(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.get("/ledger/event", params={
        "organization_id": 1,
        "year": 2025,
    })
    assert response.status_code == status.HTTP_200_OK

def test_update_event(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.put("/ledger/event", json=EditEventDto(
        event_id=1,
        organization_id=1,
        event_name="test_event",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2),
        description="test_event",
    ).model_dump(mode="json"))
    assert response.status_code == status.HTTP_202_ACCEPTED

def test_delete_event(client: TestClient):
    login(client, LoginFormDTO(email="test_user0@user.com", password="password"))
    response = client.delete("/ledger/event",params={
        "organization_id": 1,
        "event_id": 1
    })
    assert response.status_code == status.HTTP_200_OK