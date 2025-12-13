from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship


from domain.member.entity import Member

class OrganizationMember(Member):

    organization_invitations : Mapped[list["OrganizationInvitation"]] = relationship(
        "OrganizationInvitation",
        back_populates="organization_member",
    )

    __mapper_args__ = {
        "polymorphic_identity": "organization_member"
    }