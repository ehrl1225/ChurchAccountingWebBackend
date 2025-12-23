from fastapi import BackgroundTasks, HTTPException, Response, Request
from sqlalchemy.orm import Session

from common.security.email_token import generate_verify_token
from common.security.mailer import send_verify_email
from common.security.token_DTO import TokenDTO
from domain.member.repository import MemberRepository, RefreshTokenRepository
from domain.member.entity import Member
from common.env import settings
from common.security.jwt_util import set_token
from common.security.auth_util import get_user_agent, get_client_ip


class AuthService:

    def __init__(self, member_repository: MemberRepository, refresh_token_repository: RefreshTokenRepository):
        self.member_repository = member_repository
        self.refresh_token_repository = refresh_token_repository

    async def send_email_verification(self, email:str, tasks: BackgroundTasks):
        token = generate_verify_token(email)
        server_base_url = settings.profile_config.SERVER_BASE_URL
        verify_url = f"{server_base_url}/member/verify?token={token}"
        tasks.add_task(send_verify_email, email, verify_url)

    async def set_verified(self, db:Session, email:str):
        member = await self.member_repository.find_by_email(db, email)
        if member is None:
            raise HTTPException(status_code=404, detail="Member not found")
        await self.member_repository.modify_member_verification(db, member, True)

    async def create_token(self, db:Session, member:Member, request:Request, response: Response):
        set_token(member,"access", response)
        refresh_token:TokenDTO = set_token(member,"refresh", response)
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        self.refresh_token_repository.create(db, member, refresh_token, ip_address, user_agent)


