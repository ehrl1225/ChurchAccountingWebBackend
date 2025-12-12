from sqlalchemy.orm import Session

from domain.member.entity import Member, RefreshToken


class RefreshTokenRepository:


    def create(self, db:Session, member: Member, token: str):
        refresh_token = RefreshToken()
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token