from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.member.entity import Member
from typing import Optional


class MemberRepository:

    async def add_member(
            self,
            db: AsyncSession,
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
        await db.flush()
        await db.refresh(member)
        return member

    async def find_by_email(self, db:AsyncSession, email:str) -> Optional[Member]:
        query = (select(Member)
                 .filter(Member.email == email))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def modify_member_verification(
            self,
            db: AsyncSession,
            member: Member,
            email_verified: bool
    ) -> Member:
        member.email_verified = email_verified
        await db.flush()
        await db.refresh(member)
        return member

    async def find_by_id(
            self,
            db: AsyncSession,
            id: int
    ) -> Optional[Member]:
        member: Optional[Member] = await db.get(Member, id)
        return member