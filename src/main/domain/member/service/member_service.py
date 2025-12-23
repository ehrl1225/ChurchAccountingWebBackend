from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from domain.member.dto import RegisterFormDTO, LoginFormDTO
from domain.member.repository import MemberRepository
from domain.member.entity import Member
from common.security.auth_util import hash_password, verify_password

class MemberService:

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    async def add_member(
            self,
            db:Session,
            register_form_DTO: RegisterFormDTO
    ) -> Member:
        return await self.member_repository.add_member(
            db=db,
            name=register_form_DTO.name,
            email=str(register_form_DTO.email),
            hashed_password=hash_password(register_form_DTO.password),
        )

    async def check_email(self, db:Session, email: str) -> bool:
        if await self.member_repository.find_by_email(db, email):
            return True
        return False

    async def verify_password(self, db:Session, login_form: LoginFormDTO) -> Member:
        member: Optional[Member] = await self.member_repository.find_by_email(db, login_form.email)
        if member is None:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        if not verify_password(login_form.password, member.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        return member
