from datetime import timedelta

from dependency_injector.wiring import inject, Provide
from fastapi import HTTPException, status, Request, Response, Depends
from jose import JWTError
from sqlalchemy.orm import Session

from domain.member.repository import RefreshTokenRepository
from .jwt_util import decode_token, dict_to_member, member_to_dict, set_token
from domain.member.entity import Member, RefreshToken
from .member_DTO import MemberDTO
from typing import Optional

from common.dependency_injector import Container


def get_current_user(token: str) -> Optional[MemberDTO]:
    try:
        payload:dict[str, str] = decode_token(token)
        return dict_to_member(payload)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@inject
def get_current_user_from_cookie(
        request: Request,
        response: Response,
        db:Session,
        refresh_token_repository: RefreshTokenRepository = Depends(Provide[Container.refresh_token_repository])
) -> MemberDTO:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if access_token is None:
        if refresh_token is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        decoded_refresh_token = decode_token(refresh_token)
        jti = decoded_refresh_token["jti"]
        if jti is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        db_token:RefreshToken|None = refresh_token_repository.find_refresh_token(db, jti)
        if db_token is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        member = db_token.member
        set_token(member,"access", response)
        return dict_to_member(decoded_refresh_token)
    decoded_access_token = decode_token(access_token)
    return dict_to_member(decoded_access_token)
