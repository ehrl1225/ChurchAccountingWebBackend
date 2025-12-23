import asyncio

from domain.file.file.repository import FileRepository
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.event.repository import EventRepository
from domain.ledger.receipt.repository import ReceiptRepository
from domain.member.repository import MemberRepository
from domain.organization.joined_organization.dto import CreateJoinedOrganizationDto
from domain.organization.organization.dto import OrganizationCreateDto
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.organization_invitation.entity import StatusEnum, OrganizationInvitation
from domain.organization.organization_invitation.repository import OrganizationInvitationRepository
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from common.database import SessionLocal, MemberRole
from common.security.auth_util import hash_password


async def init_dev_data():
    file_repository = FileRepository()
    category_repository = CategoryRepository()
    item_repository = ItemRepository()
    event_repository = EventRepository()
    receipt_repository = ReceiptRepository()
    member_repository = MemberRepository()
    organization_invitation_repository = OrganizationInvitationRepository()
    joined_organization_repository = JoinedOrganizationRepository()
    organization_repository = OrganizationRepository()
    db = SessionLocal()

    admin = await member_repository.add_member(
        db=db,
        name="admin",
        email="admin@admin.com",
        hashed_password=hash_password("password"),
    )
    users = []
    for i in range(10):
        user = await member_repository.add_member(
            db=db,
            name=f"user{i}",
            email=f"user{i}@user.com",
            hashed_password=hash_password("password"),
        )
        users.append(user)
    organizations = []
    for i in range(3):
        organization = await organization_repository.create(
            db=db,
            organization_create_dto=OrganizationCreateDto(
                name=f"organization{i}",
                description=f"made by user{i}",
                start_year=2025,
                end_year=2025,
            )
        )
        organizations.append(organization)
        user = users[i]
        await joined_organization_repository.join_organization(
            db=db,
            create_joined_organization=CreateJoinedOrganizationDto(
                organization_id=organization.id,
                member_id=user.id,
                member_role=MemberRole.OWNER,
            )
        )
        organizations_invitations:list[OrganizationInvitation] = []
        for j in range(10):
            if i==j:
                continue
            invite_user = users[j]
            invitation = await organization_invitation_repository.create_invitation(
                db=db,
                organization=organization,
                member=invite_user,
                me_id=user.id,
            )
            organizations_invitations.append(invitation)
        joined_organizations = []
        for j in range(3):
            selected_invitation = organizations_invitations[j]
            await organization_invitation_repository.update_invitation_status(
                db=db,
                organization_invitation=selected_invitation,
                staus_enum=StatusEnum.ACCEPTED,
            )
            joined_organization = await joined_organization_repository.join_organization(
                db=db,
                create_joined_organization=CreateJoinedOrganizationDto(
                    organization_id=selected_invitation.organization_id,
                    member_id=selected_invitation.member_id,
                    member_role=MemberRole.READ_ONLY
                )
            )
            joined_organizations.append(joined_organization)
        await joined_organization_repository.change_member_role(
            db=db,
            joined_organization=joined_organizations[0],
            member_role=MemberRole.ADMIN,
        )
        await joined_organization_repository.change_member_role(
            db=db,
            joined_organization=joined_organizations[1],
            member_role=MemberRole.READ_WRITE,
        )



    db.commit()



if __name__ == '__main__':
    asyncio.run(init_dev_data())