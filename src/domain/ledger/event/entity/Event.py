from datetime import date

from sqlalchemy import String, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity

class Event(BaseEntity):
    __tablename__ = "event"

    name: Mapped[str] = mapped_column(String)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    description: Mapped[str] = mapped_column(String)
    ledger_organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    ledger_organization: Mapped["LedgerOrganization"] = relationship(
        "LedgerOrganization",
        back_populates="items",
    )