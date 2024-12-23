from datetime import date

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy import and_
from sqlalchemy.orm import joinedload, selectinload

from app.core.auth_core import (
    check_admin,
    check_admin_and_client,
    check_client,
    check_employee,
    check_individual_client,
    check_legal_client,
    get_current_user,
)
from app.core.pagination_dto import PaginationScheduleRDTOWithRelations
from app.domain.models.schedule_history_model import ScheduleHistoryModel
from app.feature.operation.operation_repository import OperationRepository
from app.feature.order.order_repository import OrderRepository
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.organization_employee.organization_employee_repository import (
    OrganizationEmployeeRepository,
)
from app.feature.schedule.dtos.schedule_dto import (
    RescheduleAllDTO,
    RescheduleOneDTO,
    ScheduleCalendarDTO,
    ScheduleCancelDTO,
    ScheduleCancelOneDTO,
    ScheduleIndividualCDTO,
    ScheduleLegalCDTO,
    ScheduleRDTO,
    ScheduleRDTOWithRelation,
)
from app.feature.schedule.filter.schedule_filter import (
    ScheduleClientFromToFilter,
    ScheduleClientScheduledFilter,
    ScheduleFilter,
)
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.user.user_repository import UserRepository
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.feature.workshop_schedule.workshop_schedule_repository import (
    WorkshopScheduleRepository,
)
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class ScheduleController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.post(
            "/create-individual",
            summary="Создание брони для физического лица",
            description="Создание брони для физического лица",
        )(self.create_individual)
        self.router.post(
            "/create-legal",
            summary="Создание брони для юридического лица",
            description="Создание брони для юридического лица",
        )(self.create_legal)
        self.router.get(
            "/get-schedule",
            summary="Получение свободного времени для бронирования",
            description="Получение свободного времени для бронирования",
        )(self.get_schedule)
        self.router.get(
            "/get/{id}",
            summary="Получение детальной информации о брони",
            description="Получение детальной информации о брони с уникальным идентификатором",
        )(self.get)
        self.router.get(
            "/get-active-schedules",
            response_model=list[ScheduleRDTOWithRelation],
            summary="Получение всех активных броней",
            description="Получение всех активных броней",
        )(self.get_active_schedules)
        self.router.get(
            "/get-canceled-schedules",
            summary="Получение всех отмененных броней",
            description="Получение всех отмененных броней",
        )(self.get_canceled_schedules)
        self.router.get(
            "/get-all-schedules",
            response_model=PaginationScheduleRDTOWithRelations,
            summary="Получение всех броней с пагинацией",
            description="Получение всех броней с пагинацией",
        )(self.get_all_schedules)
        self.router.get(
            "/my-active-schedules",
            summary="Получение всех активных броней текущего сотрудника",
            description="Получение всех активных броней текущего сотрудника",
        )(self.my_active_schedules)
        self.router.get(
            "/my-responsible-schedules",
            summary="Получение всех броней текущего сотрудника, которые являются ответственными и должны дать ответ",
            description="Получение всех броней текущего сотрудника, которые являются ответственными и должны дать ответ",
        )(self.my_responsible_schedules)
        self.router.get(
            "/my-schedules",
            summary="Получение всех броней текущего клиента по дню",
            description="Получение всех броней текущего клиента по дню",
        )(self.my_schedules)
        self.router.get(
            "/my-schedules-count",
            response_model=list[ScheduleCalendarDTO],
            summary="Получение количества броней текущего клиента по дням",
            description="Получение количества броней текущего клиента по дням",
        )(self.my_schedules_count)
        self.router.post(
            "/reschedules-all",
            summary="Перенос всех бронирований на другую дату",
            description="Перенос всех бронирований на другую дату",
        )(self.reschedules_all)
        self.router.post(
            "/cancel-all-schedules",
            summary="Отмена всех бронирований",
            description="Отмена всех бронирований",
        )(self.cancel_all_schedules)
        self.router.put(
            "/reschedule-to-date/{schedule_id}",
            summary="Перенос одного бронирования на другую дату",
            description="Перенос одного бронирования на другую дату",
        )(self.reschedule_to_date)
        self.router.put(
            "/cancel-one/{schedule_id}",
            summary="Отмена одного бронирования",
            description="Отмена одного бронирования",
        )(self.cancel_one)
        self.router.get(
            "/check-late-schedules",
            summary="Проверка наличия просроченных бронирований",
            description="Проверка наличия просроченных бронирований",
        )(self.check_late_schedules)

    async def create_individual(
        self,
        dto: ScheduleIndividualCDTO,
        userDTO: UserRDTOWithRelations = Depends(check_individual_client),
        repo: ScheduleRepository = Depends(ScheduleRepository),
        orderRepo: OrderRepository = Depends(OrderRepository),
        vehicleRepo: VehicleRepository = Depends(VehicleRepository),
        workshopScheduleRepo: WorkshopScheduleRepository = Depends(
            WorkshopScheduleRepository
        ),
    ):
        return await repo.create_individual_schedule(
            dto=dto,
            userDTO=userDTO,
            orderRepo=orderRepo,
            vehicleRepo=vehicleRepo,
            workshopScheduleRepo=workshopScheduleRepo,
        )

    async def create_legal(
        self,
        dto: ScheduleLegalCDTO,
        userDTO: UserRDTOWithRelations = Depends(check_legal_client),
        repo: ScheduleRepository = Depends(ScheduleRepository),
        orderRepo: OrderRepository = Depends(OrderRepository),
        userRepo: UserRepository = Depends(UserRepository),
        vehicleRepo: VehicleRepository = Depends(VehicleRepository),
        workshopScheduleRepo: WorkshopScheduleRepository = Depends(
            WorkshopScheduleRepository
        ),
        organizationRepo: OrganizationRepository = Depends(OrganizationRepository),
        organizationEmployeeRepo: OrganizationEmployeeRepository = Depends(
            OrganizationEmployeeRepository
        ),
    ):
        return await repo.create_legal_schedule(
            dto=dto,
            userDTO=userDTO,
            orderRepo=orderRepo,
            userRepo=userRepo,
            vehicleRepo=vehicleRepo,
            workshopScheduleRepo=workshopScheduleRepo,
            organizationRepo=organizationRepo,
            organizationEmployeeRepo=organizationEmployeeRepo,
        )

    async def get_schedule(
        self,
        workshop_sap_id: str = Query(
            max_length=255, description="Уникальный идентификатор цеха в SAP"
        ),
        schedule_date: date | None = Query(
            date.today(), description="Дата для фильтрации", ge=date.today()
        ),
        repo: ScheduleRepository = Depends(ScheduleRepository),
        workshopScheduleRepo: WorkshopScheduleRepository = Depends(
            WorkshopScheduleRepository
        ),
        userDTO: UserRDTOWithRelations = Depends(get_current_user),
    ):
        result = await repo.get_schedule(
            workshop_sap_id=workshop_sap_id,
            schedule_date=schedule_date,
            workshopScheduleRepo=workshopScheduleRepo,
        )
        return result

    async def check_late_schedules(
        self,
        repo: ScheduleRepository = Depends(ScheduleRepository),
        orderRepo: OrderRepository = Depends(OrderRepository),
    ):
        return await repo.check_late_schedules(orderRepo=orderRepo)

    async def get(
        self,
        id: int = Path(gt=0, description="Уникальный идентфикатор"),
        repo: ScheduleRepository = Depends(ScheduleRepository),
        userDTO: UserRDTOWithRelations = Depends(get_current_user),
    ):
        schedule = await repo.get(
            id=id,
            options=[
                selectinload(repo.model.order),
                selectinload(repo.model.driver),
                selectinload(repo.model.vehicle),
                selectinload(repo.model.trailer),
                # Подгружаем schedule_histories и вложенные связи через полный путь
                selectinload(
                    repo.model.schedule_histories
                ).selectinload(  # Загружаем schedule_histories
                    ScheduleHistoryModel.operation
                ),
                # Загружаем operation для schedule_histories
                selectinload(
                    repo.model.schedule_histories
                ).selectinload(  # Подгружаем снова schedule_histories для act_weights
                    ScheduleHistoryModel.act_weights
                ),
                selectinload(
                    repo.model.schedule_histories
                ).selectinload(  # Подгружаем снова schedule_histories для initial_weights
                    ScheduleHistoryModel.initial_weights
                ),
            ],
        )
        return schedule

    async def get_active_schedules(
        self,
        userDTO: UserRDTOWithRelations = Depends(check_employee),
        repo: ScheduleRepository = Depends(ScheduleRepository),
        operationRepo: OperationRepository = Depends(OperationRepository),
    ):
        return await repo.get_active_schedules(
            userDTO=userDTO, operationRepo=operationRepo
        )

    async def get_canceled_schedules(
        self,
        userDTO: UserRDTOWithRelations = Depends(check_employee),
        repo: ScheduleRepository = Depends(ScheduleRepository),
        operationRepo: OperationRepository = Depends(OperationRepository),
    ):
        return await repo.get_canceled_schedules(
            userDTO=userDTO, operationRepo=operationRepo
        )

    async def get_all_schedules(
        self,
        params: ScheduleFilter = Depends(),
        userDTO: UserRDTOWithRelations = Depends(check_employee),
        repo: ScheduleRepository = Depends(ScheduleRepository),
    ):
        return await repo.paginate_with_filter(
            dto=ScheduleRDTO,
            page=params.page,
            per_page=params.per_page,
            filters=params.apply(),
            options=[joinedload(repo.model.current_operation)],
        )

    async def my_active_schedules(
        self,
        userDTO: UserRDTOWithRelations = Depends(check_employee),
        repo: ScheduleRepository = Depends(ScheduleRepository),
    ):
        return await repo.get_all_with_filter(
            filters=[
                and_(
                    repo.model.is_active is True, repo.model.responsible_id == userDTO.id
                )
            ]
        )

    async def my_responsible_schedules(
        self,
        userDTO: UserRDTOWithRelations = Depends(check_employee),
        repo: ScheduleRepository = Depends(ScheduleRepository),
    ):
        return await repo.get_all_with_filter(
            filters=[
                and_(
                    repo.model.is_active is True, repo.model.responsible_id == userDTO.id
                )
            ],
            options=[selectinload(repo.model.current_operation)],
        )

    async def my_schedules(
        self,
        params: ScheduleClientScheduledFilter = Depends(),
        userDTO: UserRDTOWithRelations = Depends(check_client),
        repo: ScheduleRepository = Depends(ScheduleRepository),
        orderRepo: OrderRepository = Depends(OrderRepository),
    ):
        if params.order_id:
            await orderRepo.get(id=params.order_id)
        return await repo.get_all_with_filter(
            filters=params.apply(userRDTO=userDTO),
            options=[selectinload(repo.model.current_operation)],
        )

    async def my_schedules_count(
        self,
        params: ScheduleClientFromToFilter = Depends(),
        userDTO: UserRDTOWithRelations = Depends(check_client),
        repo: ScheduleRepository = Depends(ScheduleRepository),
        orderRepo: OrderRepository = Depends(OrderRepository),
    ):
        return await repo.my_schedules_count(
            userDTO=userDTO,
            filter=params,
            date_filters=params.apply(),
            orderRepo=orderRepo,
        )

    async def reschedules_all(
        self,
        dto: RescheduleAllDTO,
        repo: ScheduleRepository = Depends(ScheduleRepository),
    ):
        return await repo.reshedule_data(dto=dto)

    async def cancel_all_schedules(
        self,
        dto: ScheduleCancelDTO,
        userDTO: UserRDTOWithRelations = Depends(check_admin),
        repo: ScheduleRepository = Depends(ScheduleRepository),
        orderRepo: OrderRepository = Depends(OrderRepository),
    ):
        return await repo.cancel_all_schedules(
            dto=dto, orderRepo=orderRepo, userDTO=userDTO
        )

    async def reschedule_to_date(
        self,
        dto: RescheduleOneDTO,
        userDTO: UserRDTOWithRelations = Depends(check_admin),
        schedule_id: int = Path(description="Идентификатор заказа"),
        repo: ScheduleRepository = Depends(ScheduleRepository),
    ):
        return await repo.reschedule_to_date(schedule_id=schedule_id, dto=dto)

    async def cancel_one(
        self,
        dto: ScheduleCancelOneDTO,
        userDTO: UserRDTOWithRelations = Depends(check_admin_and_client),
        schedule_id: int = Path(description="Идентификатор заказа"),
        repo: ScheduleRepository = Depends(ScheduleRepository),
        orderRepo: OrderRepository = Depends(OrderRepository),
    ):
        return await repo.cancel_one_schedule(
            schedule_id=schedule_id, dto=dto, orderRepo=orderRepo, userDTO=userDTO
        )
