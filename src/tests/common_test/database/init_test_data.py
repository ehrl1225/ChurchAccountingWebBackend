from sqlalchemy.orm import Session
from datetime import date, timedelta

from common.database import MemberRole, TxType
from domain.file.file.repository import FileRepository
from domain.ledger.category.category.dto import CreateCategoryDTO
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.dto import CreateItemDto
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.event.dto import CreateEventDTO
from domain.ledger.event.repository import EventRepository
from domain.ledger.receipt.dto import CreateReceiptDto
from domain.ledger.receipt.repository import ReceiptRepository
from domain.member.repository import MemberRepository
from common.security.auth_util import hash_password
from domain.organization.joined_organization.dto import CreateJoinedOrganizationDto
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization.dto import OrganizationRequestDto
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.organization_invitation.repository import OrganizationInvitationRepository
from domain.organization.organization.entity import Organization
from domain.organization.organization_invitation.entity import OrganizationInvitation, StatusEnum


async def init_test_database(db:Session):
    # set repository
    member_repository = MemberRepository()
    file_repository = FileRepository()
    category_repository = CategoryRepository()
    item_repository = ItemRepository()
    event_repository = EventRepository()
    receipt_repository = ReceiptRepository()
    organization_repository = OrganizationRepository()
    organization_invitation_repository = OrganizationInvitationRepository()
    joined_organization_repository = JoinedOrganizationRepository()

    category_names = ["a", "b", "c", "d"]
    item_names = [
        ["a_a", "a_b", "a_c"],
        ["b_a", "b_b", "b_c"],
        ["c_a", "c_b", "c_c"],
    ]
    event_names = ["e_a", "e_b", "e_c"]

    users = []

    # use repository
    await member_repository.add_member(
        db=db,
        name="admin",
        email="admin@admin.com",
        hashed_password=hash_password("password")
    )
    for i in range(10):
        user = await member_repository.add_member(
            db=db,
            name=f"test_user{i}",
            email=f"test_user{i}@user.com",
            hashed_password=hash_password("password")
        )
        users.append(user)
    organizations = []
    for i in range(3):
        organization: Organization = await organization_repository.create(
            db=db,
            organization_request_dto=OrganizationRequestDto(
                name=f"organization{i}",
                description=f"description{i}",
                start_year=2025,
                end_year=2025

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
        organizations_invitations = []
        for j in range(5):
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
            selected_invitation:OrganizationInvitation = organizations_invitations[j]
            await organization_invitation_repository.update_invitation_status(
                db=db,
                organization_invitation=selected_invitation,
                staus_enum=StatusEnum.ACCEPTED
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

        for event_name in event_names:
            event = await event_repository.create_event(
                db=db,
                create_event_dto=CreateEventDTO(
                    organization_id=organization.id,
                    year=2025,
                    name=event_name,
                    start_date=date.today(),
                    end_date=date.today()+timedelta(days=1),
                    description=f"description{i}",
                )
            )

        for category_index, category_name in enumerate(category_names):
            category = await category_repository.create_category(
                db=db,
                create_category_dto=CreateCategoryDTO(
                    category_name=category_name,
                    item_name=None,
                    tx_type=TxType.INCOME,
                    organization_id=organization.id,
                    year=2025,
                )
            )
            if category_index == 3:
                continue
            for item_index, item_name in enumerate(item_names[category_index]):
                item = await item_repository.create_item(
                    db=db,
                    create_item_dto=CreateItemDto(
                        category_id=category.id,
                        organization_id=organization.id,
                        item_name=item_name,
                        year=2025,
                    )
                )
                if category_index == 2:
                    continue
                if item_index == 2:
                    continue
                await receipt_repository.create_receipt(
                    db=db,
                    create_receipt_dto=CreateReceiptDto(
                        receipt_image_url=None,
                        paper_date=date.today(),
                        actual_date=None,
                        name=f"receipt_{i}",
                        tx_type=TxType.INCOME,
                        amount=100,
                        category_id=category.id,
                        item_id=item.id,
                        event_id=None,
                        etc=None,
                        organization_id=organization.id,
                        year=2025,
                    )
                )


    db.commit()
