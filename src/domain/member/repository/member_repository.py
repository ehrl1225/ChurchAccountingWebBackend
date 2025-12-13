from fastapi import HTTPException
from sqlalchemy.orm import Session

from domain.member.dto import RegisterFormDTO
from domain.member.entity import Member
from typing import Type, Optional


class MemberRepository:

    async def add_member(
            self,
            db: Session,
            name: str,
            email: str,
            hashed_password: str
    ) -> Member:
        member: Member = Member(
            name=name,
            email=email,
            hashed_password=hashed_password,
            email_verified=False
        )
        db.add(member)
        db.commit()
        db.refresh(member)
        return member

    async def get_member_by_email(self, db:Session, email:str) -> Optional[Member]:
        member: Optional[Member]  = db.query(Member).filter_by(email=email).one_or_none()
        return member

    async def modify_member_verification(
            self,
            db: Session,
            member: Member,
            email_verified: bool
    ) -> Member:
        member.email_verified = email_verified
        db.commit()
        db.refresh(member)
        return member

    async def find_by_id(
            self,
            db: Session,
            id: int
    ):
        member: Member = db.query(Member).get(id)
        return member