from dependency_injector import containers, providers
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
from common.env import settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["domain"],
        modules=["main", "common.security.rq"]
    )
    member_repository: MemberRepository = providers.Singleton(MemberRepository)
    refresh_token_repository: RefreshTokenRepository = providers.Singleton(RefreshTokenRepository)
    organization_repository: OrganizationRepository = providers.Singleton(OrganizationRepository)
    joined_organization_repository: JoinedOrganizationRepository = providers.Singleton(JoinedOrganizationRepository)
    organization_invitation_repository: OrganizationInvitationRepository = providers.Singleton(OrganizationInvitationRepository)
    file_repository: FileRepository = providers.Singleton(FileRepository)

    member_service: MemberService = providers.Singleton(MemberService, member_repository)
    auth_service: AuthService = providers.Singleton(AuthService, member_repository, refresh_token_repository)
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
        organization_repository
    )
    storage_service: providers.Provider[StorageService] = providers.Selector(
        lambda : settings.PROFILE,
        prod=providers.Singleton(S3StorageService),
        dev=providers.Singleton(LocalStorageService),
        test=providers.Singleton(LocalStorageService),
    )
    file_service:FileService = providers.Singleton(FileService, file_repository)
