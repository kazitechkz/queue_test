from typing import Optional, List

from fastapi import APIRouter, Depends, Query, Path

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_current_user, check_admin
from app.domain.models.region_model import RegionModel
from app.feature.region.dtos.region_dto import RegionRDTO, RegionCDTO
from app.feature.region.region_repository import RegionRepository


class RegionController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get(
            "/",
            response_model=List[RegionRDTO],
            summary="Список регионов",
            description="Получение списка регионов"
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=RegionRDTO,
            summary="Создать регион",
            description="Создание региона"
        )(self.create)
        self.router.get(
            "/get-by-id/{id}",
            response_model=RegionRDTO,
            summary="Получить регион по идентификатору",
            description="Получение региона по идентификатору"
        )(self.get_by_id)
        self.router.put(
            "/update/{id}",
            response_model=RegionRDTO,
            summary="Обновить регион по идентификатору",
            description="Обновить регион по идентификатору"
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            summary="Удалить регион по идентификатору",
            description="Удалить регион по идентификатору"
        )(self.delete)

    async def get_all(
            self, repo: RegionRepository = Depends(RegionRepository),
            current_user=Depends(get_current_user)
    ):
        result = await repo.get_all()
        return result

    async def get_by_id(
            self,
            id: int = Path(gt=0),
            repo: RegionRepository = Depends(RegionRepository),
            current_user=Depends(get_current_user)
    ):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Регион не найден")
        return result

    async def create(
            self,
            organization_type_dto: RegionCDTO,
            repo: RegionRepository = Depends(RegionRepository),
            current_user=Depends(check_admin)
    ):
        existed_organization_type = await repo.get_filtered(filters={"value": organization_type_dto.value})
        if (existed_organization_type is not None):
            raise AppExceptionResponse.bad_request(message="Такое значение для региона уже существует")
        Region = RegionModel(**organization_type_dto.dict())
        result = await repo.create(obj=Region)
        return result

    async def update(
            self,
            organization_type_dto: RegionCDTO,
            id: int = Path(gt=0),
            repo: RegionRepository = Depends(RegionRepository),
            current_user=Depends(check_admin)
    ):
        Region = await repo.get(id=id)
        if Region is None:
            raise AppExceptionResponse.not_found(message="Регион не найден")
        existed_organization_type = await repo.get_filtered(filters={"value": organization_type_dto.value})
        if (existed_organization_type is not None and existed_organization_type.id != Region.id):
            raise AppExceptionResponse.bad_request(message="Такое значение для региона уже существует")
        result = await repo.update(obj=Region, dto=organization_type_dto)
        return result

    async def delete(
            self,
            id: int = Path(gt=0),
            repo: RegionRepository = Depends(RegionRepository),
            current_user=Depends(check_admin)
    ):
        await repo.delete(id=id)
