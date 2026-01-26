from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import get_db
from common.dependency_injector import Container
from common.security.rq import get_current_user_from_cookie, check_member_role
from common.enum.member_role import OWNER2READ_WRITE_MASK, OWNER2READ_MASK
from domain.ledger.category.category.dto.request import CreateCategoryDTO, SearchCategoryParams, DeleteCategoryParams, \
    ImportCategoryDto, EditCategoryDto
from domain.ledger.category.category.dto.response import EditAllDto
from domain.ledger.category.category.service import CategoryService

router = APIRouter(prefix="/ledger/category", tags=["Category"])

@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_category(
        request: Request,
        response: Response,
        create_category: CreateCategoryDTO,
        db: AsyncSession = Depends(get_db),
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
        db: AsyncSession = Depends(get_db),
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
        db: AsyncSession = Depends(get_db),
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
        db: AsyncSession = Depends(get_db),
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
        edit_all_dto: EditAllDto,
        db: AsyncSession = Depends(get_db),
        category_service: CategoryService = Depends(Provide[Container.category_service]),
):
    me_dto = await get_current_user_from_cookie(request=request, response=response, db=db)
    await check_member_role(
        db=db,
        member_id=me_dto.id,
        organization_id=edit_all_dto.organization_id,
        member_role_mask=OWNER2READ_WRITE_MASK,
    )
    await category_service.edit_all(db, edit_all_dto)

@router.delete("/", status_code=status.HTTP_202_ACCEPTED)
@inject
async def delete_category(
        request: Request,
        response: Response,
        delete_category: Annotated[DeleteCategoryParams, Depends()],
        db: AsyncSession = Depends(get_db),
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