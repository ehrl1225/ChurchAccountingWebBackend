from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from common.database import BaseEntity
from common.enum.status_enum import StatusEnum

class OrganizationInvitation(BaseEntity):
    __tablename__ = "organization_invitation"

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum, name="status_enum"),nullable=False, default=StatusEnum.PENDING)
    invitor_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="organization_invitations"
    )
    member: Mapped["Member"] = relationship(
        "Member",
        foreign_keys=[member_id],
        back_populates="organization_invitations"
    )
    invitor: Mapped["Member"] = relationship(
        "Member",
        foreign_keys=[invitor_id],
        back_populates="invitor_invitations"
    )