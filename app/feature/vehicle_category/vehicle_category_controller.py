from typing import Optional, List

from fastapi import APIRouter, Depends, Query, Path

from app.core.app_exception_response import AppExceptionResponse
from app.domain.models.vehicle_category_model import VehicleCategoryModel
from app.feature.vehicle_category.dtos.vehicle_category_dto import VehicleCategoryRDTO, VehicleCategoryCDTO
from app.feature.vehicle_category.vehicle_category_repository import VehicleCategoryRepository


class VehicleCategoryController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", response_model=List[VehicleCategoryRDTO])(self.get_all)
        self.router.post("/create", response_model=VehicleCategoryRDTO)(self.create)
        self.router.get("/get_by_id/{id}", response_model=VehicleCategoryRDTO)(self.get_by_id)
        self.router.put("/update/{id}", response_model=VehicleCategoryRDTO)(self.update)
        self.router.delete("/delete/{id}")(self.delete)

    async def get_all(self, repo: VehicleCategoryRepository = Depends(VehicleCategoryRepository)):
        result = await repo.get_all()
        return result

    async def get_by_id(self, id: int = Path(gt=0), repo: VehicleCategoryRepository = Depends(VehicleCategoryRepository)):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Категория транспорта не найден")
        return result

    async def create(self, organization_type_dto: VehicleCategoryCDTO, repo: VehicleCategoryRepository = Depends(VehicleCategoryRepository)):
        existed_organization_type = await repo.get_filtered(filters={"value":organization_type_dto.value})
        if (existed_organization_type is not None):
            raise AppExceptionResponse.bad_request(message="Такое значение для категории транспорта уже существует")
        VehicleCategory = VehicleCategoryModel(**organization_type_dto.dict())
        result = await repo.create(obj=VehicleCategory)
        return result

    async def update(self, organization_type_dto: VehicleCategoryCDTO, id: int = Path(gt=0),
                     repo: VehicleCategoryRepository = Depends(VehicleCategoryRepository)):
        VehicleCategory = await repo.get(id=id)
        if VehicleCategory is None:
            raise AppExceptionResponse.not_found(message="Цвет не найден")
        existed_organization_type = await repo.get_filtered(filters={"value":organization_type_dto.value})
        if (existed_organization_type is not None and existed_organization_type.id != VehicleCategory.id):
            raise AppExceptionResponse.bad_request(message="Такое значение для категории транспорта уже существует")
        result = await repo.update(obj=VehicleCategory, dto=organization_type_dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: VehicleCategoryRepository = Depends(VehicleCategoryRepository)):
        await repo.delete(id=id)