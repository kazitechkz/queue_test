from fastapi import APIRouter, Path, Depends

from app.core.auth_core import check_employee
from app.feature.act_weight.act_weight_repository import ActWeightRepository
from app.feature.initial_weight.initial_weight_repository import InitialWeightRepository
from app.feature.operation.operation_repository import OperationRepository
from app.feature.order.order_repository import OrderRepository
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryAnswerDTO
from app.feature.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class ScheduleHistoryController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get(
            "/take-request/{schedule_id}",
            summary="Взять заявку в обработку",
            description="Взять заявку на текущее расписание",
        )(self.take_request)
        self.router.put(
            "/make-decision/{schedule_id}",
            summary="Принять или отказать заявку",
            description="Принять или отказать заявку на текущее расписание",
        )(self.accept_or_cancel)

    async def take_request(
            self,
            schedule_id: int = Path(description="ID расписания", gt=0),
            userRDTO: UserRDTOWithRelations = Depends(check_employee),
            repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
            scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
            operationRepo: OperationRepository = Depends(OperationRepository),
    ):
        return await repo.take_request(schedule_id=schedule_id, userRDTO=userRDTO, scheduleRepo=scheduleRepo,
                                       operationRepo=operationRepo)

    async def accept_or_cancel(
            self,
            dto: ScheduleHistoryAnswerDTO,
            schedule_id: int = Path(description="ID расписания", gt=0),
            userRDTO: UserRDTOWithRelations = Depends(check_employee),
            repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
            scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
            initialWeightRepo: InitialWeightRepository = Depends(InitialWeightRepository),
            actWeightRepo: ActWeightRepository = Depends(ActWeightRepository),
            orderRepo: OrderRepository = Depends(OrderRepository),
            operationRepo: OperationRepository = Depends(OperationRepository),
    ):
        return await repo.accept_or_cancel(schedule_id=schedule_id, dto=dto, userRDTO=userRDTO,
                                           scheduleRepo=scheduleRepo, initialWeightRepo=initialWeightRepo,
                                           actWeightRepo=actWeightRepo, orderRepo=orderRepo,
                                           operationRepo=operationRepo)
