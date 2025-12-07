from dependency_injector import containers, providers
from domain.member.repository import MemberRepository
from domain.member.service import MemberService
from domain.member.service.auth_service import AuthService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["domain"],
        modules=["main"]
    )
    member_repository: MemberRepository = providers.Singleton(MemberRepository)
    member_service: MemberService = providers.Singleton(MemberService, member_repository)
    auth_service: AuthService = providers.Singleton(AuthService, member_repository)