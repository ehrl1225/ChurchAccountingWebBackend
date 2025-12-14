from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Optional, Literal
from common.env import settings
from domain.member.entity import Member
from fastapi import HTTPException, Response
from .member_DTO import MemberDTO
from .token_DTO import TokenDTO
import uuid

def create_token(data:dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token:str) -> dict:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return payload

def member_to_dict(member: Member, scope: str, jti: str) -> dict:
    return {
        "id": member.id,
        "email": member.email,
        "scope": scope,
        "jti": jti
    }

def dict_to_member(member: dict) -> MemberDTO:
    if "id" not in member:
        raise HTTPException(status_code=404, detail="Invalid token")
    if "email" not in member:
        raise HTTPException(status_code=404, detail="Invalid token")
    return MemberDTO(**member)

def set_token(member: Member, scope: Literal["access", "refresh"], response: Response) -> TokenDTO:
    token_time: timedelta = timedelta(minutes=15)
    match scope:
        case "access":
            token_time = timedelta(minutes=settings.profile_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        case "refresh":
            token_time = timedelta(days=settings.profile_config.REFRESH_TOKEN_EXPIRE_DAYS)
    jti = uuid.uuid4().hex
    token = create_token(member_to_dict(member, scope, jti), token_time)
    response.set_cookie(
        key=f"{scope}_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return TokenDTO(token=token, jti=jti)