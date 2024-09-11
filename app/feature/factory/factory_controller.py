from typing import List

from fastapi import APIRouter, Depends, Path

from app.core.app_exception_response import AppExceptionResponse
from app.domain.models.factory_model import FactoryModel
from app.feature.factory.dtos.factory_dto import FactoryRDTO, FactoryCDTO
from app.feature.factory.factory_repository import FactoryRepository


class FactoryController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", )(self.all)
        self.router.post("/create", response_model=FactoryRDTO)(self.create)
        self.router.get("/get/{id}", response_model=FactoryRDTO)(self.get)
        self.router.get("/get_by_sap/{sap_id}", response_model=FactoryRDTO)(self.get_by_sap)
        self.router.put("/update/{id}", response_model=FactoryRDTO)(self.update)
        self.router.delete("/delete/{id}")(self.delete)

    async def all(self, repo: FactoryRepository = Depends(FactoryRepository)):
        result = await repo.get_all()
        return result

    async def get(self, id: int = Path(gt=0), repo: FactoryRepository = Depends(FactoryRepository)):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Завод не найден")
        return result

    async def get_by_sap(self, sap_id: int = Path(gt=0), repo: FactoryRepository = Depends(FactoryRepository)):
        result = await repo.get_filtered(filters={"sap_id": sap_id})
        if result is None:
            raise AppExceptionResponse.not_found(message="Завод не найден")
        return result

    async def create(self, dto: FactoryCDTO, repo: FactoryRepository = Depends(FactoryRepository)):
        existed = await repo.get_filtered(filters={"sap_id": dto.sap_id})
        if (existed is not None):
            raise AppExceptionResponse.bad_request(message="Завод с таким sap_id уже существует")
        factory = FactoryModel(**dto.dict())
        result = await repo.create(obj=factory)
        return result

    async def update(self, dto: FactoryCDTO, id: int = Path(gt=0),
                     repo: FactoryRepository = Depends(FactoryRepository)):
        existed = await repo.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Завод не найден")
        existed_sap_factory = await repo.get_filtered(filters={"sap_id": dto.sap_id})
        if (existed_sap_factory is not None and existed_sap_factory.id != existed.id):
            raise AppExceptionResponse.bad_request(message="Такое значение sap_id уже существует")
        result = await repo.update(obj=existed, dto=dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: FactoryRepository = Depends(FactoryRepository)):
        await repo.delete(id=id)
