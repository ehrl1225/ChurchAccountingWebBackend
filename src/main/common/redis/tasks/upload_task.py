import json
from typing import Optional

import numpy as np
import pandas as pd
import io
import httpx

import asyncio
from datetime import date
from common.env import settings
from common.database import SessionLocal, TxType
from common.redis import get_redis
from common.redis.redis_client import RedisClient
from domain.file.file.controller import FileType
from domain.file.file.service import LocalStorageService, S3StorageService

from domain.ledger.category.category.dto.request import CategoryCheck
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.category.entity import Category
from domain.ledger.category.item.dto import ItemCheck
from domain.ledger.category.item.entity import Item
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.event.entity import Event
from domain.ledger.event.repository import EventRepository
from domain.ledger.receipt.entity import Receipt
from domain.ledger.receipt.repository import ReceiptRepository
from domain.file.file.service import StorageService
from domain.organization.organization.entity import Organization
from domain.organization.organization_invitation.entity import OrganizationInvitation
from domain.organization.joined_organization.entity import JoinedOrganization
from domain.member.entity import Member



async def async_process_excel(file_name: str, organization_id: int, year: int):
    await RedisClient.init()
    category_repository = CategoryRepository()
    item_repository = ItemRepository()
    event_repository = EventRepository()
    receipt_repository = ReceiptRepository()
    storage_service:Optional[StorageService] = None
    redis= await get_redis()
    match settings.PROFILE:
        case "prod":
            storage_service = S3StorageService()
        case _:
            storage_service = LocalStorageService()
    file_key = f"{FileType.EXCEL.value}/{organization_id}/{year}/{file_name}"
    print("Processing excel receipt upload")
    result_payload = {}
    async with SessionLocal() as db:
        try:
            excel_data = None
            async with httpx.AsyncClient() as client:
                file_get_url = await storage_service.create_presigned_get_url(file_key)
                response = await client.get(file_get_url)
                response.raise_for_status()
                excel_data = io.BytesIO(response.content)
            if excel_data is None:
                return
            df = pd.read_excel(excel_data)
            receipts_to_create:list[Receipt] = []
            categories_to_check:list[CategoryCheck] = []
            items_data_to_check:list[ItemCheck] = []
            event_data_to_check:list[str] = []
            for index, row in df.iterrows():
                amount = row["amount"]
                tx_type = TxType.INCOME if amount > 0 else TxType.OUTCOME
                category_name = row["category_name"]
                item_name = row["item_name"]
                event_name = row.get("event_name" , None)

                category_check = CategoryCheck(
                    tx_type=tx_type,
                    name=category_name,
                )
                categories_to_check.append(category_check)
                item_check = ItemCheck(
                    tx_type=tx_type,
                    category_name=category_name,
                    item_name=item_name,
                )
                items_data_to_check.append(item_check)
                if not pd.isna(event_name):
                    event_data_to_check.append(event_name)
            existing_categories = await category_repository.find_all_by_names(db, categories_to_check, organization_id, year)
            category_map:dict[tuple[str, TxType], Category] = { (c.name, c.tx_type):c for c in existing_categories }
            new_categories = []
            new_categories_set = set()
            for category in categories_to_check:
                if (category.name, category.tx_type) in new_categories_set:
                    continue
                if (category.name, category.tx_type) not in category_map:
                    c = Category(
                        name=category.name,
                        tx_type=category.tx_type,
                        organization_id=organization_id,
                        year=year,
                    )
                    new_categories.append(c)
                    new_categories_set.add((category.name, category.tx_type))
            for category in await category_repository.bulk_create(db, new_categories):
                category_map[(category.name, category.tx_type)] = category


            existing_items = await item_repository.find_all_by_names(db, items_data_to_check, organization_id, year)
            item_map:dict[tuple[str, TxType, str], Item] = { (i.category.name, i.category.tx_type, i.name):i for i in existing_items }
            new_items = []
            new_items_set = set()
            for item in items_data_to_check:
                if (item.category_name, item.tx_type, item.item_name) in new_items_set:
                    continue
                if (item.category_name, item.tx_type, item.item_name) not in item_map:
                    i = Item(
                        name=item.item_name,
                        category_id=category_map[(item.category_name, item.tx_type)].id,
                        organization_id=organization_id,
                        year=year,
                    )
                    new_items.append(i)
                    new_items_set.add((item.category_name, item.tx_type, item.item_name))
            for item in await item_repository.bulk_create(db, new_items):
                item_map[(item.category.name, item.category.tx_type, item.name)] = item

            existing_events = await event_repository.find_all_by_names(db, event_data_to_check, organization_id, year)
            event_map = { e.name: e for e in existing_events }
            new_events = []
            new_events_set = set()
            for event in event_data_to_check:
                if event in new_events_set:
                    continue
                if event.name not in event_map:
                    e = Event(
                        name=event,
                        start_date=date(year=year, month=1, day=1),
                        end_date=date(year=year, month=1, day=1),
                        organization_id=organization_id,
                        year=year,
                    )
                    new_events.append(e)
                    new_categories_set.add(event)
            for event in await event_repository.bulk_create(db, new_events):
                event_map[event.name] = event

            for index, row in df.iterrows():
                paper_date = row["paper_date"]
                actual_date = row["actual_date"]
                name = row["name"]
                amount = row["amount"]
                tx_type = TxType.INCOME if amount > 0 else TxType.OUTCOME
                category_name = row["category_name"]
                item_name = row["item_name"]
                event_name = row["event_name"]
                etc = row["etc"]
                actual_date = actual_date if not pd.isna(actual_date) else None
                category_id = category_map[(category_name, tx_type)].id
                item_id = item_map[(category_name, tx_type, item_name)].id
                event_id = event_map.get(event_name, None) if not pd.isna(event_name) != np.nan else None
                etc = etc if not pd.isna(etc) else None
                receipt = Receipt(
                    paper_date=paper_date,
                    actual_date=actual_date,
                    name=name,
                    tx_type=tx_type,
                    amount=amount,
                    category_id=category_id,
                    item_id=item_id,
                    event_id=event_id,
                    etc=etc,
                    organization_id=organization_id,
                    year=year,
                )
                receipts_to_create.append(receipt)
            await receipt_repository.bulk_create(db, receipts_to_create)
            await db.commit()
            print("success")
            result_payload = {"status":"completed", "file_url":"no url"}
        except Exception as e:
            print(e)
            await db.rollback()
            result_payload = {"status":"failed", "file_url":"no url"}
        finally:
            if result_payload:
                await redis.set(f"file_name:{file_name}", json.dumps(result_payload), ex=600)
            channel_name = f"excel_upload:{file_name}"
            await redis.publish(channel_name, "completed")
            await RedisClient.close()
            await storage_service.delete_file(file_key)

def process_excel_receipt_upload(file_path: str, organization_id: int, year: int):
    asyncio.run(async_process_excel(file_path, organization_id, year))
