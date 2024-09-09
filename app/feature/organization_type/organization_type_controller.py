from typing import Optional, List

from fastapi import APIRouter, Depends, Query, Path

from app.core.app_exception_response import AppExceptionResponse
from app.domain.models.organization_type_model import OrganizationTypeModel
from app.feature.organization_type.dtos.organization_type_dto import OrganizationTypeRDTO, OrganizationTypeCDTO
from app.feature.organization_type.organization_type_repository import OrganizationTypeRepository


class OrganizationTypeController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", response_model=List[OrganizationTypeRDTO])(self.get_all)
        self.router.post("/create", response_model=OrganizationTypeRDTO)(self.create)
        self.router.get("/get_by_id/{id}", response_model=OrganizationTypeRDTO)(self.get_by_id)
        self.router.put("/update/{id}", response_model=OrganizationTypeRDTO)(self.update)
        self.router.delete("/delete/{id}")(self.delete)

    async def get_all(self, repo: OrganizationTypeRepository = Depends(OrganizationTypeRepository)):
        result = await repo.get_all()
        return result

    async def get_by_id(self, id: int = Path(gt=0), repo: OrganizationTypeRepository = Depends(OrganizationTypeRepository)):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Тип пользователя не найден")
        return result

    async def create(self, organization_type_dto: OrganizationTypeCDTO, repo: OrganizationTypeRepository = Depends(OrganizationTypeRepository)):
        existed_organization_type = await repo.get_filtered(filters={"value":organization_type_dto.value})
        if (existed_organization_type is not None):
            raise AppExceptionResponse.bad_request(message="Такое значение для типа организации уже существует")
        OrganizationType = OrganizationTypeModel(**organization_type_dto.dict())
        result = await repo.create(obj=OrganizationType)
        return result

    async def update(self, organization_type_dto: OrganizationTypeCDTO, id: int = Path(gt=0),
                     repo: OrganizationTypeRepository = Depends(OrganizationTypeRepository)):
        OrganizationType = await repo.get(id=id)
        if OrganizationType is None:
            raise AppExceptionResponse.not_found(message="Тип Организации не найден")
        existed_organization_type = await repo.get_filtered(filters={"value":organization_type_dto.value})
        if (existed_organization_type is not None and existed_organization_type.id != OrganizationType.id):
            raise AppExceptionResponse.bad_request(message="Такое значение для типа организации уже существует")
        result = await repo.update(obj=OrganizationType, dto=organization_type_dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: OrganizationTypeRepository = Depends(OrganizationTypeRepository)):
        await repo.delete(id=id)