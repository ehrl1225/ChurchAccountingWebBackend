from sqlalchemy.orm import Session
from common.security.auth_util import hash_jwt_token
from common.security.token_DTO import TokenDTO
from domain.member.entity import Member, RefreshToken
from datetime import datetime, timedelta
from common.env import settings
from typing import Optional

class RefreshTokenRepository:


    def create(self, db:Session, member: Member, token:TokenDTO, ip_address:Optional[str], user_agent:Optional[str]) -> RefreshToken:
        hashed_token = hash_jwt_token(token.token)
        refresh_token = RefreshToken(
            hashed_token=hashed_token,
            jti=token.jti,
            issued_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=settings.profile_config.REFRESH_TOKEN_EXPIRE_DAYS),
            ip_address=ip_address,
            user_agent=user_agent,
            member_id=member.id,
            member=member,
        )
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token