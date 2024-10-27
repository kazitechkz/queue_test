from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_current_user, check_admin
from app.domain.models.material_model import MaterialModel
from app.feature.material.dtos.material_dto import MaterialRDTO, MaterialCDTO, MaterialWithRelationsDTO
from app.feature.material.material_repository import MaterialRepository
from app.feature.workshop.workshop_repository import WorkshopRepository


class MaterialController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get(
            "/",
            response_model=List[MaterialWithRelationsDTO],
            summary="Список материалов",
            description="Получение списка материалов"
        )(self.all)
        self.router.post(
            "/create",
            response_model=MaterialRDTO,
            summary="Создать материал",
            description="Создание материала"
        )(self.create)
        self.router.get(
            "/get/{id}",
            response_model=MaterialWithRelationsDTO,
            summary="Получить материал по идентификатору",
            description="Получение материала по идентификатору"
        )(self.get)
        self.router.get(
            "/get-by-sap/{sap_id}",
            response_model=MaterialWithRelationsDTO,
            summary="Получить материал по идентификатору в системе SAP",
            description="Получение материала по идентификатору в системе SAP"
        )(self.get_by_sap)
        self.router.put(
            "/update/{id}",
            response_model=MaterialRDTO,
            summary="Обновить материал по идентификатору",
            description="Обновление материала по идентификатору"
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            summary="Удалить материал по идентификатору",
            description="Удаление материала по идентификатору"
        )(self.delete)

    async def all(
            self,
            repo: MaterialRepository = Depends(MaterialRepository),
            current_user = Depends(get_current_user)
    ):
        result = await repo.get_all_with_filter(options=[
            selectinload(repo.model.workshop)
        ])
        result_dto = [MaterialWithRelationsDTO.from_orm(resultItem) for resultItem in result]
        return result_dto

    async def get(
            self,
            id: int = Path(gt=0),
            repo: MaterialRepository = Depends(MaterialRepository),
            current_user=Depends(get_current_user)
    ):
        result = await repo.get(id=id,options=[selectinload(repo.model.workshop)])
        if result is None:
            raise AppExceptionResponse.not_found(message="Материал не найден")
        result_dto = MaterialWithRelationsDTO.from_orm(result)
        return result_dto

    async def get_by_sap(
            self,
            sap_id: int = Path(gt=0),
            repo: MaterialRepository = Depends(MaterialRepository),
            current_user=Depends(get_current_user)
    ):
        result = await repo.get_filtered(filters={"sap_id": sap_id},options=[selectinload(repo.model.workshop)])
        if result is None:
            raise AppExceptionResponse.not_found(message="Материал не найден")
        result_dto = MaterialWithRelationsDTO.from_orm(result)
        return result_dto

    async def create(
            self,
            dto: MaterialCDTO,
            repo: MaterialRepository = Depends(MaterialRepository),
            workshopRepo:WorkshopRepository = Depends(WorkshopRepository),
            current_user=Depends(check_admin)
    ):
        existed = await repo.get_filtered(filters={"sap_id": dto.sap_id})
        if (existed is not None):
            raise AppExceptionResponse.bad_request(message="Материал с таким sap_id уже существует")
        workshop = workshopRepo.get(id=dto.workshop_id)
        if workshop is None:
            raise AppExceptionResponse.bad_request(message="Цеха не существует")
        material = MaterialModel(**dto.dict())
        result = await repo.create(obj=material)
        return result

    async def update(self, dto: MaterialCDTO, id: int = Path(gt=0),
                     repo: MaterialRepository = Depends(MaterialRepository),
                     workshopRepo:WorkshopRepository = Depends(WorkshopRepository),
                     current_user=Depends(check_admin)
                     ):
        existed = await repo.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Цех не найден")
        existed_sap_Material = await repo.get_filtered(filters={"sap_id": dto.sap_id})
        if (existed_sap_Material is not None and existed_sap_Material.id != existed.id):
            raise AppExceptionResponse.bad_request(message="Такое значение sap_id уже существует")
        workshop = workshopRepo.get(id=dto.workshop_id)
        if workshop is None:
            raise AppExceptionResponse.bad_request(message="Цеха не существует")
        result = await repo.update(obj=existed, dto=dto)
        return result

    async def delete(
            self,
            id: int = Path(gt=0),
            repo: MaterialRepository = Depends(MaterialRepository),
            current_user=Depends(check_admin)
    ):
        await repo.delete(id=id)