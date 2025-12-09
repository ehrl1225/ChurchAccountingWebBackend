from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from domain.member.entity import Member

class OrganizationMember(Member):

    organization_invitations : Mapped[list["OrganizationInvitation"]] = relationship(
        "OrganizationInvitation",
        back_populates="organization_invitation",
    )

    __mapper_args__ = {
        "polymorphic_identity": "organization_member"
    }