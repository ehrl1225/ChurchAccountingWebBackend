from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity

class Item(BaseEntity):
    __tablename__ = "item"
    name: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="items",
    )
    receipts: Mapped[list["Receipt"]] = relationship(
        "Receipt",
        back_populates="item"
    )
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="items",
    )
