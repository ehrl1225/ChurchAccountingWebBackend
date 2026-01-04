from dependency_injector.wiring import inject, Provide
from fastapi import HTTPException, Request, Response, Depends, status
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Optional

from common.database.member_role import get_member_roles
from domain.member.repository import RefreshTokenRepository, MemberRepository
from domain.organization.joined_organization.repository import JoinedOrganizationRepository
from domain.organization.organization.repository import OrganizationRepository
from domain.organization.joined_organization.entity import JoinedOrganization
from .jwt_util import decode_token, dict_to_member, set_token
from domain.member.entity import RefreshToken
from .member_DTO import MemberDTO
from common.dependency_injector import Container



def get_current_user(token: str) -> Optional[MemberDTO]:
    try:
        payload:dict[str, str] = decode_token(token)
        return dict_to_member(payload)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

@inject
async def get_current_user_from_cookie(
        request: Request,
        response: Response,
        db:Session,
        refresh_token_repository: RefreshTokenRepository = Depends(Provide[Container.refresh_token_repository])
) -> MemberDTO:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    if access_token is not None:
        try:
            decoded_access_token = decode_token(access_token)
            return dict_to_member(decoded_access_token)
        except JWTError:
            pass

    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    try:
        decoded_refresh_token = decode_token(refresh_token)
        jti = decoded_refresh_token["jti"]
        if jti is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        db_token:RefreshToken|None = refresh_token_repository.find_refresh_token(db, jti)
        if db_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        member = db_token.member
        set_token(member,"access", response)
        return dict_to_member(decoded_refresh_token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

@inject
async def check_member_role(
        db:Session,
        member_id: int,
        organization_id: int,
        member_role_mask: int,
        member_repository: MemberRepository = Depends(Provide[Container.member_repository]),
        organization_repository: OrganizationRepository = Depends(Provide[Container.organization_repository]),
        joined_organization_repository: JoinedOrganizationRepository = Depends(Provide[Container.joined_organization_repository])
):
    member_roles = get_member_roles(member_role_mask)
    organization = await organization_repository.find_by_id(db, organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    member = await member_repository.find_by_id(db, member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    joined_organization:JoinedOrganization = await joined_organization_repository.find_by_member_and_organization(db, member, organization)
    if not joined_organization:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Member didn't joined organization")
    if joined_organization.member_role not in member_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Member role not exist")
