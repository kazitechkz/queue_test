from fastapi import APIRouter, Depends, Path

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_admin, get_current_user
from app.domain.models.workshop_schedule_model import WorkshopScheduleModel
from app.feature.workshop.workshop_repository import WorkshopRepository
from app.feature.workshop_schedule.dtos.workshop_schedule_dto import (
    WorkshopScheduleCDTO,
    WorkshopScheduleRDTO,
)
from app.feature.workshop_schedule.workshop_schedule_repository import (
    WorkshopScheduleRepository,
)


class WorkshopScheduleController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=list[WorkshopScheduleRDTO],
            summary="Получение расписания цеха",
            description="Получение всех расписаний цеха",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=WorkshopScheduleRDTO,
            summary="Создание расписания цеха",
            description="Создание нового расписания цеха",
        )(self.create)
        self.router.get(
            "/get-by-id/{id}",
            response_model=WorkshopScheduleRDTO,
            summary="Получение расписания цеха по идентификатору",
            description="Получение расписания цеха по уникальному идентификатору",
        )(self.get_by_id)
        self.router.put(
            "/update/{id}",
            response_model=WorkshopScheduleRDTO,
            summary="Обновление расписания цеха по уникальному идентификатору",
            description="Обновление расписания цеха по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            summary="Удаление расписания цеха по уникальному идентификатору",
            description="Удаление расписания цеха по уникальному идентификатору",
        )(self.delete)

    async def get_all(
        self,
        repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository),
        current_user=Depends(get_current_user),
    ):
        result = await repo.get_all()
        return result

    async def get_by_id(
        self,
        id: int = Path(gt=0),
        repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository),
        current_user=Depends(get_current_user),
    ):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Расписание цеха не найдена")
        return result

    async def create(
        self,
        dto: WorkshopScheduleCDTO,
        repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository),
        workshopRepo: WorkshopRepository = Depends(WorkshopRepository),
        current_user=Depends(check_admin),
    ):
        await self.check_form(dto=dto, repo=repo, workshopRepo=workshopRepo)
        result = await repo.create(obj=WorkshopScheduleModel(**dto.dict()))
        return result

    async def update(
        self,
        dto: WorkshopScheduleCDTO,
        id: int = Path(gt=0),
        repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository),
        workshopRepo: WorkshopRepository = Depends(WorkshopRepository),
        current_user=Depends(check_admin),
    ):
        existed = await self.check_form(
            dto=dto, repo=repo, workshopRepo=workshopRepo, id=id
        )
        result = await repo.update(obj=existed, dto=dto)
        return result

    async def delete(
        self,
        id: int = Path(gt=0),
        repo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository),
        current_user=Depends(check_admin),
    ) -> None:
        await repo.delete(id=id)

    @staticmethod
    async def check_form(
        dto: WorkshopScheduleCDTO,
        repo: WorkshopScheduleRepository,
        workshopRepo: WorkshopRepository,
        id: int | None = None,
    ):
        if id is not None:
            existed = await repo.get(id=id)
            if existed is None:
                raise AppExceptionResponse.bad_request(
                    message="Расписание цеха не найдено"
                )
        workshop = await workshopRepo.get(id=dto.workshop_id)
        if workshop is None:
            raise AppExceptionResponse.bad_request(message="Цех не найден")
        if workshop.sap_id != dto.workshop_sap_id:
            raise AppExceptionResponse.bad_request(message="Цех не найден")

        if id is not None:
            return existed
        return None
