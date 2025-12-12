from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Response, Request
from sqlalchemy.orm import Session

from common.database import get_db
from common.dependency_injector import Container
from common.security.email_token import verify_token
from common.env import settings
from domain.member.dto import RegisterFormDTO, LoginFormDTO
from domain.member.service import MemberService
from domain.member.service.auth_service import AuthService
from domain.member.entity import Member

router = APIRouter(prefix="/member", tags=["member"])


@router.post("/register")
@inject
async def register_member(
        registerForm: RegisterFormDTO,
        tasks: BackgroundTasks,
        db: Session = Depends(get_db),
        member_service: MemberService = Depends(Provide[Container.member_service]),
        auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    email: str = str(registerForm.email)
    if not member_service.check_email(db, email):
        raise HTTPException(status_code=400, detail="Invalid email")
    await member_service.add_member(db, registerForm)
    # await auth_service.send_email_verification(email,tasks)

@router.post("/login")
@inject
async def login_member(
        loginForm: LoginFormDTO,
        request: Request,
        response:Response,
        db: Session = Depends(get_db),
        member_service: MemberService = Depends(Provide[Container.member_service]),
        auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    member = await member_service.verify_password(db, loginForm)
    await auth_service.create_token(db, member,request, response)


@router.get("/verify")
@inject
async def verify_email(
        token: str = Query(...),
        db: Session = Depends(get_db),
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    try:
        subject = verify_token(token, settings.profile_config.VERIFY_TOKEN_EXPIRATION)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")
    await auth_service.set_verified(db,subject)

