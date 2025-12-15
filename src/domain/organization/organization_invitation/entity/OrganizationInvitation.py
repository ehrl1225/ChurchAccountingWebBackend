from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from common.database import BaseEntity
from domain.organization.organization_invitation.entity import StatusEnum

class OrganizationInvitation(BaseEntity):
    __tablename__ = "organization_invitation"

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum, name="status_enum"),default=StatusEnum.PENDING)

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="organization_invitations"
    )
    member: Mapped["Member"] = relationship(
        "Member",
        back_populates="organization_invitations"
    )