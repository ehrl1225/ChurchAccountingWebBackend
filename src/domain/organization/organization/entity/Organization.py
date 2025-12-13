from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity

class Organization(BaseEntity):
    __tablename__ = "organization"

    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    start_year: Mapped[int] = mapped_column(Integer)
    end_year: Mapped[int] = mapped_column(Integer)

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