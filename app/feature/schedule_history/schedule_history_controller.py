from fastapi import APIRouter, Path, Depends

from app.core.auth_core import check_individual_client, check_security
from app.feature.order.order_repository import OrderRepository
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryRDTO
from app.feature.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.feature.user.dtos.user_dto import UserRDTOWithRelations
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryEnterFactoryDTO, ScheduleHistoryCDTO

class ScheduleHistoryController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/take-request-to-enter-factory/{schedule_id}", response_model=ScheduleHistoryRDTO)(self.take_request_to_enter_factory)
        self.router.put("/enter-factory-pass-request/{schedule_history_id}", response_model=ScheduleHistoryRDTO)(self.enter_factory_pass_request)

    async def enter_factory_pass_request(self,
                                answer: ScheduleHistoryEnterFactoryDTO,
                                schedule_history_id:int = Path(gt=0),
                                userDTO: UserRDTOWithRelations = Depends(check_security),
                                repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
                                scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
                                orderRepo:OrderRepository = Depends(OrderRepository),
                                ):
        return await repo.enter_factory_pass_request(
                            schedule_history_id = schedule_history_id,
                            answer=answer,
                            userRDTO=userDTO,
                            scheduleRepo=scheduleRepo,
                            orderRepo=orderRepo)

    async def take_request_to_enter_factory(self,
                                            schedule_id: int = Path(gt=0),
                                            userDTO: UserRDTOWithRelations = Depends(check_security),
                                            repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
                                            scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
                                            ):
        return await repo.enter_factory_take_request(schedule_id=schedule_id, userRDTO=userDTO,
                                                     scheduleRepo=scheduleRepo)