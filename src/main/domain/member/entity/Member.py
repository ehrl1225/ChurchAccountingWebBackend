from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import BaseEntity

class Member(BaseEntity):
    __tablename__ = 'member'
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="member"
    )
    organization_invitations: Mapped[list["OrganizationInvitation"]] = relationship(
        "OrganizationInvitation",
        primaryjoin="Member.id == OrganizationInvitation.member_id",
        back_populates="member",
    )
    joined_organizations: Mapped[list["JoinedOrganization"]] = relationship(
        "JoinedOrganization",
        back_populates="member",
    )
    invitor_invitations: Mapped[list["OrganizationInvitation"]] = relationship(
        "OrganizationInvitation",
        primaryjoin="Member.id == OrganizationInvitation.invitor_id",
        back_populates="invitor",
    )