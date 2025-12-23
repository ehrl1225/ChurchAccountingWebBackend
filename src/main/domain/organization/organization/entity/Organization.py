from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity

class Organization(BaseEntity):
    __tablename__ = "organization"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    start_year: Mapped[int] = mapped_column(Integer, nullable=False)
    end_year: Mapped[int] = mapped_column(Integer, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)

    organization_invitations: Mapped[list["OrganizationInvitation"]] = relationship(
        "OrganizationInvitation",
        back_populates="organization",
    )
    joined_organization: Mapped[list["JoinedOrganization"]] = relationship(
        "JoinedOrganization",
        back_populates="organization",
    )
    categories: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="organization"
    )
    items: Mapped[list["Item"]] = relationship(
        "Item",
        back_populates="organization"
    )
    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="organization"
    )
    receipts: Mapped[list["Receipt"]] = relationship(
        "Receipt",
        back_populates="organization"
    )