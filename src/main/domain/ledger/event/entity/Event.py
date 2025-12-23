from datetime import date

from sqlalchemy import String, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity

class Event(BaseEntity):
    __tablename__ = "event"

    name: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="events",
    )
    receipts: Mapped[list["Receipt"]] = relationship(
        "Receipt",
        back_populates="event",
    )