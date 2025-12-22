from sqlalchemy.orm import Session

from domain.file.file.repository import FileRepository
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.event.repository import EventRepository
from domain.ledger.receipt.repository import ReceiptRepository
from domain.member.repository import MemberRepository
from common.security.auth_util import hash_password
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.organization_invitation.repository import OrganizationInvitationRepository


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

    # use repository
    await member_repository.add_member(
        db=db,
        name="admin",
        email="admin@admin.com",
        hashed_password=hash_password("password")
    )