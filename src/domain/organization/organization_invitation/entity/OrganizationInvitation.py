from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from common.database import BaseEntity

class OrganizationInvitation(BaseEntity):
    __tablename__ = "organization_invitation"

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    organization_member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="organization_invitations"
    )
    organization_member: Mapped["OrganizationMember"] = relationship(
        "OrganizationMember",
        back_populates="organization_invitations"
    )