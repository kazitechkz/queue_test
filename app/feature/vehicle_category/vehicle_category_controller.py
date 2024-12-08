from fastapi import APIRouter, Depends, Path

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_admin, get_current_user
from app.domain.models.vehicle_category_model import VehicleCategoryModel
from app.feature.vehicle_category.dtos.vehicle_category_dto import (
    VehicleCategoryCDTO,
    VehicleCategoryRDTO,
)
from app.feature.vehicle_category.vehicle_category_repository import (
    VehicleCategoryRepository,
)


class VehicleCategoryController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=list[VehicleCategoryRDTO],
            summary="Список категорий транспорта",
            description="Получение категорий транспорта",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=VehicleCategoryRDTO,
            summary="Создать категорию транспорта",
            description="Создать категорию транспорта",
        )(self.create)
        self.router.get(
            "/get-by-id/{id}",
            response_model=VehicleCategoryRDTO,
            summary="Получить категорию транспорта по идентификатору",
            description="Получить категорию транспорта по идентификатору",
        )(self.get_by_id)
        self.router.put(
            "/update/{id}",
            response_model=VehicleCategoryRDTO,
            summary="Обновить категорию транспорта по идентификатору",
            description="Обновить категорию транспорта по идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            summary="Удалить категорию транспорта по идентификатору",
            description="Удалить категорию транспорта по идентификатору",
        )(self.delete)

    async def get_all(
        self,
        repo: VehicleCategoryRepository = Depends(VehicleCategoryRepository),
        current_user=Depends(get_current_user),
    ):
        result = await repo.get_all()
        return result

    async def get_by_id(
        self,
        id: int = Path(gt=0),
        repo: VehicleCategoryRepository = Depends(VehicleCategoryRepository),
        current_user=Depends(get_current_user),
    ):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Категория транспорта не найден")
        return result

    async def create(
        self,
        organization_type_dto: VehicleCategoryCDTO,
        repo: VehicleCategoryRepository = Depends(VehicleCategoryRepository),
        current_user=Depends(check_admin),
    ):
        existed_organization_type = await repo.get_filtered(
            filters={"value": organization_type_dto.value}
        )
        if existed_organization_type is not None:
            raise AppExceptionResponse.bad_request(
                message="Такое значение для категории транспорта уже существует"
            )
        VehicleCategory = VehicleCategoryModel(**organization_type_dto.dict())
        result = await repo.create(obj=VehicleCategory)
        return result

    async def update(
        self,
        organization_type_dto: VehicleCategoryCDTO,
        id: int = Path(gt=0),
        repo: VehicleCategoryRepository = Depends(VehicleCategoryRepository),
        current_user=Depends(check_admin),
    ):
        VehicleCategory = await repo.get(id=id)
        if VehicleCategory is None:
            raise AppExceptionResponse.not_found(message="Цвет не найден")
        existed_organization_type = await repo.get_filtered(
            filters={"value": organization_type_dto.value}
        )
        if (
            existed_organization_type is not None
            and existed_organization_type.id != VehicleCategory.id
        ):
            raise AppExceptionResponse.bad_request(
                message="Такое значение для категории транспорта уже существует"
            )
        result = await repo.update(obj=VehicleCategory, dto=organization_type_dto)
        return result

    async def delete(
        self,
        id: int = Path(gt=0),
        repo: VehicleCategoryRepository = Depends(VehicleCategoryRepository),
        current_user=Depends(check_admin),
    ) -> None:
        await repo.delete(id=id)
