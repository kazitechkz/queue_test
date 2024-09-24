import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.auth_core import check_individual_client, check_legal_client
from app.feature.order.order_repository import OrderRepository
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.organization_employee.organization_employee_repository import OrganizationEmployeeRepository
from app.feature.schedule.dtos.schedule_dto import ScheduleRDTO, ScheduleIndividualCDTO, ScheduleLegalCDTO
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.user.dtos.user_dto import UserRDTOWithRelations
from app.feature.user.user_repository import UserRepository
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.feature.workshop_schedule.workshop_schedule_repository import WorkshopScheduleRepository


class ScheduleController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/create-individual", response_model=ScheduleRDTO)(self.create_individual)
        self.router.post("/create-legal", response_model=ScheduleRDTO)(self.create_legal)
        self.router.get("/get_schedule")(self.get_schedule)

    async def create_individual(self,
                                dto: ScheduleIndividualCDTO,
                                userDTO: UserRDTOWithRelations = Depends(check_individual_client),
                                repo: ScheduleRepository = Depends(ScheduleRepository),
                                orderRepo: OrderRepository = Depends(OrderRepository),
                                vehicleRepo: VehicleRepository = Depends(VehicleRepository),
                                workshopScheduleRepo:WorkshopScheduleRepository = Depends(WorkshopScheduleRepository)
                                ):
        return await repo.create_individual_schedule(dto=dto,userDTO=userDTO,orderRepo=orderRepo,vehicleRepo=vehicleRepo,workshopScheduleRepo= workshopScheduleRepo)

    async def create_legal(self,
                           dto: ScheduleLegalCDTO,
                           userDTO: UserRDTOWithRelations = Depends(check_legal_client),
                           repo: ScheduleRepository = Depends(ScheduleRepository),
                           orderRepo: OrderRepository = Depends(OrderRepository),
                           userRepo: UserRepository = Depends(UserRepository),
                           vehicleRepo: VehicleRepository = Depends(VehicleRepository),
                           workshopScheduleRepo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository),
                           organizationRepo: OrganizationRepository = Depends(OrganizationRepository),
                           organizationEmployeeRepo: OrganizationEmployeeRepository = Depends(OrganizationEmployeeRepository),
                                ):
        return await repo.create_legal_schedule(
                    dto = dto,
                    userDTO=userDTO,
                    orderRepo=orderRepo,
                    userRepo=userRepo,
                    vehicleRepo=vehicleRepo,
                    workshopScheduleRepo = workshopScheduleRepo,
                    organizationRepo=organizationRepo,
                    organizationEmployeeRepo=organizationEmployeeRepo
        )

    async def get_schedule(self,
                           workshop_sap_id:str = Query(max_length=255, description="Уникальный идентификатор цеха в SAP"),
                           schedule_date: Optional[datetime.date] = Query(datetime.date.today(), description="Дата для фильтрации",ge=datetime.date.today()),
                           repo: ScheduleRepository = Depends(ScheduleRepository),
                           workshopScheduleRepo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository),
                           ):
        result = await repo.get_schedule(workshop_sap_id=workshop_sap_id,schedule_date=schedule_date,workshopScheduleRepo=workshopScheduleRepo)
        return result