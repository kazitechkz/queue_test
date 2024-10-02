from datetime import date, time
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_

from app.core.auth_core import check_individual_client, check_legal_client, check_employee, check_client
from app.feature.operation.operation_repository import OperationRepository
from app.feature.order.order_repository import OrderRepository
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.organization_employee.organization_employee_repository import OrganizationEmployeeRepository
from app.feature.schedule.dtos.schedule_dto import ScheduleRDTO, ScheduleIndividualCDTO, ScheduleLegalCDTO
from app.feature.schedule.filter.schedule_filter import ScheduleFilter, ScheduleClientScheduledFilter, \
    ScheduleClientFromToFilter
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.user.user_repository import UserRepository
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.feature.workshop_schedule.workshop_schedule_repository import WorkshopScheduleRepository
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class ScheduleController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/create-individual", response_model=ScheduleRDTO)(self.create_individual)
        self.router.post("/create-legal", response_model=ScheduleRDTO)(self.create_legal)
        self.router.get("/get-schedule")(self.get_schedule)
        self.router.get("/get-active-schedules")(self.get_active_schedules)
        self.router.get("/get-canceled-schedules")(self.get_canceled_schedules)
        self.router.get("/get-all-schedules")(self.get_all_schedules)
        self.router.get("/my-active-schedules")(self.my_active_schedules)
        self.router.get("/my-schedules")(self.my_schedules)
        self.router.get("/my-schedules-count")(self.my_schedules_count)

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
                           schedule_date: Optional[date] = Query(date.today(), description="Дата для фильтрации",ge=date.today()),
                           repo: ScheduleRepository = Depends(ScheduleRepository),
                           workshopScheduleRepo: WorkshopScheduleRepository = Depends(WorkshopScheduleRepository),
                           ):
        result = await repo.get_schedule(workshop_sap_id=workshop_sap_id,schedule_date=schedule_date,workshopScheduleRepo=workshopScheduleRepo)
        return result

    async def get_active_schedules(self,
                                 userDTO: UserRDTOWithRelations = Depends(check_employee),
                                 repo: ScheduleRepository = Depends(ScheduleRepository),
                                 operationRepo: OperationRepository = Depends(OperationRepository)
                                 ):
        return await repo.get_active_schedules(userDTO=userDTO, operationRepo=operationRepo)


    async def get_canceled_schedules(self,
                                 userDTO: UserRDTOWithRelations = Depends(check_employee),
                                 repo: ScheduleRepository = Depends(ScheduleRepository),
                                 operationRepo: OperationRepository = Depends(OperationRepository)
                                 ):
        return await repo.get_canceled_schedules(userDTO=userDTO, operationRepo=operationRepo)

    async def get_all_schedules(self,
                                 params: ScheduleFilter = Depends(),
                                 userDTO: UserRDTOWithRelations = Depends(check_employee),
                                 repo: ScheduleRepository = Depends(ScheduleRepository),
                                 ):
        return await repo.paginate_with_filter(
            dto=ScheduleRDTO, page=params.page, per_page=params.per_page,
            filters=params.apply()
        )

    async def my_active_schedules(self,
                                 userDTO: UserRDTOWithRelations = Depends(check_employee),
                                 repo: ScheduleRepository = Depends(ScheduleRepository),
                           ):

        return await repo.get_all_with_filter(filters=[
            and_(repo.model.is_active == True,repo.model.responsible_id == userDTO.id)
        ])

    async def my_schedules(
            self,
            params: ScheduleClientScheduledFilter = Depends(),
            userDTO: UserRDTOWithRelations = Depends(check_client),
            repo: ScheduleRepository = Depends(ScheduleRepository),
            orderRepo: OrderRepository = Depends(OrderRepository)
    ):
        if params.order_id:
            order = await orderRepo.get(id=params.order_id)
        return await repo.get_all_with_filter(filters=params.apply(userRDTO=userDTO))

    async def my_schedules_count(
            self,
            params: ScheduleClientFromToFilter = Depends(),
            userDTO: UserRDTOWithRelations = Depends(check_client),
            repo: ScheduleRepository = Depends(ScheduleRepository),
            orderRepo:OrderRepository = Depends(OrderRepository)
    ):
        return await repo.my_schedules_count( userDTO = userDTO,
                                 filter = params,
                                 date_filters = params.apply(),
                                 orderRepo = orderRepo)