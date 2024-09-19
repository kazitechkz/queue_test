import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy import between

from app.core.app_exception_response import AppExceptionResponse
from app.domain.models.workshop_schedule_model import WorkshopScheduleModel
from app.feature.workshop.workshop_repository import WorkshopRepository
from app.feature.workshop_schedule.dtos.workshop_schedule_dto import WorkshopScheduleRDTO, WorkshopScheduleCDTO
from app.feature.workshop_schedule.workshop_schedule_repository import WorkshopScheduleRepository


class WorkshopScheduleController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", response_model=List[WorkshopScheduleRDTO])(self.get_all)
        self.router.post("/create", response_model=WorkshopScheduleRDTO)(self.create)
        self.router.get("/get_by_id/{id}", response_model=WorkshopScheduleRDTO)(self.get_by_id)
        self.router.get("/get_active", response_model=Optional[WorkshopScheduleRDTO])(self.get_active)
        self.router.get("/get_schedule")(self.get_schedule)
        self.router.put("/update/{id}", response_model=WorkshopScheduleRDTO)(self.update)
        self.router.delete("/delete/{id}")(self.delete)

    async def get_all(self, repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository)):
        result = await repo.get_all()
        return result

    async def get_by_id(self, id: int = Path(gt=0), repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository)):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Расписание цеха не найдена")
        return result

    async def get_active(self,
                         workshop_sap_id: str = Query(max_length=255,
                                                      description="Уникальный идентификатор цеха в SAP"),
                         schedule_date: Optional[datetime.date] = Query(datetime.date.today(), description="Дата для фильтрации",
                                                               ge=datetime.date.today()),
                         repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository)):
        result = await repo.get_active(workshop_sap_id=workshop_sap_id,schedule_date=schedule_date)
        return result

    async def get_schedule(self,
                           workshop_sap_id:str = Query(max_length=255, description="Уникальный идентификатор цеха в SAP"),
                           schedule_date: Optional[datetime.date] = Query(datetime.date.today(), description="Дата для фильтрации",ge=datetime.date.today()),
                           repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository)):
        result = await repo.get_schedule(workshop_sap_id=workshop_sap_id,schedule_date=schedule_date)
        return result

    async def create(self,
                     dto:WorkshopScheduleCDTO,
                     repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository),
                     workshopRepo:WorkshopRepository = Depends(WorkshopRepository)):
        await self.check_form(dto=dto,repo=repo,workshopRepo=workshopRepo)
        result = await repo.create(obj=WorkshopScheduleModel(**dto.dict()))
        return result

    async def update(self,
                     dto: WorkshopScheduleCDTO,
                     id:int = Path(gt=0),
                     repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository),
                     workshopRepo:WorkshopRepository = Depends(WorkshopRepository)):
        existed = await self.check_form(dto=dto,repo=repo,workshopRepo=workshopRepo,id=id)
        result = await repo.update(obj=existed,dto=dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository)):
        await repo.delete(id=id)


    @staticmethod
    async def check_form(
                dto: WorkshopScheduleCDTO,
                repo: WorkshopScheduleRepository,
                workshopRepo: WorkshopRepository,
                id: Optional[int] = None):
        if id is not None:
            existed = await repo.get(id=id)
            if existed is None:
                    raise AppExceptionResponse.bad_request(message="Расписание цеха не найдено")
        workshop = await workshopRepo.get(id=dto.workshop_id)
        if workshop is None:
            raise AppExceptionResponse.bad_request(message="Цех не найден")
        if workshop.sap_id != dto.workshop_sap_id:
            raise AppExceptionResponse.bad_request(message="Цех не найден")

        if id is not None:
            return existed



