import json
import uuid
from typing import Optional
from fastapi import HTTPException, status, UploadFile
from redis.asyncio import Redis
from rq import Queue
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import TxType
from common.database.file_type import FileType
from domain.file.file.dto.file_info_response_dto import FileInfoResponseDto
from domain.file.file.entity import FileInfo
from domain.file.file.repository import FileRepository
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.event.repository import EventRepository
from domain.ledger.receipt.dto import CreateReceiptDto, SummaryType
from domain.ledger.receipt.dto.request.delete_receipt_params import DeleteReceiptParams
from domain.ledger.receipt.dto.request.edit_receipt_dto import EditReceiptDto
from domain.ledger.receipt.dto.request.upload_receipt_dto import UploadReceiptDto
from domain.ledger.receipt.dto.response import SummaryData, ReceiptResponseDto
from domain.ledger.receipt.dto.request.search_receipt_params import SearchAllReceiptParams
from domain.ledger.receipt.dto.request.receipt_summary_params import ReceiptSummaryParams
from domain.ledger.receipt.dto.response.receipt_summary_category_dto import ReceiptSummaryCategoryDto
from domain.ledger.receipt.dto.response.receipt_summary_dto import ReceiptSummaryDto
from domain.ledger.receipt.dto.response.receipt_summary_item_dto import ReceiptSummaryItemDto
from domain.ledger.receipt.repository import ReceiptRepository
from domain.ledger.receipt.entity import Receipt
from domain.member.repository import MemberRepository
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization.repository import OrganizationRepository


class ReceiptService:

    def __init__(
            self,
            receipt_repository: ReceiptRepository,
            category_repository: CategoryRepository,
            item_repository: ItemRepository,
            event_repository: EventRepository,
            organization_repository: OrganizationRepository,
            member_repository: MemberRepository,
            joined_organization_repository: JoinedOrganizationRepository,
            file_repository: FileRepository,
            redis_client: Redis,
            redis_queue:Queue,
    ):
        self.receipt_repository = receipt_repository
        self.category_repository = category_repository
        self.item_repository = item_repository
        self.event_repository = event_repository
        self.organization_repository = organization_repository
        self.member_repository = member_repository
        self.joined_organization_repository = joined_organization_repository
        self.file_repository = file_repository
        self.redis_client = redis_client
        self.redis_queue = redis_queue

    async def create_receipt(self, db: AsyncSession, create_receipt_dto:CreateReceiptDto) -> ReceiptResponseDto:
        # verify
        if create_receipt_dto.amount < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="amount must be greater than 0")
        if create_receipt_dto.tx_type == TxType.OUTCOME:
            create_receipt_dto.amount = -create_receipt_dto.amount
        organization = await self.organization_repository.find_by_id(db, create_receipt_dto.organization_id)
        if organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        if not organization.start_year <= create_receipt_dto.year <= organization.end_year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization start year must be in range")
        category = await self.category_repository.find_by_id(db, create_receipt_dto.category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        if category.organization_id != organization.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category is not belong to organization")
        if category.year != create_receipt_dto.year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="wrong year")
        if category.year != create_receipt_dto.paper_date.year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="wrong year")
        if create_receipt_dto.actual_date is not None and category.year != create_receipt_dto.actual_date.year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="wrong year")

        item = await self.item_repository.find_by_id(db, create_receipt_dto.item_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        if item.organization_id != organization.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item is not belong to organization")
        if item.category_id != category.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="item is not belong to category")
        event = None
        if create_receipt_dto.event_id is not None:
            event = await self.event_repository.find_by_id(db, create_receipt_dto.event_id)
            if event is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        # work
        receipt = await self.receipt_repository.create_receipt(
            db,
            create_receipt_dto
        )
        file_info = None
        if create_receipt_dto.receipt_image_id is not None:
            file_info = await self.file_repository.find_by_id(db, create_receipt_dto.receipt_image_id)
            if file_info is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
            await self.file_repository.update_file_info(db, file_info, receipt.id)
        receipt_dto = ReceiptResponseDto.model_validate(receipt)
        receipt_dto.category_name = category.name
        receipt_dto.item_name = item.name
        receipt_dto.amount = abs(receipt.amount)
        if event is not None:
            receipt_dto.event_name = event.name
        if file_info is not None:
            receipt_dto.receipt_image_id = file_info.id
            receipt_dto.receipt_image_file_name = file_info.file_name
        return receipt_dto

    async def upload_excel(
            self,
            upload_receipt_dto: UploadReceiptDto
    ):

        self.redis_queue.enqueue(
            "common.redis.redis_tasks.process_excel_receipt_upload",
            upload_receipt_dto.excel_file_name,
            upload_receipt_dto.organization_id,
            upload_receipt_dto.year,
        )

    async def download_excel(self, organization_id: int, year: int):
        file_name = f"{uuid.uuid4().hex}.xlsx"
        initial_state = {"status":"pending"}
        await self.redis_client.set(f"file_name:{file_name}", json.dumps(initial_state), ex=600)
        self.redis_queue.enqueue(
            "common.redis.redis_tasks.process_excel_receipt_download",
            file_name,
            organization_id,
            year
        )
        return FileInfoResponseDto(
            id=0,
            file_name=file_name,
            url="",
            fields={}
        )


    async def get_all_receipts(self, db: AsyncSession, search_receipt_params:SearchAllReceiptParams):
        # verify
        organization = await self.organization_repository.find_by_id(db, search_receipt_params.organization_id)
        if organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        if not organization.start_year <= search_receipt_params.year <= organization.end_year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization start year must be in range")

        # work
        receipts:list[Receipt] = await self.receipt_repository.find_all(
            db=db,
            organization_id=search_receipt_params.organization_id,
            year=search_receipt_params.year,)
        receipt_dtos = []
        for receipt in receipts:
            receipt_dto = ReceiptResponseDto.model_validate(receipt)
            receipt_dto.category_name = receipt.category.name
            receipt_dto.item_name = receipt.item.name
            receipt_dto.amount = abs(receipt.amount)
            file:Optional[FileInfo] = receipt.file
            if file is not None:
                receipt_dto.receipt_image_id = file.id
                receipt_dto.receipt_image_file_name = file.file_name

            if receipt_dto.event_id is not None:
                receipt_dto.event_name = receipt.event.name
            receipt_dtos.append(receipt_dto)
        return receipt_dtos

    async def get_summary_receipt(self, db: AsyncSession, receipt_summary_params:ReceiptSummaryParams):
        data: list[SummaryData] = []
        event_name = None
        total_income = 0
        total_outcome = 0
        match receipt_summary_params.summary_type:
            case SummaryType.MONTH:
                if receipt_summary_params.month_number is not None:
                    data.extend(await self.receipt_repository.find_amount_by_month(
                        db,
                        receipt_summary_params.organization_id,
                        receipt_summary_params.year,
                        receipt_summary_params.month_number
                    ))
                else:
                    data.extend(await self.receipt_repository.find_all_amount(
                        db,
                        receipt_summary_params.organization_id,
                        receipt_summary_params.year
                    ))
            case SummaryType.EVENT:
                if receipt_summary_params.event_id is not None:
                    data.extend(await self.receipt_repository.find_by_event(
                        db,
                        receipt_summary_params.organization_id,
                        receipt_summary_params.year,
                        receipt_summary_params.event_id
                    ))
                else:
                    data.extend(await self.receipt_repository.find_all_by_event(
                        db,
                        receipt_summary_params.organization_id,
                        receipt_summary_params.year
                    ))
            case _:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="wrong summary_type")
        receipt_category_dtos:list[ReceiptSummaryCategoryDto] = []
        receipt_category_dict:dict[int, ReceiptSummaryCategoryDto] = {}
        if len(data) > 0:
            for d in data:
                item = ReceiptSummaryItemDto(
                    item_id=d.item.id,
                    item_name=d.item.name,
                    amount=abs(d.total_amount)
                )
                match d.category.tx_type:
                    case TxType.INCOME:
                        total_income += d.total_amount
                    case TxType.OUTCOME:
                        total_outcome += d.total_amount
                    case _:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="wrong tx_type")
                if d.category.id not in receipt_category_dict:
                    category_dto = ReceiptSummaryCategoryDto(
                        category_id=d.category.id,
                        category_name=d.category.name,
                        amount=abs(d.total_amount),
                        items=[item],
                        tx_type = d.category.tx_type
                    )
                    receipt_category_dict[d.category.id] = category_dto
                    receipt_category_dtos.append(category_dto)
                else:
                    receipt_category_dict[d.category.id].items.append(item)
        if receipt_summary_params.event_id is not None:
            event = await self.event_repository.find_by_id(db, receipt_summary_params.event_id)
            if event is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
            event_name = event.name
        balance = total_income + total_outcome
        return ReceiptSummaryDto(
            summary_type=receipt_summary_params.summary_type,
            month_number=receipt_summary_params.month_number,
            event_id=receipt_summary_params.event_id,
            event_name=event_name,
            total_income=total_income,
            total_outcome=abs(total_outcome),
            balance=balance,
            categories=receipt_category_dtos
        )

    async def update(self, db: AsyncSession, edit_receipt_dto: EditReceiptDto) -> ReceiptResponseDto:
        # verify
        organization = await self.organization_repository.find_by_id(db, edit_receipt_dto.organization_id)
        if organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        category = await self.category_repository.find_by_id(db, edit_receipt_dto.category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        if category.organization_id != edit_receipt_dto.organization_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="category is not belong to organization")
        item = await self.item_repository.find_by_id(db, edit_receipt_dto.item_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        if item.organization_id != edit_receipt_dto.organization_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="item is not belong to organization")
        if item.category_id != category.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="item is not belong to category")
        receipt = await self.receipt_repository.find_by_id(db, edit_receipt_dto.receipt_id)
        if receipt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
        if receipt.organization_id != edit_receipt_dto.organization_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="receipt is not belong to organization")
        if edit_receipt_dto.paper_date.year != category.year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="year must follow category year")
        if edit_receipt_dto.actual_date is not None and edit_receipt_dto.actual_date.year != receipt.year:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="year must be in range")
        if  edit_receipt_dto.amount <0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="amount cannot be negative")
        if edit_receipt_dto.tx_type == TxType.OUTCOME:
            edit_receipt_dto.amount = -edit_receipt_dto.amount
        event = None
        if edit_receipt_dto.event_id is not None:
            event = await self.event_repository.find_by_id(db, edit_receipt_dto.event_id)
            if event is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        # work
        receipt = await self.receipt_repository.find_by_id_with_file(db, edit_receipt_dto.receipt_id)
        receipt = await self.receipt_repository.update(db, receipt, edit_receipt_dto)
        file_info = None
        if edit_receipt_dto.receipt_image_id is not None:
            file_info = await self.file_repository.find_by_id(db, edit_receipt_dto.receipt_image_id)
            if file_info is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
            if receipt.file is not None:
                old_file_info = receipt.file
                await self.file_repository.update_file_info(db, old_file_info, None)
            await self.file_repository.update_file_info(db, file_info, receipt.id)
        receipt_dto = ReceiptResponseDto.model_validate(receipt)
        receipt_dto.category_name = category.name
        receipt_dto.item_name = item.name
        if event is not None:
            receipt_dto.event_name = event.name
        receipt_dto.amount = abs(receipt.amount)
        if file_info is not None:
            receipt_dto.receipt_image_id = file_info.id
            receipt_dto.receipt_image_file_name = file_info.file_name
        return receipt_dto

    async def delete(self, db: AsyncSession, delete_receipt_dto:DeleteReceiptParams):
        organization = await self.organization_repository.find_by_id(db, delete_receipt_dto.organization_id)
        if organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        receipt = await self.receipt_repository.find_by_id(db, delete_receipt_dto.receipt_id)
        if receipt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
        if receipt.organization_id != delete_receipt_dto.organization_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="organization not found")

        await self.receipt_repository.delete(db, receipt)