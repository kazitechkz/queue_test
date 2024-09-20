from fastapi import APIRouter, Path, Depends

from app.core.auth_core import check_individual_client, check_security, check_weigher, check_security_loader, \
    check_loader
from app.feature.initial_weight.initial_weight_repository import InitialWeightRepository
from app.feature.order.order_repository import OrderRepository
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryRDTO, ScheduleHistoryInitialWeightDTO
from app.feature.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.feature.user.dtos.user_dto import UserRDTOWithRelations
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryEnterFactoryDTO, ScheduleHistoryCDTO
from app.feature.vehicle.vehicle_repository import VehicleRepository


class ScheduleHistoryController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        #Служба безопасности КПП
        self.router.get("/process-kpp-entry-request/{schedule_id}", response_model=ScheduleHistoryRDTO)(self.process_kpp_entry_request)
        self.router.put("/confirm-or-deny-entry/{schedule_history_id}", response_model=ScheduleHistoryRDTO)(self.confirm_or_deny_entry)
        #Первичное взвешивание
        self.router.get("/accept-initial-weighing-request/{schedule_id}", response_model=ScheduleHistoryRDTO)(self.accept_initial_weighing_request)
        self.router.put("/confirm-or-deny-initial-weighing/{schedule_history_id}", response_model=ScheduleHistoryRDTO)(self.confirm_or_deny_initial_weighing)
        #Служба охраны КПП при погрузке:
        self.router.get("/process-kpp-loading-request/{schedule_id}", response_model=ScheduleHistoryRDTO)(self.process_kpp_loading_request)
        self.router.put("/confirm-or-deny-loading-entry/{schedule_history_id}", response_model=ScheduleHistoryRDTO)(self.confirm_or_deny_loading_entry)
        # Погрузка:
        self.router.get("/accept-loading-request/{schedule_id}", response_model=ScheduleHistoryRDTO)(self.accept_loading_request)
        self.router.put("/confirm-or-deny-loading/{schedule_history_id}", response_model=ScheduleHistoryRDTO)(self.confirm_or_deny_loading)

    async def process_kpp_entry_request(self,
                                            schedule_id: int = Path(gt=0),
                                            userDTO: UserRDTOWithRelations = Depends(check_security),
                                            repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
                                            scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
                                            ):
        return await repo.process_kpp_entry_request(schedule_id=schedule_id, userRDTO=userDTO,
                                                     scheduleRepo=scheduleRepo)

    async def confirm_or_deny_entry(self,
                                answer: ScheduleHistoryEnterFactoryDTO,
                                schedule_history_id:int = Path(gt=0),
                                userDTO: UserRDTOWithRelations = Depends(check_security),
                                repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
                                scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
                                orderRepo:OrderRepository = Depends(OrderRepository),
                                ):
        return await repo.confirm_or_deny_entry(
                            schedule_history_id = schedule_history_id,
                            answer=answer,
                            userRDTO=userDTO,
                            scheduleRepo=scheduleRepo,
                            orderRepo=orderRepo)

    async def accept_initial_weighing_request(self,
                                            schedule_id: int = Path(gt=0),
                                            userDTO: UserRDTOWithRelations = Depends(check_weigher),
                                            repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
                                            scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
                                            ):
        return await repo.accept_initial_weighing_request(schedule_id=schedule_id, userRDTO=userDTO,
                                                     scheduleRepo=scheduleRepo)

    async def confirm_or_deny_initial_weighing(self,
                                               dto: ScheduleHistoryInitialWeightDTO,
                                               schedule_history_id:int = Path(gt=0),
                                               userRDTO: UserRDTOWithRelations = Depends(check_weigher),
                                               repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
                                               scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
                                               initialWeightRepo: InitialWeightRepository = Depends(InitialWeightRepository),
                                               vehicleRepo: VehicleRepository = Depends(VehicleRepository),
                                               orderRepo: OrderRepository = Depends(OrderRepository)
                                               ):
        return await repo.confirm_or_deny_initial_weighing(
            dto=dto,
            schedule_history_id=schedule_history_id,
            userRDTO=userRDTO,
            scheduleRepo=scheduleRepo,
            initialWeightRepo=initialWeightRepo,
            vehicleRepo=vehicleRepo,
            orderRepo=orderRepo
        )

    async def process_kpp_loading_request(self,
                                            schedule_id: int = Path(gt=0),
                                            userDTO: UserRDTOWithRelations = Depends(check_security_loader),
                                            repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
                                            scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
                                            ):
        return await repo.process_kpp_loading_request(schedule_id=schedule_id, userRDTO=userDTO,
                                                     scheduleRepo=scheduleRepo)

    async def confirm_or_deny_loading_entry(self,
                                answer: ScheduleHistoryEnterFactoryDTO,
                                schedule_history_id:int = Path(gt=0),
                                userDTO: UserRDTOWithRelations = Depends(check_security_loader),
                                repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
                                scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
                                orderRepo:OrderRepository = Depends(OrderRepository),
                                ):
        return await repo.confirm_or_deny_loading_entry(
                            schedule_history_id = schedule_history_id,
                            answer=answer,
                            userRDTO=userDTO,
                            scheduleRepo=scheduleRepo,
                            orderRepo=orderRepo)


    async def accept_loading_request(self,
                                            schedule_id: int = Path(gt=0),
                                            userDTO: UserRDTOWithRelations = Depends(check_loader),
                                            repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
                                            scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
                                            ):
        return await repo.process_kpp_loading_request(schedule_id=schedule_id, userRDTO=userDTO,
                                                     scheduleRepo=scheduleRepo)

    async def confirm_or_deny_loading(self,
                                answer: ScheduleHistoryEnterFactoryDTO,
                                schedule_history_id:int = Path(gt=0),
                                userDTO: UserRDTOWithRelations = Depends(check_loader),
                                repo: ScheduleHistoryRepository = Depends(ScheduleHistoryRepository),
                                scheduleRepo: ScheduleRepository = Depends(ScheduleRepository),
                                orderRepo:OrderRepository = Depends(OrderRepository),
                                ):
        return await repo.confirm_or_deny_loading_entry(
                            schedule_history_id = schedule_history_id,
                            answer=answer,
                            userRDTO=userDTO,
                            scheduleRepo=scheduleRepo,
                            orderRepo=orderRepo)