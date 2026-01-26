from typing import Optional

from common.database import BaseEntity
from common.enum.tx_type import TxType
from sqlalchemy import String, Date, Enum, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

class Receipt(BaseEntity):
    __tablename__ = "receipt"

    paper_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_date: Mapped[date] = mapped_column(Date, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    tx_type: Mapped[TxType] = mapped_column(Enum(TxType, name="tx_type_enum"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), nullable=False)
    event_id: Mapped[Optional[int]] = mapped_column(ForeignKey("event.id", ondelete="SET NULL"), nullable=True)
    etc:Mapped[str] = mapped_column(String, nullable=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="receipts"
    )
    item: Mapped["Item"] = relationship(
        "Item",
        back_populates="receipts"
    )
    event: Mapped["Event"] = relationship(
        "Event",
        back_populates="receipts"
    )
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="receipts"
    )
    file: Mapped["FileInfo"] = relationship(
        "FileInfo",
        back_populates="receipt"
    )



