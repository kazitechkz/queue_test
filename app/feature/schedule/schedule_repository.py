from datetime import datetime, timedelta, time
from typing import Optional, Union

from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

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
from app.domain.models.workshop_model import WorkshopModel
from app.domain.models.workshop_schedule_model import WorkshopScheduleModel
from app.feature.order.dtos.order_dto import OrderCDTO
from app.feature.order.order_repository import OrderRepository
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.organization_employee.organization_employee_repository import OrganizationEmployeeRepository
from app.feature.schedule.dtos.schedule_dto import ScheduleIndividualCDTO, ScheduleCDTO, ScheduleLegalCDTO, \
    ScheduleSpaceDTO
from app.feature.user.user_repository import UserRepository
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.feature.workshop_schedule.workshop_schedule_repository import WorkshopScheduleRepository
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class ScheduleRepository(BaseRepository[ScheduleModel]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(ScheduleModel, db)

    async def calculate_order(self, order: OrderModel, orderRepo: OrderRepository, ):
        schedule_booked = await self.get_all_with_filter(filters=[
            and_(self.model.order_id == order.id, self.model.is_active == True, self.model.is_executed == False)
        ])
        schedule_released = await self.get_all_with_filter(filters=[
            and_(self.model.order_id == order.id, self.model.is_active == False, self.model.is_executed == True)
        ])
        order_dto = OrderCDTO.from_orm(order)
        # Рассчитываем суммарные объемы загрузки
        release_max = sum(schedule.vehicle_netto_kg for schedule in schedule_released)
        booked_max = sum(schedule.loading_volume_kg for schedule in schedule_booked)

        # Присваиваем рассчитанные значения в DTO
        order_dto.quan_booked = booked_max
        order_dto.quan_released = release_max
        await orderRepo.update(obj=order, dto=order_dto)

    async def create_individual_schedule(
            self,
            userDTO: UserRDTOWithRelations,
            dto: ScheduleIndividualCDTO,
            orderRepo: OrderRepository,
            vehicleRepo: VehicleRepository,
            workshopScheduleRepo: WorkshopScheduleRepository
    ):
        trailer = None
        order = await orderRepo.get(id=dto.order_id)
        vehicle = await vehicleRepo.get(id=dto.vehicle_id)
        workshopSchedule = await workshopScheduleRepo.get(id=dto.workshop_id)
        if dto.trailer_id is not None:
            trailer = await vehicleRepo.get(id=dto.trailer_id)
        self.check_individual_form(dto=dto, order=order, vehicle=vehicle, trailer=trailer, userDTO=userDTO,
                                   workshopSchedule=workshopSchedule)
        scheduleDTO = self.prepare_dto_individual(dto=dto, order=order, userDTO=userDTO,
                                                  vehicle=vehicle, trailer=trailer)
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
        driver: Union[UserRDTOWithRelations, UserModel] = userDTO
        print(f"Driver is: {driver}")
        print(f"userDTO is: {userDTO}")
        print(f"dto is: {dto}")
        order = await orderRepo.get(id=dto.order_id)
        if order is not None:
            organization = await organizationRepo.get_first_with_filters(
                filters=[{"owner_id": userDTO.id}, {"id": dto.organization_id}])
            print(f"Org is: {organization}")
        vehicle = await vehicleRepo.get(id=dto.vehicle_id)
        workshopSchedule = await workshopScheduleRepo.get(id=dto.workshop_schedule_id)
        if organization is not None and dto.driver_id != userDTO.id:
            organizationEmployee = await organizationEmployeeRepo.get_first_with_filters(
                filters=[{"organization_id": organization.id, "employee_id": dto.driver_id}])
            if organizationEmployee is not None:
                driver = await userRepo.get(id=dto.driver_id)
        if dto.trailer_id is not None:
            trailer = await vehicleRepo.get(id=dto.trailer_id)
        self.check_legal_form(dto=dto,
                              order=order,
                              vehicle=vehicle,
                              trailer=trailer,
                              userDTO=userDTO,
                              organization=organization,
                              organizationEmployee=organizationEmployee,
                              workshopSchedule=workshopSchedule)
        scheduleDTO = self.prepare_dto_legal(dto=dto, order=order, userDTO=userDTO, vehicle=vehicle, trailer=trailer,
                                             organization=organization, driver=driver)
        schedule = await self.create(obj=ScheduleModel(**scheduleDTO.dict()))
        await self.calculate_order(order=order, orderRepo=orderRepo)
        return schedule

    async def get_schedule(
            self, workshop_sap_id: str,
            schedule_date: datetime.date,
            workshopScheduleRepo: WorkshopScheduleRepository,
    ):
        active_schedule = await workshopScheduleRepo.get_first_with_filters(
            filters=[{"workshop_sap_id": workshop_sap_id}])
        if active_schedule is None:
            raise AppExceptionResponse.not_found("Активное расписание не найдено")
        time_start = time(0, 0, 59)
        time_end = time(23, 59, 59)
        date_start = datetime.combine(schedule_date, time_start)
        date_end = datetime.combine(schedule_date, time_end)
        schedules = await self.get_all_with_filter(filters=[and_(
            self.model.is_active == True,
            self.model.start_at > date_start,
            self.model.start_at < date_end
        )])

        planned_schedules = []
        # Преобразуем start_time, end_time и current_time в datetime для удобной работы
        current_time_dt = datetime.combine(datetime.today(), datetime.now().time())
        start_time_dt = datetime.combine(datetime.today(), active_schedule.start_at)
        end_time_dt = datetime.combine(datetime.today(), active_schedule.end_at)

        # Если дата в будущем, используем время начала рабочего дня
        if schedule_date > current_time_dt.date():
            current_time_dt = start_time_dt
        # Если дата сегодня, проверяем текущее время
        elif schedule_date == current_time_dt.date():
            if current_time_dt.time() > active_schedule.start_at:
                # Корректируем расписание с ближайшего интервала
                time_diff = (current_time_dt - start_time_dt).total_seconds()
                full_intervals_passed = time_diff // (
                        (active_schedule.car_service_min + active_schedule.break_between_service_min) * 60)
                adjusted_start_time = start_time_dt + timedelta(
                    minutes=(full_intervals_passed + 1) * (
                            active_schedule.car_service_min + active_schedule.break_between_service_min))
                current_time_dt = max(adjusted_start_time, current_time_dt)
            else:
                current_time_dt = start_time_dt
        else:
            # Если дата в прошлом, расписание не генерируем
            raise AppExceptionResponse.bad_request("Нельзя получить расписание для прошедших дат.")

        # Генерация расписания с учетом текущего времени или указанной даты
        while current_time_dt.time() < active_schedule.end_at:
            # Время окончания обслуживания
            service_end_time = current_time_dt + timedelta(minutes=active_schedule.car_service_min)

            if service_end_time.time() > active_schedule.end_at:
                break

            filtered_items = [item for item in schedules if
                              item.start_at == datetime.combine(schedule_date, current_time_dt.time())]
            space = 0
            if filtered_items is not None:
                space = len(filtered_items)
            free_space = active_schedule.machine_at_one_time - space
            if free_space >= 1:
                scheduled_time_dto = ScheduleSpaceDTO(
                    scheduled_data=schedule_date,
                    start_at=current_time_dt.time(),
                    end_at=service_end_time.time(),
                    free_space=free_space
                )
                # Добавляем в расписание интервал работы
                planned_schedules.append(scheduled_time_dto)
            # Добавляем перерыв
            current_time_dt = service_end_time + timedelta(minutes=active_schedule.break_between_service_min)

        return planned_schedules

    @staticmethod
    def prepare_dto_individual(dto: ScheduleIndividualCDTO, order: Optional[OrderModel], userDTO: UserRDTOWithRelations,
                               vehicle: Optional[VehicleModel], trailer: Optional[VehicleModel]) -> ScheduleCDTO:
        vehicle_load = vehicle.load_max_kg
        if trailer is None:
            trailer_id = None
            trailer_info = None
        else:
            trailer_id = trailer.id
            trailer_info = get_vehicle_information(trailer)
            vehicle_load += trailer.load_max_kg

        if order.quan_left < vehicle_load:
            vehicle_load = order.quan_left

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
            workshop_schedule_id=dto.workshop_id,
            current_operation_id=1,
            start_at=datetime.combine(dto.scheduled_data, dto.start_at),
            end_at=datetime.combine(dto.scheduled_data, dto.end_at),
            loading_volume_kg=vehicle_load,
        )

    @staticmethod
    def prepare_dto_legal(
            dto: ScheduleLegalCDTO,
            order: Optional[OrderModel],
            userDTO: UserRDTOWithRelations,
            organization: OrganizationModel,
            driver: Union[UserRDTOWithRelations, UserModel],
            vehicle: Optional[VehicleModel],
            trailer: Optional[VehicleModel],
    ) -> ScheduleCDTO:
        vehicle_load = vehicle.load_max_kg
        if trailer is None:
            trailer_id = None
            trailer_info = None
        else:
            trailer_id = trailer.id
            trailer_info = get_vehicle_information(trailer)
            vehicle_load += trailer.load_max_kg

        if order.quan_left < vehicle_load:
            vehicle_load = order.quan_left

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
            loading_volume_kg=vehicle_load,
        )

    @staticmethod
    def check_individual_form(dto: ScheduleIndividualCDTO, order: Optional[OrderModel], userDTO: UserRDTOWithRelations,
                              vehicle: Optional[VehicleModel], trailer: Optional[VehicleModel],
                              workshopSchedule: Optional[WorkshopScheduleModel]
                              ):
        if order is None:
            raise AppExceptionResponse.bad_request("Заказ не найден")
        if order.owner_id != userDTO.id:
            raise AppExceptionResponse.bad_request("У вас нет доступа к данному заказу")
        if order.is_paid == False or order.txn_id is None:
            raise AppExceptionResponse.bad_request("Сначала оплатите заказ")
        if order.quan_left < 1000:
            raise AppExceptionResponse.bad_request("Вы реализовали весь материал")
        if vehicle is None:
            raise AppExceptionResponse.bad_request("Транспорт не найден")
        if vehicle.owner_id != userDTO.id:
            raise AppExceptionResponse.bad_request("У вас нет доступа к данному транспорту")
        if dto.trailer_id is not None:
            if trailer is None:
                raise AppExceptionResponse.bad_request("Прицеп не найден")
            if trailer.owner_id != userDTO.id:
                raise AppExceptionResponse.bad_request("У вас нет доступа к данному прицепу")
        if workshopSchedule is None:
            raise AppExceptionResponse.bad_request("Шаблонная модель расписания цеха не найдена")
        if order.workshop_sap_id != workshopSchedule.workshop_sap_id:
            raise AppExceptionResponse.bad_request("Шаблонная модель расписания цеха не совпадает")

    @staticmethod
    def check_legal_form(
            dto: ScheduleLegalCDTO,
            order: Optional[OrderModel],
            userDTO: UserRDTOWithRelations,
            vehicle: Optional[VehicleModel],
            trailer: Optional[VehicleModel],
            organization: Optional[OrganizationModel],
            organizationEmployee: Optional[OrganizationEmployeeModel],
            workshopSchedule: Optional[WorkshopScheduleModel]
    ):
        if organization is None:
            raise AppExceptionResponse.bad_request("Организация не найдена")
        if order is None:
            raise AppExceptionResponse.bad_request("Заказ не найден")
        if order.organization_id != dto.organization_id:
            raise AppExceptionResponse.bad_request("У вас нет доступа к данному заказу")
        if order.is_paid == False or order.txn_id is None:
            raise AppExceptionResponse.bad_request("Сначала оплатите заказ")
        if order.quan_left < 1000:
            raise AppExceptionResponse.bad_request("Вы реализовали весь материал")
        if vehicle is None:
            raise AppExceptionResponse.bad_request("Транспорт не найден")
        if vehicle.organization_id != dto.organization_id:
            raise AppExceptionResponse.bad_request("У вас нет доступа к данному транспорту")
        if dto.trailer_id is not None:
            if trailer is None:
                raise AppExceptionResponse.bad_request("Прицеп не найден")
            if trailer.organization_id != dto.organization_id:
                raise AppExceptionResponse.bad_request("У вас нет доступа к данному прицепу")
        if workshopSchedule is None:
            raise AppExceptionResponse.bad_request("Шаблонная модель расписания цеха не найдена")
        if order.workshop_sap_id != workshopSchedule.workshop_sap_id:
            raise AppExceptionResponse.bad_request("Шаблонная модель расписания цеха не совпадает")
        if dto.driver_id != userDTO.id:
            if organizationEmployee is None:
                raise AppExceptionResponse.bad_request("У вас нет доступа к данному водителю")
