from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity

class Organization(BaseEntity):
    __tablename__ = "organization"

    type: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    start_year: Mapped[int] = mapped_column(Integer)
    end_year: Mapped[int] = mapped_column(Integer)

    organization_invitations: Mapped[list["OrganizationInvitation"]] = relationship(
        "OrganizationInvitation",
        back_populates="organization",
    )

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "organization"
    }