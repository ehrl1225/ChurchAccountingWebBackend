from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Response, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from common.database import get_db
from common.dependency_injector import Container
from domain.file.word.dto.create_settlement_dto import CreateSettlementDto
from domain.file.word.service import WordService
from common.security.rq import get_current_user_from_cookie, check_member_role
from common.enum.member_role import OWNER2READ_MASK

router = APIRouter(prefix="/file/word", tags=["Word"])

@router.get("/")
@inject
async def create_word_file(
        request:Request,
        response:Response,
        create_settlement_dto:Annotated[CreateSettlementDto, Depends()],
        db:AsyncSession = Depends(get_db),
        word_service: WordService = Depends(Provide[Container.word_service])
):
    me_dto = await get_current_user_from_cookie(request, response, db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=create_settlement_dto.organization_id,
        member_role_mask=OWNER2READ_MASK
    )
    stream = await word_service.create_document(db, create_settlement_dto)
    headers = {
        "Content-Disposition": 'attachment; filename="report.docx"',
        "Content-Type": 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    }
    return StreamingResponse(stream, headers=headers)
