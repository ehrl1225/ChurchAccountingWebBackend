from dependency_injector import containers, providers
from redis import Redis
from rq import Queue

from common.redis import get_redis
from common.redis.redis_client import get_queue
from domain.file.word.service import WordService
from domain.member.repository import MemberRepository, RefreshTokenRepository
from domain.member.service import MemberService
from domain.member.service.auth_service import AuthService
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.organization.service import OrganizationService
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization_invitation.repository import OrganizationInvitationRepository
from domain.organization.organization_invitation.service import OrganizationInvitationService
from domain.organization.joined_organization.service import JoinedOrganizationService
from domain.file.file.service import FileService, StorageService, LocalStorageService, S3StorageService
from domain.file.file.repository import FileRepository
from domain.ledger.category.category.repository import CategoryRepository
from domain.ledger.category.item.repository import ItemRepository
from domain.ledger.event.repository import EventRepository
from domain.ledger.receipt.repository import ReceiptRepository
from domain.ledger.category.category.service import CategoryService
from domain.ledger.category.item.service import ItemService
from domain.ledger.event.service import EventService
from domain.ledger.receipt.service import ReceiptService

from common.env import settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["domain"],
        modules=["app_setting", "common.security.rq"]
    )


    member_repository: MemberRepository = providers.Singleton(MemberRepository)
    refresh_token_repository: RefreshTokenRepository = providers.Singleton(RefreshTokenRepository)
    organization_repository: OrganizationRepository = providers.Singleton(OrganizationRepository)
    joined_organization_repository: JoinedOrganizationRepository = providers.Singleton(JoinedOrganizationRepository)
    organization_invitation_repository: OrganizationInvitationRepository = providers.Singleton(OrganizationInvitationRepository)
    file_repository: FileRepository = providers.Singleton(FileRepository)
    category_repository: CategoryRepository = providers.Singleton(CategoryRepository)
    item_repository: ItemRepository = providers.Singleton(ItemRepository)
    event_repository: EventRepository = providers.Singleton(EventRepository)
    receipt_repository: ReceiptRepository = providers.Singleton(ReceiptRepository)

    redis_client: Redis = providers.Singleton(get_redis)
    redis_queue:Queue = providers.Singleton(get_queue)

    member_service: MemberService = providers.Singleton(MemberService, member_repository)
    auth_service: AuthService = providers.Singleton(
        AuthService,
        member_repository,
        refresh_token_repository
    )
    organization_service: OrganizationService = providers.Singleton(
        OrganizationService,
        organization_repository,
        member_repository,
        joined_organization_repository,
    )
    organization_invitation_service: OrganizationInvitationService = providers.Singleton(
        OrganizationInvitationService,
        organization_invitation_repository,
        organization_repository,
        member_repository,
        joined_organization_repository,
    )
    joined_organization_service: JoinedOrganizationService = providers.Singleton(
        JoinedOrganizationService,
        joined_organization_repository,
        member_repository,
        organization_repository,
        redis_client,
    )
    storage_service: providers.Provider[StorageService] = providers.Selector(
        lambda : settings.PROFILE,
        prod=providers.Singleton(S3StorageService),
        dev=providers.Singleton(LocalStorageService),
        test=providers.Singleton(LocalStorageService),
    )
    file_service:FileService = providers.Singleton(FileService, file_repository)
    category_service:CategoryService = providers.Singleton(
        CategoryService,
        category_repository,
        item_repository,
        organization_repository,
    )
    item_service:ItemService = providers.Singleton(
        ItemService,
        category_repository,
        item_repository,
        organization_repository,
    )
    event_service:EventService = providers.Singleton(
        EventService,
        event_repository,
        organization_repository
    )
    receipt_service:ReceiptService = providers.Singleton(
        ReceiptService,
        receipt_repository,
        category_repository,
        item_repository,
        event_repository,
        organization_repository,
        member_repository,
        joined_organization_repository,
        redis_queue,
    )
    word_service:WordService = providers.Singleton(
        WordService,
        organization_repository,
        receipt_service,
    )