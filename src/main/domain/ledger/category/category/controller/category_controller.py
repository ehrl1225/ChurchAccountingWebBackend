from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from starlette import status

from common.database import get_db
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie
from domain.ledger.category.category.dto import CreateCategoryDTO
from domain.ledger.category.category.service import CategoryService

router = APIRouter(prefix="/ledger/category", tags=["Category"])

@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_category(
        request: Request,
        response: Response,
        create_category: CreateCategoryDTO,
        db: Session = Depends(get_db),
        category_service:CategoryService = Depends(Provide[Container.category_service])
):
    try:
        me_dto = await get_current_user_from_cookie(request=request,response=response, db=db)

        await category_service.create(db, create_category)
        db.commit()
    except Exception as err:
        db.rollback()
        raise err
