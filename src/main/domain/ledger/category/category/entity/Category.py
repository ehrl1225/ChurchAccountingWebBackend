from sqlalchemy import String, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from common.database import BaseEntity
from common.enum.tx_type import TxType

class Category(BaseEntity):
    __tablename__ = "category"
    name: Mapped[str] = mapped_column(String, nullable=False)
    tx_type: Mapped[TxType] = mapped_column(Enum(TxType, name="tx_type_enum"), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    items: Mapped[list["Item"]] = relationship(
        "Item",
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    receipts: Mapped[list["Receipt"]] = relationship(
        "Receipt",
        back_populates="category",
    )
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="categories",
    )
