import docx
from docx.document import Document
from docx.styles.style import BaseStyle, ParagraphStyle
from docx.types import annotations
from docx.styles.styles import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.table import _Cell, Table
from datetime import datetime
import calendar
from .word_util import *

from sqlalchemy.ext.asyncio import AsyncSession

from common.database import TxType
from domain.file.word.dto.create_settlement_dto import CreateSettlementDto
from domain.ledger.receipt.dto import SummaryType, ReceiptSummaryParams
from domain.ledger.receipt.service import ReceiptService


class WordService:

    def __init__(self, receipt_service: ReceiptService):
        self.receipt_service = receipt_service

    async def create_month_document(self,db:AsyncSession, create_settlement:CreateSettlementDto):
        doc:Document = docx.Document()

        style_1 = setFont(doc, "style_1", "맑은 고딕", 15, True)
        style_2 = setFont(doc, "style_2", "맑은 고딕", 10, False)
        style_3 = setFont(doc, "style_3", "맑은 고딕", 13, True)
        style_4 = setFont(doc, "style_4", "맑은 고딕", 30, False)
        style_5 = setFont(doc, "style_5", "맑은 고딕", 15, False)

        single = {"val":"single"}
        single_bold = {"val": "single", "sz": 10}
        double = {"val": "double"}
        cell_color = "#E5E5E5"
        last_cell_color = "#BFBFBF"

        year = create_settlement.year
        month = create_settlement.month_number
        first_day, last_day = calendar.monthrange(year, month)
        organization_name = create_settlement.organization_name

        data = await self.receipt_service.get_summary_receipt(db, receipt_summary_params=ReceiptSummaryParams(
            summary_type=create_settlement.summary_type,
            month_number=create_settlement.month_number,
            organization_id=create_settlement.organization_id,
            year=create_settlement.year,
            event_id=create_settlement.event_id,
        ))
        income_categories = []
        outcome_categories = []
        income_items_count = 0
        outcome_items_count = 0
        total_row_count = income_items_count + outcome_items_count + 6
        income_total = data.total_income
        outcome_total = data.total_outcome
        balance = data.balance

        for category in data.categories:
            if category.tx_type == TxType.INCOME:
                income_categories.append(category.name)
                income_items_count += len(category.items)
            else:
                outcome_categories.append(category.name)
                outcome_items_count += len(category.items)

        table = doc.add_table(rows=total_row_count, cols=6)
        first_line_items = ["구 분", "항 목", "내 용", "금 액", "비 고"]
        mergeCell(table.cell(0, 3), table.cell(0, 4))
        for col in [i for i in range(6) if i != 4]:
            cell = table.cell(0, col)
            if col == 0:
                setCellBorder(cell, start=single_bold)
            elif col == 5:
                setCellBorder(cell, start=single, end=single_bold)
            else:
                setCellBorder(cell, start=single)
            setCellBorder(cell, top=single_bold, bottom=double)
            setCellColor(cell, cell_color)
            if col < 4:
                setCellText(cell, first_line_items[col], style_3, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_VERTICAL.CENTER)
            else:
                setCellText(cell, first_line_items[4], style_3, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_VERTICAL.CENTER)


        # 작성 시작

        p1 = doc.add_paragraph(f'{year}년도 {organization_name} {month}월 결산안', style=style_1)
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p2 = doc.add_paragraph(f"({year}.{month}.{first_day} ~ {year}.{month}.{last_day})", style=style_2)
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p3 = doc.add_paragraph("[단위 : 원]", style=style_2)
        p3.alignment = WD_ALIGN_PARAGRAPH.RIGHT



        doc.save("test.docx")

if __name__ == '__main__':
    import asyncio
    service = WordService()
    asyncio.run(
    service.create_month_document(create_settlement=CreateSettlementDto(
        summary_type=SummaryType.MONTH,
        month_number=1,
        organization_id=1,
        event_id=None,
        year=2026,
        organization_name="빛울림 청년부"
    )))