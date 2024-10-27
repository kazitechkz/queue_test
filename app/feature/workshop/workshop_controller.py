from typing import List

from fastapi import APIRouter, Depends, Path

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_current_user, check_admin
from app.domain.models.workshop_model import WorkshopModel
from app.feature.factory.factory_repository import FactoryRepository
from app.feature.workshop.dtos.workshop_dto import WorkshopRDTO, WorkshopCDTO
from app.feature.workshop.workshop_repository import WorkshopRepository


class WorkshopController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get(
            "/",
            response_model=List[WorkshopRDTO],
            summary="Получить список всех цехов",
            description="Получить список всех цехов"
        )(self.all)
        self.router.post(
            "/create",
            response_model=WorkshopRDTO,
            summary="Создать цех",
            description="Создание цеха"
        )(self.create)
        self.router.get(
            "/get/{id}",
            response_model=WorkshopRDTO,
            summary="Получить цех по id",
            description="Получение цеха по id"
        )(self.get)
        self.router.get(
            "/get-by-sap/{sap_id}",
            response_model=WorkshopRDTO,
            summary="Получить цех по id в SAP",
            description="Получение цеха по id в SAP"
        )(self.get_by_sap)
        self.router.put(
            "/update/{id}",
            response_model=WorkshopRDTO,
            summary="Обновить цех по id",
            description="Обновление цеха по id"
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            summary="Удалить цех по id",
            description="Удаление цеха по id"
        )(self.delete)

    async def all(
            self,
            repo: WorkshopRepository = Depends(WorkshopRepository),
            current_user=Depends(get_current_user)
    ):
        result = await repo.get_all()
        return result

    async def get(
            self,
            id: int = Path(gt=0),
            repo: WorkshopRepository = Depends(WorkshopRepository),
            current_user=Depends(get_current_user)
    ):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Цех не найден")
        return result

    async def get_by_sap(
            self,
            sap_id: int = Path(gt=0),
            repo: WorkshopRepository = Depends(WorkshopRepository),
            current_user=Depends(get_current_user)
    ):
        result = await repo.get_filtered(filters={"sap_id": sap_id})
        if result is None:
            raise AppExceptionResponse.not_found(message="Цех не найден")
        return result

    async def create(
            self,
            dto: WorkshopCDTO,
            repo: WorkshopRepository = Depends(WorkshopRepository),
            factoryRepo:FactoryRepository = Depends(FactoryRepository),
            current_user=Depends(check_admin)
    ):
        existed = await repo.get_filtered(filters={"sap_id": dto.sap_id})
        if (existed is not None):
            raise AppExceptionResponse.bad_request(message="Цех с таким sap_id уже существует")
        factory = factoryRepo.get(id=dto.factory_id)
        if factory is None:
            raise AppExceptionResponse.bad_request(message="Цеха не существует")
        workshop = WorkshopModel(**dto.dict())
        result = await repo.create(obj=workshop)
        return result

    async def update(self, dto: WorkshopCDTO, id: int = Path(gt=0),
                     repo: WorkshopRepository = Depends(WorkshopRepository),
                     factoryRepo: FactoryRepository = Depends(FactoryRepository),
                     current_user=Depends(check_admin)
                     ):
        existed = await repo.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Цех не найден")
        existed_sap_workshop = await repo.get_filtered(filters={"sap_id": dto.sap_id})
        if (existed_sap_workshop is not None and existed_sap_workshop.id != existed.id):
            raise AppExceptionResponse.bad_request(message="Такое значение sap_id уже существует")
        factory = factoryRepo.get(id=dto.factory_id)
        if factory is None:
            raise AppExceptionResponse.bad_request(message="Цеха не существует")
        result = await repo.update(obj=existed, dto=dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: WorkshopRepository = Depends(WorkshopRepository),current_user=Depends(check_admin)):
        await repo.delete(id=id)