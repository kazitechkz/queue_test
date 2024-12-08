from datetime import date, datetime, time, timedelta

from fastapi import Depends
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.core.schedule_core import get_vehicle_information
from app.domain.models.order_model import OrderModel
from app.domain.models.organization_employee_model import OrganizationEmployeeModel
from app.domain.models.organization_model import OrganizationModel
from app.domain.models.schedule_model import ScheduleModel
from app.domain.models.user_model import UserModel
from app.domain.models.vehicle_model import VehicleModel
from app.domain.models.workshop_schedule_model import WorkshopScheduleModel
from app.feature.operation.operation_repository import OperationRepository
from app.feature.order.dtos.order_dto import OrderCDTO
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
    ScheduleCDTO,
    ScheduleIndividualCDTO,
    ScheduleLegalCDTO,
    ScheduleSpaceDTO,
)
from app.feature.schedule.filter.schedule_filter import ScheduleClientFromToFilter
from app.feature.user.user_repository import UserRepository
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.feature.workshop_schedule.workshop_schedule_repository import (
    WorkshopScheduleRepository,
)
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class ScheduleRepository(BaseRepository[ScheduleModel]):
    def __init__(self, db: Session = Depends(get_db)) -> None:
        super().__init__(ScheduleModel, db)

    async def check_late_schedules(self, orderRepo: OrderRepository):
        current_time = datetime.now()
        filters = [
            (
                or_(
                    and_(
                        self.model.end_at < current_time,
                        self.model.rescheduled_end_at is None,
                        self.model.is_active is True,
                        self.model.is_used is False,
                    ),
                    and_(
                        self.model.rescheduled_end_at < current_time,
                        self.model.rescheduled_end_at is not None,
                        self.model.is_active is True,
                        self.model.is_used is False,
                    ),
                )
            )
        ]
        updated = 0
        schedules = await self.get_all_with_filter(filters=filters)
        schedule_ids = [schedule.id for schedule in schedules]
        order_ids = [schedule.order_id for schedule in schedules]
        if len(schedule_ids) > 0:
            updated_value = {
                "canceled_at": current_time,
                "cancel_reason": "Опоздали",
                "is_active": False,
                "is_used": False,
                "is_executed": False,
                "is_canceled": True,
            }
            updated = await self.update_with_filters(
                update_values=updated_value,
                filters=[and_(self.model.id.in_(schedule_ids))],
            )
            orders = await orderRepo.get_all_with_filter(
                filters=[and_(orderRepo.model.id.in_(order_ids))]
            )
            for order in orders:
                await self.calculate_order(order=order, orderRepo=orderRepo)
        return updated

    async def my_schedules_count(
        self,
        userDTO: UserRDTOWithRelations,
        filter: ScheduleClientFromToFilter,
        date_filters: list,
        orderRepo: OrderRepository,
    ) -> list[ScheduleCalendarDTO]:
        filters = []

        if filter.order_id:
            order = await orderRepo.get(id=filter.order_id)
            if order is None:
                msg = "Заказ не найден"
                raise AppExceptionResponse.bad_request(msg)
            if userDTO.user_type.value == TableConstantsNames.UserLegalTypeValue:
                organization_ids = [
                    organization.id for organization in userDTO.organizations
                ]
                if order.organization_id not in organization_ids:
                    msg = "Заказ не найден или не принадлежит компании"
                    raise AppExceptionResponse.bad_request(msg)
            filters.append(and_(self.model.order_id == filter.order_id))
        if userDTO.user_type.value == TableConstantsNames.UserLegalTypeValue:
            organization_ids = [organization.id for organization in userDTO.organizations]
            filters.append(and_(self.model.organization_id.in_(organization_ids)))
        if userDTO.user_type.value == TableConstantsNames.UserIndividualTypeValue:
            filters.append(
                and_(
                    or_(
                        self.model.owner_id == userDTO.id,
                        self.model.driver_id == userDTO.id,
                    )
                )
            )
        start_date = datetime.combine(filter.start_at, time(0, 0, 0))
        end_date = datetime.combine(filter.end_at, time(23, 59, 59))
        filters.append(
            and_(self.model.start_at >= start_date, self.model.end_at <= end_date)
        )
        schedules = await self.get_all_with_filter(filters=filters)
        schedule_calendars_dto = []
        for date_filter in date_filters:
            total = [
                schedule.id
                for schedule in schedules
                if schedule.start_at >= date_filter[0]
                and schedule.start_at < date_filter[1]
            ]
            active_schedule = [
                schedule.id
                for schedule in schedules
                if schedule.is_active
                and schedule.start_at >= date_filter[0]
                and schedule.start_at < date_filter[1]
            ]
            canceled_schedule = [
                schedule.id
                for schedule in schedules
                if schedule.is_canceled
                and schedule.start_at >= date_filter[0]
                and schedule.start_at < date_filter[1]
            ]

            executed_schedule = [
                schedule.id
                for schedule in schedules
                if schedule.is_executed
                and schedule.start_at >= date_filter[0]
                and schedule.start_at < date_filter[1]
            ]
            if len(total) > 0:
                schedule_calendars_dto.append(
                    ScheduleCalendarDTO(
                        scheduled_at=date_filter[0].date(),
                        total=len(total),
                        total_active=len(active_schedule),
                        total_canceled=len(canceled_schedule),
                        total_executed=len(executed_schedule),
                    )
                )

        return schedule_calendars_dto

    async def get_active_schedules(
        self, userDTO: UserRDTOWithRelations, operationRepo: OperationRepository
    ):
        operations = await operationRepo.get_all_with_filter(
            filters=[and_(operationRepo.model.role_value == userDTO.role.value)]
        )
        operation_ids = [operation.id for operation in operations]
        filters = []
        exclude_id = None
        entry_filter = None
        for operation in operations:
            if operation.value == TableConstantsNames.EntryOperationName:
                entry_filter = and_(
                    self.model.current_operation_id == operation.id,
                    self.model.responsible_name is None,
                    self.model.is_active is True,
                    or_(
                        and_(
                            self.model.rescheduled_start_at is None,
                            self.model.rescheduled_end_at is None,
                            self.model.start_at <= datetime.now(),
                            self.model.end_at >= datetime.now(),
                        ),
                        and_(
                            self.model.rescheduled_start_at <= datetime.now(),
                            self.model.rescheduled_end_at >= datetime.now(),
                        ),
                    ),
                )
                exclude_id = operation.id
            elif entry_filter is not None:
                if exclude_id in operation_ids:
                    operation_ids.remove(exclude_id)
                filters.append(
                    or_(
                        entry_filter,
                        and_(
                            self.model.current_operation_id
                            == TableConstantsNames.ExitCheckOperationId,
                            self.model.responsible_id is None,
                            self.model.responsible_name is None,
                            self.model.is_active is True,
                        ),
                    )
                )
            else:
                filters.append(
                    and_(
                        self.model.current_operation_id.in_(operation_ids),
                        self.model.responsible_id is None,
                        self.model.responsible_name is None,
                        self.model.is_active is True,
                    )
                )

        return await self.get_all_with_filter(
            filters=filters, options=[selectinload(self.model.current_operation)]
        )

    async def get_canceled_schedules(
        self, userDTO: UserRDTOWithRelations, operationRepo: OperationRepository
    ):
        operations = await operationRepo.get_all_with_filter(
            filters=[and_(operationRepo.model.role_value == userDTO.role.value)]
        )
        operation_ids = [operation.id for operation in operations]
        start_of_day = datetime.combine(datetime.today(), time(0, 0, 0))
        end_of_day = datetime.combine(datetime.today(), time(23, 59, 59))
        schedules = await self.get_all_with_filter(
            filters=[
                and_(
                    self.model.current_operation_id.in_(operation_ids),
                    self.model.is_canceled is True,
                    self.model.start_at > start_of_day,
                    self.model.end_at < end_of_day,
                )
            ],
            options=[selectinload(self.model.current_operation)],
        )
        return schedules

    async def calculate_order(
        self, order: OrderModel, orderRepo: OrderRepository
    ) -> None:
        schedule_booked = await self.get_all_with_filter(
            filters=[
                and_(
                    self.model.order_id == order.id,
                    self.model.is_active is True,
                    self.model.is_executed is False,
                )
            ]
        )
        schedule_released = await self.get_all_with_filter(
            filters=[
                and_(
                    self.model.order_id == order.id,
                    self.model.is_active is False,
                    self.model.is_executed is True,
                )
            ]
        )
        order_dto = OrderCDTO.from_orm(order)
        # Рассчитываем суммарные объемы загрузки
        release_max = sum(schedule.vehicle_netto_kg for schedule in schedule_released)
        booked_max = sum(schedule.loading_volume_kg for schedule in schedule_booked)

        # Присваиваем рассчитанные значения в DTO
        if order.status_id == TableConstantsNames.OrderStatusWaitingForExecutionId:
            order_dto.status_id = 6
        order_dto.quan_booked = booked_max
        order_dto.quan_released = release_max
        await orderRepo.update(obj=order, dto=order_dto)

    async def create_individual_schedule(
        self,
        userDTO: UserRDTOWithRelations,
        dto: ScheduleIndividualCDTO,
        orderRepo: OrderRepository,
        vehicleRepo: VehicleRepository,
        workshopScheduleRepo: WorkshopScheduleRepository,
    ):
        trailer = None
        active_schedules = None
        order = await orderRepo.get(id=dto.order_id)
        vehicle = await vehicleRepo.get(id=dto.vehicle_id)
        workshopSchedule = await workshopScheduleRepo.get(id=dto.workshop_schedule_id)
        if order:
            active_schedules = await self.get_schedule(
                workshop_sap_id=order.workshop_sap_id,
                schedule_date=dto.scheduled_data,
                workshopScheduleRepo=workshopScheduleRepo,
            )
        if dto.trailer_id is not None:
            trailer = await vehicleRepo.get(id=dto.trailer_id)
        # Статическая проверка
        self.check_individual_form(
            dto=dto,
            order=order,
            vehicle=vehicle,
            trailer=trailer,
            userDTO=userDTO,
            workshopSchedule=workshopSchedule,
            openWorkshopSchedules=active_schedules,
        )
        # Проверка доступных машин
        await self.check_available_vehicle_or_driver(
            scheduled_data=dto.scheduled_data,
            start_at=dto.start_at,
            end_at=dto.end_at,
            vehicle_id=dto.vehicle_id,
            trailer_id=dto.trailer_id,
        )

        scheduleDTO = self.prepare_dto_individual(
            dto=dto, order=order, userDTO=userDTO, vehicle=vehicle, trailer=trailer
        )
        schedule = await self.create(obj=ScheduleModel(**scheduleDTO.dict()))
        await self.calculate_order(order=order, orderRepo=orderRepo)
        return schedule

    async def create_legal_schedule(
        self,
        userDTO: UserRDTOWithRelations,
        dto: ScheduleLegalCDTO,
        orderRepo: OrderRepository,
        userRepo: UserRepository,
        vehicleRepo: VehicleRepository,
        workshopScheduleRepo: WorkshopScheduleRepository,
        organizationRepo: OrganizationRepository,
        organizationEmployeeRepo: OrganizationEmployeeRepository,
    ):
        trailer = None
        organization = None
        organizationEmployee = None
        active_schedules = None
        driver: UserRDTOWithRelations | UserModel = userDTO
        order = await orderRepo.get(id=dto.order_id)
        if order is not None:
            organization = await organizationRepo.get_first_with_filters(
                filters=[{"owner_id": userDTO.id}, {"id": dto.organization_id}]
            )
            active_schedules = await self.get_schedule(
                workshop_sap_id=order.workshop_sap_id,
                schedule_date=dto.scheduled_data,
                workshopScheduleRepo=workshopScheduleRepo,
            )
        vehicle = await vehicleRepo.get(id=dto.vehicle_id)
        workshopSchedule = await workshopScheduleRepo.get(id=dto.workshop_schedule_id)
        if organization is not None and dto.driver_id != userDTO.id:
            organizationEmployee = await organizationEmployeeRepo.get_first_with_filters(
                filters=[
                    {"organization_id": organization.id, "employee_id": dto.driver_id}
                ]
            )
            if organizationEmployee is not None:
                driver = await userRepo.get(id=dto.driver_id)
        if dto.trailer_id is not None:
            trailer = await vehicleRepo.get(id=dto.trailer_id)
            # Статическая проверка
        self.check_legal_form(
            dto=dto,
            order=order,
            vehicle=vehicle,
            trailer=trailer,
            userDTO=userDTO,
            organization=organization,
            organizationEmployee=organizationEmployee,
            workshopSchedule=workshopSchedule,
            openWorkshopSchedules=active_schedules,
        )
        # Проверка доступных машин
        await self.check_available_vehicle_or_driver(
            scheduled_data=dto.scheduled_data,
            start_at=dto.start_at,
            end_at=dto.end_at,
            vehicle_id=dto.vehicle_id,
            trailer_id=dto.trailer_id,
        )
        scheduleDTO = self.prepare_dto_legal(
            dto=dto,
            order=order,
            userDTO=userDTO,
            vehicle=vehicle,
            trailer=trailer,
            organization=organization,
            driver=driver,
        )
        schedule = await self.create(obj=ScheduleModel(**scheduleDTO.dict()))
        await self.calculate_order(order=order, orderRepo=orderRepo)
        return schedule

    async def get_schedule(
        self,
        workshop_sap_id: str,
        schedule_date: datetime.date,
        workshopScheduleRepo: WorkshopScheduleRepository,
    ) -> list[ScheduleSpaceDTO]:
        active_schedule = await workshopScheduleRepo.get_with_filter(
            filters=[
                and_(
                    workshopScheduleRepo.model.workshop_sap_id == workshop_sap_id,
                    workshopScheduleRepo.model.date_start <= schedule_date,
                    workshopScheduleRepo.model.date_end >= schedule_date,
                    workshopScheduleRepo.model.is_active is True,
                )
            ]
        )
        if active_schedule is None:
            msg = "Активное расписание не найдено"
            raise AppExceptionResponse.not_found(msg)
        time_start = time(0, 0, 59)
        time_end = time(23, 59, 59)
        date_start = datetime.combine(schedule_date, time_start)
        date_end = datetime.combine(schedule_date, time_end)
        schedules = await self.get_all_with_filter(
            filters=[
                and_(
                    self.model.is_active is True,
                    self.model.start_at > date_start,
                    self.model.start_at < date_end,
                )
            ]
        )

        planned_schedules = []
        # Преобразуем start_time, end_time и current_time в datetime для удобной работы
        current_time_dt = datetime.combine(datetime.today(), datetime.now().time())
        start_time_dt = datetime.combine(datetime.today(), active_schedule.start_at)
        datetime.combine(datetime.today(), active_schedule.end_at)

        # Если дата в будущем, используем время начала рабочего дня
        if schedule_date > current_time_dt.date():
            current_time_dt = start_time_dt
        # Если дата сегодня, проверяем текущее время
        elif schedule_date == current_time_dt.date():
            if current_time_dt.time() > active_schedule.start_at:
                # Корректируем расписание с ближайшего интервала
                time_diff = (current_time_dt - start_time_dt).total_seconds()
                full_intervals_passed = time_diff // (
                    (
                        active_schedule.car_service_min
                        + active_schedule.break_between_service_min
                    )
                    * 60
                )
                adjusted_start_time = start_time_dt + timedelta(
                    minutes=(full_intervals_passed + 1)
                    * (
                        active_schedule.car_service_min
                        + active_schedule.break_between_service_min
                    )
                )
                current_time_dt = max(adjusted_start_time, current_time_dt)
            else:
                current_time_dt = start_time_dt
        else:
            # Если дата в прошлом, расписание не генерируем
            msg = "Нельзя получить расписание для прошедших дат."
            raise AppExceptionResponse.bad_request(msg)

        # Генерация расписания с учетом текущего времени или указанной даты
        while current_time_dt.time() < active_schedule.end_at:
            # Время окончания обслуживания
            service_end_time = current_time_dt + timedelta(
                minutes=active_schedule.car_service_min
            )

            if service_end_time.time() > active_schedule.end_at:
                break

            filtered_items = [
                item
                for item in schedules
                if item.start_at
                == datetime.combine(schedule_date, current_time_dt.time())
            ]
            space = 0
            if filtered_items is not None:
                space = len(filtered_items)
            free_space = active_schedule.machine_at_one_time - space
            if free_space >= 1:
                scheduled_time_dto = ScheduleSpaceDTO(
                    workshop_schedule_id=active_schedule.id,
                    scheduled_data=schedule_date,
                    start_at=current_time_dt.time(),
                    end_at=service_end_time.time(),
                    free_space=free_space,
                )
                # Добавляем в расписание интервал работы
                planned_schedules.append(scheduled_time_dto)
            # Добавляем перерыв
            current_time_dt = service_end_time + timedelta(
                minutes=active_schedule.break_between_service_min
            )

        return planned_schedules

    async def reshedule_data(self, dto: RescheduleAllDTO):
        start_at = datetime.combine(date=dto.scheduled_data, time=time(0, 0, 0))
        end_at = datetime.combine(date=dto.scheduled_data, time=time(23, 59, 59))

        if dto.scheduled_data == date.today():
            start_at = datetime.now()

        schedules = await self.get_all_with_filter(
            filters=[
                and_(
                    self.model.is_active is True,
                    self.model.is_used is False,
                    self.model.end_at > start_at,
                    self.model.end_at < end_at,
                )
            ]
        )
        schedules_update = []
        for schedule in schedules:
            schedule.rescheduled_start_at = schedule.start_at + timedelta(
                minutes=dto.minute
            )
            schedule.rescheduled_end_at = schedule.end_at + timedelta(minutes=dto.minute)
            updated_schedule = await self.update(
                obj=schedule, dto=ScheduleCDTO.from_orm(schedule)
            )
            schedules_update.append(updated_schedule)
        return schedules_update

    async def reschedule_to_date(self, schedule_id: int, dto: RescheduleOneDTO):
        schedule = await self.get_first_with_filter(
            and_(
                self.model.id == schedule_id,
                self.model.is_active is True,
                self.model.is_used is False,
            )
        )
        if schedule is None:
            msg = "Расписание не найдено либо неактивно"
            raise AppExceptionResponse.bad_request(msg)

        schedule_dto = ScheduleCDTO.from_orm(schedule)
        schedule_dto.rescheduled_start_at = datetime.combine(
            dto.scheduled_data, dto.start_at
        )
        schedule_dto.rescheduled_end_at = datetime.combine(dto.scheduled_data, dto.end_at)
        updated_schedule = await self.update(obj=schedule, dto=schedule_dto)
        return updated_schedule

    async def cancel_one_schedule(
        self,
        schedule_id: int,
        dto: ScheduleCancelOneDTO,
        orderRepo: OrderRepository,
        userDTO: UserRDTOWithRelations,
    ):
        filters = []
        if userDTO.role.value == TableConstantsNames.RoleAdminValue:
            filters.append(
                and_(
                    self.model.id == schedule_id,
                    self.model.is_active is True,
                    self.model.is_used is False,
                )
            )
        else:
            filters.append(
                and_(
                    self.model.id == schedule_id,
                    self.model.is_active is True,
                    self.model.is_used is False,
                    self.model.owner_id == userDTO.id,
                )
            )
        schedule = await self.get_first_with_filter(filters=filters)
        if schedule is None:
            msg = "Расписание не найдено либо неактивно"
            raise AppExceptionResponse.bad_request(msg)
        current_datetime = datetime.now()
        schedule_dto = ScheduleCDTO.from_orm(schedule)
        schedule_dto.canceled_at = current_datetime
        schedule_dto.canceled_by = userDTO.id
        schedule_dto.cancel_reason = dto.cancel_reason
        schedule_dto.is_active = False
        schedule_dto.is_used = False
        schedule_dto.is_executed = False
        schedule_dto.is_canceled = True
        updated_schedule = await self.update(obj=schedule, dto=schedule_dto)
        if updated_schedule:
            order = await orderRepo.get(id=updated_schedule.order_id)
            await self.calculate_order(order=order, orderRepo=orderRepo)
        return updated_schedule

    async def cancel_all_schedules(
        self,
        dto: ScheduleCancelDTO,
        orderRepo: OrderRepository,
        userDTO: UserRDTOWithRelations,
    ):
        start_at = datetime.combine(date=dto.scheduled_data, time=time(0, 0, 0))
        end_at = datetime.combine(date=dto.scheduled_data, time=time(23, 59, 59))
        if dto.scheduled_data == date.today():
            start_at = datetime.now()
        schedules = await self.get_all_with_filter(
            filters=[
                and_(
                    self.model.is_active is True,
                    self.model.is_used is False,
                    self.model.end_at > start_at,
                    self.model.end_at < end_at,
                )
            ]
        )
        schedules_update = []
        current_datetime = datetime.now()
        for schedule in schedules:
            # Отменяем состояние Расписания
            schedule_dto = ScheduleCDTO.from_orm(schedule)
            schedule_dto.canceled_at = current_datetime
            schedule_dto.canceled_by = userDTO.id
            schedule_dto.cancel_reason = dto.cancel_reason
            schedule_dto.is_active = False
            schedule_dto.is_used = False
            schedule_dto.is_executed = False
            schedule_dto.is_canceled = True
            updated_schedule = await self.update(obj=schedule, dto=schedule_dto)
            if updated_schedule:
                order = await orderRepo.get(id=updated_schedule.order_id)
                await self.calculate_order(order=order, orderRepo=orderRepo)
            schedules_update.append(updated_schedule)
        return schedules_update

    @staticmethod
    def prepare_dto_individual(
        dto: ScheduleIndividualCDTO,
        order: OrderModel | None,
        userDTO: UserRDTOWithRelations,
        vehicle: VehicleModel | None,
        trailer: VehicleModel | None,
    ) -> ScheduleCDTO:
        quan_kg = int(dto.booked_quan_t * 1000)

        if trailer is None:
            trailer_id = None
            trailer_info = None
        else:
            trailer_id = trailer.id
            trailer_info = get_vehicle_information(trailer)

        return ScheduleCDTO(
            order_id=order.id,
            zakaz=order.zakaz,
            owner_id=userDTO.id,
            owner_name=userDTO.name,
            owner_iin=userDTO.iin,
            driver_id=userDTO.id,
            driver_name=userDTO.name,
            driver_iin=userDTO.iin,
            vehicle_id=vehicle.id,
            vehicle_info=get_vehicle_information(vehicle),
            trailer_id=trailer_id,
            trailer_info=trailer_info,
            workshop_schedule_id=dto.workshop_schedule_id,
            current_operation_id=1,
            start_at=datetime.combine(dto.scheduled_data, dto.start_at),
            end_at=datetime.combine(dto.scheduled_data, dto.end_at),
            loading_volume_kg=quan_kg,
        )

    @staticmethod
    def prepare_dto_legal(
        dto: ScheduleLegalCDTO,
        order: OrderModel | None,
        userDTO: UserRDTOWithRelations,
        organization: OrganizationModel,
        driver: UserRDTOWithRelations | UserModel,
        vehicle: VehicleModel | None,
        trailer: VehicleModel | None,
    ) -> ScheduleCDTO:
        quan_kg = int(dto.booked_quan_t * 1000)

        if trailer is None:
            trailer_id = None
            trailer_info = None
        else:
            trailer_id = trailer.id
            trailer_info = get_vehicle_information(trailer)

        return ScheduleCDTO(
            order_id=order.id,
            zakaz=order.zakaz,
            owner_id=userDTO.id,
            owner_name=userDTO.name,
            owner_iin=userDTO.iin,
            driver_id=driver.id,
            driver_name=driver.name,
            driver_iin=driver.iin,
            organization_id=organization.id,
            organization_full_name=organization.full_name,
            organization_bin=organization.bin,
            vehicle_id=vehicle.id,
            vehicle_info=get_vehicle_information(vehicle),
            trailer_id=trailer_id,
            trailer_info=trailer_info,
            workshop_schedule_id=dto.workshop_schedule_id,
            current_operation_id=1,
            start_at=datetime.combine(dto.scheduled_data, dto.start_at),
            end_at=datetime.combine(dto.scheduled_data, dto.end_at),
            loading_volume_kg=quan_kg,
        )

    @staticmethod
    def check_individual_form(
        dto: ScheduleIndividualCDTO,
        order: OrderModel | None,
        userDTO: UserRDTOWithRelations,
        vehicle: VehicleModel | None,
        trailer: VehicleModel | None,
        workshopSchedule: WorkshopScheduleModel | None,
        openWorkshopSchedules: list[ScheduleSpaceDTO] | None,
    ) -> None:
        if order is None:
            msg = "Заказ не найден"
            raise AppExceptionResponse.bad_request(msg)
        if order.owner_id != userDTO.id:
            msg = "У вас нет доступа к данному заказу"
            raise AppExceptionResponse.bad_request(msg)
        if order.is_paid is False or order.txn_id is None:
            msg = "Сначала оплатите заказ"
            raise AppExceptionResponse.bad_request(msg)
        if order.quan_left < 1000:
            msg = "Вы реализовали весь материал"
            raise AppExceptionResponse.bad_request(msg)
        if vehicle is None:
            msg = "Транспорт не найден"
            raise AppExceptionResponse.bad_request(msg)
        if vehicle.owner_id != userDTO.id:
            msg = "У вас нет доступа к данному транспорту"
            raise AppExceptionResponse.bad_request(msg)
        if dto.trailer_id is not None:
            if trailer is None:
                msg = "Прицеп не найден"
                raise AppExceptionResponse.bad_request(msg)
            if trailer.owner_id != userDTO.id:
                msg = "У вас нет доступа к данному прицепу"
                raise AppExceptionResponse.bad_request(msg)
        if workshopSchedule is None:
            msg = "Шаблонная модель расписания цеха не найдена"
            raise AppExceptionResponse.bad_request(msg)
        if order.workshop_sap_id != workshopSchedule.workshop_sap_id:
            msg = "Шаблонная модель расписания цеха не совпадает"
            raise AppExceptionResponse.bad_request(msg)
        if openWorkshopSchedules is None:
            msg = "Время расписания не найдено или забронировано"
            raise AppExceptionResponse.bad_request(msg)
        scheduled_at = next(
            (
                openSchedule
                for openSchedule in openWorkshopSchedules
                if openSchedule.start_at == dto.start_at
                and openSchedule.end_at == dto.end_at
            ),
            None,
        )
        if scheduled_at is None:
            msg = "Время расписания не найдено или забронировано"
            raise AppExceptionResponse.bad_request(msg)
        quan_kg = int(dto.booked_quan_t * 1000)
        vehicle_load = vehicle.load_max_kg
        if trailer:
            vehicle_load += trailer.weight_clean_kg
        if quan_kg > order.quan_left:
            msg = "Вы не можете забронировать материал объем которого превышают доступный остаток"
            raise AppExceptionResponse.bad_request(msg)
        if quan_kg > vehicle_load:
            msg = "Вы не можете забронировать материал объем которого превышают максимальную грузоподъемность транспорта"
            raise AppExceptionResponse.bad_request(msg)

    @staticmethod
    def check_legal_form(
        dto: ScheduleLegalCDTO,
        order: OrderModel | None,
        userDTO: UserRDTOWithRelations,
        vehicle: VehicleModel | None,
        trailer: VehicleModel | None,
        organization: OrganizationModel | None,
        organizationEmployee: OrganizationEmployeeModel | None,
        workshopSchedule: WorkshopScheduleModel | None,
        openWorkshopSchedules: list[ScheduleSpaceDTO] | None,
    ) -> None:
        if organization is None:
            msg = "Организация не найдена"
            raise AppExceptionResponse.bad_request(msg)
        if order is None:
            msg = "Заказ не найден"
            raise AppExceptionResponse.bad_request(msg)
        if order.organization_id != dto.organization_id:
            msg = "У вас нет доступа к данному заказу"
            raise AppExceptionResponse.bad_request(msg)
        if order.is_paid is False or order.txn_id is None:
            msg = "Сначала оплатите заказ"
            raise AppExceptionResponse.bad_request(msg)
        if order.quan_left < 1000:
            msg = "Вы реализовали весь материал"
            raise AppExceptionResponse.bad_request(msg)
        if vehicle is None:
            msg = "Транспорт не найден"
            raise AppExceptionResponse.bad_request(msg)
        if vehicle.organization_id != dto.organization_id:
            msg = "У вас нет доступа к данному транспорту"
            raise AppExceptionResponse.bad_request(msg)
        if dto.trailer_id is not None:
            if trailer is None:
                msg = "Прицеп не найден"
                raise AppExceptionResponse.bad_request(msg)
            if trailer.organization_id != dto.organization_id:
                msg = "У вас нет доступа к данному прицепу"
                raise AppExceptionResponse.bad_request(msg)
        if workshopSchedule is None:
            msg = "Шаблонная модель расписания цеха не найдена"
            raise AppExceptionResponse.bad_request(msg)
        if order.workshop_sap_id != workshopSchedule.workshop_sap_id:
            msg = "Шаблонная модель расписания цеха не совпадает"
            raise AppExceptionResponse.bad_request(msg)
        if dto.driver_id != userDTO.id and organizationEmployee is None:
            msg = "У вас нет доступа к данному водителю"
            raise AppExceptionResponse.bad_request(msg)
        if openWorkshopSchedules is None:
            msg = "Время расписания забронировано или не найдено"
            raise AppExceptionResponse.bad_request(msg)
        scheduled_at = next(
            (
                openSchedule
                for openSchedule in openWorkshopSchedules
                if openSchedule.start_at == dto.start_at
                and openSchedule.end_at == dto.end_at
            ),
            None,
        )
        if scheduled_at is None:
            msg = "Время расписания забронировано или не найдено"
            raise AppExceptionResponse.bad_request(msg)
        quan_kg = int(dto.booked_quan_t * 1000)
        vehicle_load = vehicle.load_max_kg
        if trailer:
            vehicle_load += trailer.weight_clean_kg
        if quan_kg > order.quan_left:
            msg = "Вы не можете забронировать материал объем которого превышают доступный остаток"
            raise AppExceptionResponse.bad_request(msg)
        if quan_kg > vehicle_load:
            msg = "Вы не можете забронировать материал объем которого превышают максимальную грузоподъемность транспорта"
            raise AppExceptionResponse.bad_request(msg)

    async def check_available_vehicle_or_driver(
        self,
        scheduled_data: date,
        start_at: time,
        end_at: time,
        vehicle_id: int,
        trailer_id: int | None,
    ) -> None:
        start_at = datetime.combine(scheduled_data, start_at)
        end_at = datetime.combine(scheduled_data, end_at)
        filters = [
            and_(
                self.model.vehicle_id == vehicle_id,
                self.model.start_at == start_at,
                self.model.end_at == end_at,
            )
        ]
        if trailer_id is not None:
            filters.append(
                and_(
                    or_(
                        self.model.vehicle_id == vehicle_id,
                        self.model.trailer_id == trailer_id,
                    )
                )
            )
        else:
            filters.append(and_(self.model.vehicle_id == vehicle_id))
        result = await self.get_with_filter(filters=filters)
        if result is not None:
            msg = "Данный транспорт или трейлер уже занят на текущее время"
            raise AppExceptionResponse.bad_request(msg)
