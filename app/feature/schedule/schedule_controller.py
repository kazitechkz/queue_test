from fastapi import APIRouter, Depends

from app.core.auth_core import check_individual_client
from app.feature.order.order_repository import OrderRepository
from app.feature.schedule.dtos.schedule_dto import ScheduleRDTO, ScheduleIndividualCDTO
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.user.dtos.user_dto import UserRDTOWithRelations
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.feature.workshop_schedule.workshop_schedule_repository import WorkshopScheduleRepository


class ScheduleController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/create-individual", response_model=ScheduleRDTO)(self.create_individual)

    async def create_individual(self,
                                dto: ScheduleIndividualCDTO,
                                userDTO: UserRDTOWithRelations = Depends(check_individual_client),
                                repo: ScheduleRepository = Depends(ScheduleRepository),
                                orderRepo: OrderRepository = Depends(OrderRepository),
                                vehicleRepo: VehicleRepository = Depends(VehicleRepository),
                                workshopScheduleRepo:WorkshopScheduleRepository = Depends(WorkshopScheduleRepository)
                                ):
        return await repo.create_individual_schedule(dto=dto,userDTO=userDTO,orderRepo=orderRepo,vehicleRepo=vehicleRepo,workshopScheduleRepo= workshopScheduleRepo)