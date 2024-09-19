from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.core.schedule_core import get_vehicle_information
from app.domain.models.order_model import OrderModel
from app.domain.models.schedule_model import ScheduleModel
from app.domain.models.vehicle_model import VehicleModel
from app.domain.models.workshop_model import WorkshopModel
from app.domain.models.workshop_schedule_model import WorkshopScheduleModel
from app.feature.order.dtos.order_dto import OrderCDTO
from app.feature.order.order_repository import OrderRepository
from app.feature.schedule.dtos.schedule_dto import ScheduleIndividualCDTO, ScheduleCDTO
from app.feature.user.dtos.user_dto import UserRDTOWithRelations
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.feature.workshop_schedule.workshop_schedule_repository import WorkshopScheduleRepository


class ScheduleRepository(BaseRepository[ScheduleModel]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(ScheduleModel, db)

    async def calculate_order(self,order:OrderModel,orderRepo: OrderRepository,):
        schedule_booked = await self.get_all_with_filter(filters=[
            and_(self.model.order_id == order.id, self.model.is_active == True, self.model.is_executed == False)
        ])
        schedule_released = await self.get_all_with_filter(filters=[
            and_(self.model.order_id == order.id, self.model.is_active == False, self.model.is_executed == True)
        ])
        order_dto = OrderCDTO.from_orm(order)
        # Рассчитываем суммарные объемы загрузки
        release_max = sum(schedule.loading_volume_kg for schedule in schedule_released)
        booked_max = sum(schedule.loading_volume_kg for schedule in schedule_booked)

        # Присваиваем рассчитанные значения в DTO
        order_dto.quan_booked = booked_max
        order_dto.quan_released = release_max
        await orderRepo.update(obj=order,dto=order_dto)


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
        self.check_form(dto=dto, order=order, vehicle=vehicle, trailer=trailer, userDTO=userDTO,workshopSchedule=workshopSchedule)
        scheduleDTO = self.prepare_dto_individual(dto = dto, order=order, userDTO=userDTO,
                               vehicle=vehicle, trailer=trailer)
        schedule = await self.create(obj=ScheduleModel(**scheduleDTO.dict()))
        await self.calculate_order(order=order,orderRepo=orderRepo)
        return schedule




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
    def check_form(dto: ScheduleIndividualCDTO, order: Optional[OrderModel], userDTO: UserRDTOWithRelations,
                   vehicle: Optional[VehicleModel], trailer: Optional[VehicleModel],
                   workshopSchedule:Optional[WorkshopScheduleModel]
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
