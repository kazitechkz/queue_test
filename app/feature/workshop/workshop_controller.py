from fastapi import APIRouter, Depends, Path

from app.core.app_exception_response import AppExceptionResponse
from app.domain.models.workshop_model import WorkshopModel
from app.feature.factory.factory_repository import FactoryRepository
from app.feature.workshop.dtos.workshop_dto import WorkshopRDTO, WorkshopCDTO
from app.feature.workshop.workshop_repository import WorkshopRepository


class WorkshopController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", )(self.all)
        self.router.post("/create", response_model=WorkshopRDTO)(self.create)
        self.router.get("/get/{id}", response_model=WorkshopRDTO)(self.get)
        self.router.get("/get_by_sap/{sap_id}", response_model=WorkshopRDTO)(self.get_by_sap)
        self.router.put("/update/{id}", response_model=WorkshopRDTO)(self.update)
        self.router.delete("/delete/{id}")(self.delete)

    async def all(self, repo: WorkshopRepository = Depends(WorkshopRepository)):
        result = await repo.get_all()
        return result

    async def get(self, id: int = Path(gt=0), repo: WorkshopRepository = Depends(WorkshopRepository)):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Цех не найден")
        return result

    async def get_by_sap(self, sap_id: int = Path(gt=0), repo: WorkshopRepository = Depends(WorkshopRepository)):
        result = await repo.get_filtered(filters={"sap_id": sap_id})
        if result is None:
            raise AppExceptionResponse.not_found(message="Завод не найден")
        return result

    async def create(self, dto: WorkshopCDTO, repo: WorkshopRepository = Depends(WorkshopRepository),factoryRepo:FactoryRepository = Depends(FactoryRepository)):
        existed = await repo.get_filtered(filters={"sap_id": dto.sap_id})
        if (existed is not None):
            raise AppExceptionResponse.bad_request(message="Цех с таким sap_id уже существует")
        factory = factoryRepo.get(id=dto.factory_id)
        if factory is None:
            raise AppExceptionResponse.bad_request(message="Завода не существует")
        workshop = WorkshopModel(**dto.dict())
        result = await repo.create(obj=workshop)
        return result

    async def update(self, dto: WorkshopCDTO, id: int = Path(gt=0),
                     repo: WorkshopRepository = Depends(WorkshopRepository),
                     factoryRepo: FactoryRepository = Depends(FactoryRepository)
                     ):
        existed = await repo.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Цех не найден")
        existed_sap_workshop = await repo.get_filtered(filters={"sap_id": dto.sap_id})
        if (existed_sap_workshop is not None and existed_sap_workshop.id != existed.id):
            raise AppExceptionResponse.bad_request(message="Такое значение sap_id уже существует")
        factory = factoryRepo.get(id=dto.factory_id)
        if factory is None:
            raise AppExceptionResponse.bad_request(message="Завода не существует")
        result = await repo.update(obj=existed, dto=dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: WorkshopRepository = Depends(WorkshopRepository)):
        await repo.delete(id=id)