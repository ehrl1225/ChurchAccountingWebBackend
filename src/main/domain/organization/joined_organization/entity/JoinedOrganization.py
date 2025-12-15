from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity, MemberRole

class JoinedOrganization(BaseEntity):
    __tablename__ = "joined_organization"


    member_role: Mapped[MemberRole] = mapped_column(Enum(MemberRole, name="member_role_enum"), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="joined_organization"
    )
    member: Mapped["Member"] = relationship(
        "Member",
        back_populates="joined_organization"
    )