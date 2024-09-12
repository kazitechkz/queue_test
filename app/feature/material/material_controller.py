from fastapi import APIRouter, Depends, Path

from app.core.app_exception_response import AppExceptionResponse
from app.domain.models.material_model import MaterialModel
from app.feature.factory.factory_repository import FactoryRepository
from app.feature.material.dtos.material_dto import MaterialRDTO, MaterialCDTO
from app.feature.material.material_repository import MaterialRepository
from app.feature.workshop.workshop_repository import WorkshopRepository


class MaterialController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", )(self.all)
        self.router.post("/create", response_model=MaterialRDTO)(self.create)
        self.router.get("/get/{id}", response_model=MaterialRDTO)(self.get)
        self.router.get("/get_by_sap/{sap_id}", response_model=MaterialRDTO)(self.get_by_sap)
        self.router.put("/update/{id}", response_model=MaterialRDTO)(self.update)
        self.router.delete("/delete/{id}")(self.delete)

    async def all(self, repo: MaterialRepository = Depends(MaterialRepository)):
        result = await repo.get_all()
        return result

    async def get(self, id: int = Path(gt=0), repo: MaterialRepository = Depends(MaterialRepository)):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Материал не найден")
        return result

    async def get_by_sap(self, sap_id: int = Path(gt=0), repo: MaterialRepository = Depends(MaterialRepository)):
        result = await repo.get_filtered(filters={"sap_id": sap_id})
        if result is None:
            raise AppExceptionResponse.not_found(message="Материал не найден")
        return result

    async def create(self, dto: MaterialCDTO, repo: MaterialRepository = Depends(MaterialRepository),workshopRepo:WorkshopRepository = Depends(WorkshopRepository)):
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
                     workshopRepo:WorkshopRepository = Depends(WorkshopRepository)
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

    async def delete(self, id: int = Path(gt=0), repo: MaterialRepository = Depends(MaterialRepository)):
        await repo.delete(id=id)