from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from starlette import status

from common.database import get_db
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie, check_member_role
from common.database.member_role import OWNER2READ_WRITE_MASK, OWNER2READ_MASK
from domain.ledger.category.category.dto import CreateCategoryDTO, SearchCategoryParams, DeleteCategoryParams, \
    ImportCategoryDto
from domain.ledger.category.category.dto.edit_all_category_dto import EditAllCategoryDto
from domain.ledger.category.category.dto.edit_category_dto import EditCategoryDto
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
    me_dto = await get_current_user_from_cookie(request=request,response=response, db=db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=create_category.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK,
    )
    await category_service.create(db,create_category)

@router.post("/import")
@inject
async def import_category(
        request: Request,
        response: Response,
        import_category: ImportCategoryDto,
        db: Session = Depends(get_db),
        category_service:CategoryService = Depends(Provide[Container.category_service])
):
    me_dto = await get_current_user_from_cookie(request=request, response=response, db=db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=import_category.from_organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK,
    )
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=import_category.to_organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK,
    )
    await category_service.import_categories(db, import_category)

@router.get("/")
@inject
async def get_categories(
        request: Request,
        response: Response,
        search_category: Annotated[SearchCategoryParams, Depends()],
        db: Session = Depends(get_db),
        category_service:CategoryService = Depends(Provide[Container.category_service])
):
    me_dto = await get_current_user_from_cookie(request=request,response=response, db=db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=search_category.organization_id,
        member_role_mask=OWNER2READ_MASK,
    )
    return await category_service.find_all(db, search_category)

@router.put("/", status_code=status.HTTP_202_ACCEPTED)
@inject
async def update_category(
        request: Request,
        response: Response,
        edit_category:EditCategoryDto,
        db: Session = Depends(get_db),
        category_service:CategoryService = Depends(Provide[Container.category_service])
):
    me_dto = await get_current_user_from_cookie(request=request, response=response, db=db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=edit_category.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK,
    )
    await category_service.update(db, edit_category)

@router.put("/all", status_code=status.HTTP_202_ACCEPTED)
@inject
async def update_all_categories(
        request: Request,
        response: Response,
        edit_all_category: EditAllCategoryDto,
        db: Session = Depends(get_db),
        category_service: CategoryService = Depends(Provide[Container.category_service]),
):
    me_dto = await get_current_user_from_cookie(request=request, response=response, db=db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=edit_all_category.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK,
    )

@router.delete("/", status_code=status.HTTP_202_ACCEPTED)
@inject
async def delete_category(
        request: Request,
        response: Response,
        delete_category: Annotated[DeleteCategoryParams, Depends()],
        db: Session = Depends(get_db),
        category_service:CategoryService = Depends(Provide[Container.category_service])
):
    me_dto = await get_current_user_from_cookie(request=request, response=response, db=db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=delete_category.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK
    )
    await category_service.delete(db, delete_category)