from sqlalchemy import ForeignKey, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity
from common.enum.member_role import MemberRole
from datetime import datetime

class JoinedOrganization(BaseEntity):
    __tablename__ = "joined_organization"


    member_role: Mapped[MemberRole] = mapped_column(Enum(MemberRole, name="member_role_enum"), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="joined_organizations"
    )
    member: Mapped["Member"] = relationship(
        "Member",
        back_populates="joined_organizations"
    )