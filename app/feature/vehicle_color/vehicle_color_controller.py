from fastapi import APIRouter, Depends, Path

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_admin, get_current_user
from app.domain.models.vehicle_color_model import VehicleColorModel
from app.feature.vehicle_color.dtos.vehicle_color_dto import (
    VehicleColorCDTO,
    VehicleColorRDTO,
)
from app.feature.vehicle_color.vehicle_color_repository import VehicleColorRepository


class VehicleColorController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=list[VehicleColorRDTO],
            summary="Список цветов транспорта",
            description="Получение списка цветов транспорта",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=VehicleColorRDTO,
            summary="Создать цвет транспорта",
            description="Создать цвет транспорта",
        )(self.create)
        self.router.get(
            "/get-by-id/{id}",
            response_model=VehicleColorRDTO,
            summary="Получить цвет транспорта по идентификатору",
            description="Получить цвет транспорта по идентификатору",
        )(self.get_by_id)
        self.router.put(
            "/update/{id}",
            response_model=VehicleColorRDTO,
            summary="Обновить цвет транспорта по идентификатору",
            description="Обновить цвет транспорта по идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            summary="Удалить цвет транспорта по идентификатору",
            description="Удалить цвет транспорта по идентификатору",
        )(self.delete)

    async def get_all(
        self,
        repo: VehicleColorRepository = Depends(VehicleColorRepository),
        current_user=Depends(get_current_user),
    ):
        result = await repo.get_all()
        return result

    async def get_by_id(
        self,
        id: int = Path(gt=0),
        repo: VehicleColorRepository = Depends(VehicleColorRepository),
        current_user=Depends(get_current_user),
    ):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Цвета транспорта не найден")
        return result

    async def create(
        self,
        organization_type_dto: VehicleColorCDTO,
        repo: VehicleColorRepository = Depends(VehicleColorRepository),
        current_user=Depends(check_admin),
    ):
        existed_organization_type = await repo.get_filtered(
            filters={"value": organization_type_dto.value}
        )
        if existed_organization_type is not None:
            raise AppExceptionResponse.bad_request(
                message="Такое значение для цвета транспорта уже существует"
            )
        VehicleColor = VehicleColorModel(**organization_type_dto.dict())
        result = await repo.create(obj=VehicleColor)
        return result

    async def update(
        self,
        organization_type_dto: VehicleColorCDTO,
        id: int = Path(gt=0),
        repo: VehicleColorRepository = Depends(VehicleColorRepository),
        current_user=Depends(check_admin),
    ):
        VehicleColor = await repo.get(id=id)
        if VehicleColor is None:
            raise AppExceptionResponse.not_found(message="Цвет не найден")
        existed_organization_type = await repo.get_filtered(
            filters={"value": organization_type_dto.value}
        )
        if (
            existed_organization_type is not None
            and existed_organization_type.id != VehicleColor.id
        ):
            raise AppExceptionResponse.bad_request(
                message="Такое значение для цвета транспорта уже существует"
            )
        result = await repo.update(obj=VehicleColor, dto=organization_type_dto)
        return result

    async def delete(
        self,
        id: int = Path(gt=0),
        repo: VehicleColorRepository = Depends(VehicleColorRepository),
        current_user=Depends(check_admin),
    ) -> None:
        await repo.delete(id=id)
