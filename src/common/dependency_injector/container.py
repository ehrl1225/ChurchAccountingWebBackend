from dependency_injector import containers, providers
from domain.member.repository import MemberRepository, RefreshTokenRepository
from domain.member.service import MemberService
from domain.member.service.auth_service import AuthService
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.organization.service import OrganizationService
from domain.organization.joined_organization.repository import JoinedOrganizationRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["domain"],
        modules=["main"]
    )
    member_repository: MemberRepository = providers.Singleton(MemberRepository)
    refresh_token_repository: RefreshTokenRepository = providers.Singleton(RefreshTokenRepository)
    organization_repository: OrganizationRepository = providers.Singleton(OrganizationRepository)
    joined_organization_repository: JoinedOrganizationRepository = providers.Singleton(JoinedOrganizationRepository)

    member_service: MemberService = providers.Singleton(MemberService, member_repository)
    auth_service: AuthService = providers.Singleton(AuthService, member_repository, refresh_token_repository)
    organization_service: OrganizationService = providers.Singleton(
        OrganizationService,
        organization_repository,
        member_repository,
        joined_organization_repository,
    )
