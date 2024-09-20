from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.core.schedule_core import get_vehicle_information
from app.domain.models.initial_weight_model import InitialWeightModel
from app.domain.models.schedule_history_model import ScheduleHistoryModel
from app.domain.models.schedule_model import ScheduleModel
from app.feature.initial_weight.dtos.initial_weight_dto import InitialWeightCDTO
from app.feature.initial_weight.initial_weight_repository import InitialWeightRepository
from app.feature.operation.operation_repository import OperationRepository
from app.feature.order.order_repository import OrderRepository
from app.feature.schedule.dtos.schedule_dto import ScheduleCDTO, ScheduleRDTO
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryEnterFactoryDTO, ScheduleHistoryCDTO, \
    ScheduleHistoryDTO, ScheduleHistoryInitialWeightDTO
from app.feature.user.dtos.user_dto import UserRDTOWithRelations
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.shared.database_constants import TableConstantsNames


class ScheduleHistoryRepository(BaseRepository[ScheduleHistoryModel]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(ScheduleHistoryModel, db)
    #КПП
    async def process_kpp_entry_request(self,
                            schedule_id,
                            userRDTO:UserRDTOWithRelations,
                            scheduleRepo:ScheduleRepository,
                            ):
        schedule = await scheduleRepo.get_first_with_filter(filters=[
            and_(
                ScheduleModel.id == schedule_id,
                ScheduleModel.start_at <= datetime.now(),
                ScheduleModel.end_at >= datetime.now(),
                ScheduleModel.is_active == True,
                ScheduleModel.current_operation_id == TableConstantsNames.EntryOperationId
            )
        ])
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        schedule_history = await self.get_first_with_filters(filters=[{"schedule_id":schedule_id}])
        if schedule_history is not None:
            raise AppExceptionResponse.bad_request("Этап пройден")

        schedule_history_model = ScheduleHistoryModel(
            schedule_id = schedule_id,
            operation_id = TableConstantsNames.EntryOperationId,
            responsible_id = userRDTO.id,
            responsible_name = userRDTO.name,
            responsible_iin = userRDTO.iin,
            start_at=datetime.now()
        )

        return await self.create(obj=schedule_history_model)

    async def confirm_or_deny_entry(self,
                            schedule_history_id,
                            answer:ScheduleHistoryEnterFactoryDTO,
                            userRDTO:UserRDTOWithRelations,
                            scheduleRepo:ScheduleRepository,
                            orderRepo:OrderRepository
                            ):
        schedule_history = await self.get_first_with_filter(filters=[
            and_(
                self.model.id == schedule_history_id,
                self.model.responsible_id == userRDTO.id,
                self.model.is_passed == None
            )
        ])
        if schedule_history is None:
            raise AppExceptionResponse.bad_request("Этап не найден")
        schedule:ScheduleModel = await scheduleRepo.get(id=schedule_history.schedule_id)
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        schedule_dto = ScheduleCDTO.from_orm(schedule)
        schedule_history_dto = ScheduleHistoryCDTO.from_orm(schedule_history)
        schedule_history_dto.is_passed = answer.is_passed
        schedule_history_dto.cancel_reason = answer.cancel_reason
        schedule_history_dto.end_at = datetime.now()
        if not answer.is_passed:
            schedule_history_dto.canceled_at = datetime.now()
            schedule_dto.is_active = False
            schedule_dto.is_canceled = True
            schedule_dto.cancel_reason = answer.cancel_reason
            schedule_dto.canceled_by = userRDTO.id
        else:
            schedule_dto.current_operation_id = TableConstantsNames.InitialWeightOperationId
            schedule_dto.is_used = True
            new_schedule_history_model = ScheduleHistoryModel(
                schedule_id=schedule.id,
                operation_id=TableConstantsNames.InitialWeightOperationId,
            )
            await self.create(obj=new_schedule_history_model)

        await scheduleRepo.update(obj=schedule,dto=schedule_dto)
        order = await orderRepo.get(id=schedule.order_id)
        if order is not None:
            await scheduleRepo.calculate_order(order=order, orderRepo=orderRepo)
        return await self.update(obj=schedule_history,dto=schedule_history_dto)
    # КПП

    #Весовщик первичное
    async def accept_initial_weighing_request(self,
                            schedule_id,
                            userRDTO:UserRDTOWithRelations,
                            scheduleRepo:ScheduleRepository,
                            ):
        schedule = await scheduleRepo.get_first_with_filter(filters=[
            and_(
                ScheduleModel.id == schedule_id,
                ScheduleModel.is_active == True,
                ScheduleModel.current_operation_id == TableConstantsNames.InitialWeightOperationId
            )
        ])
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        schedule_history = await self.get_first_with_filters(filters=[{"schedule_id":schedule_id},{"operation_id":TableConstantsNames.InitialWeightOperationId}])
        if schedule_history is None:
            schedule_history = ScheduleHistoryModel(
                schedule_id=schedule.id,
                operation_id=TableConstantsNames.InitialWeightOperationId,
            )
            schedule_history = await self.create(obj=schedule_history)
        if schedule_history.responsible_id is not None:
            raise AppExceptionResponse.bad_request("Заявка уже принята в обработку")
        schedule_history_dto = ScheduleHistoryCDTO.from_orm(schedule_history)
        schedule_history_dto.responsible_id = userRDTO.id
        schedule_history_dto.responsible_name = userRDTO.name
        schedule_history_dto.responsible_iin = userRDTO.iin
        schedule_history_dto.start_at = datetime.now()
        return await self.update(obj=schedule_history,dto=schedule_history_dto)

    async def confirm_or_deny_initial_weighing(self,
                                              schedule_history_id,
                                              dto:ScheduleHistoryInitialWeightDTO,
                                              userRDTO: UserRDTOWithRelations,
                                              scheduleRepo: ScheduleRepository,
                                              initialWeightRepo:InitialWeightRepository,
                                              vehicleRepo: VehicleRepository,
                                              orderRepo: OrderRepository
                                              ):

        schedule_history = await self.get_first_with_filter(filters=[
            and_(
                self.model.id == schedule_history_id,
                self.model.responsible_id == userRDTO.id,
                self.model.operation_id == TableConstantsNames.InitialWeightOperationId,
                self.model.is_passed == None
            )
        ])

        if schedule_history is None:
            raise AppExceptionResponse.bad_request("Этап расписания не найдено")

        schedule = await scheduleRepo.get(id=schedule_history.schedule_id)
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")

        vehicle = await vehicleRepo.get(id=schedule.vehicle_id)
        vehicle_info = get_vehicle_information(vehicle)
        if vehicle is None:
            raise AppExceptionResponse.bad_request("Транспорт не найден")

        trailer_id = None
        trailer_info = None
        if schedule.trailer_id is not None:
            trailer = await vehicleRepo.get(id=schedule.trailer_id)
            if trailer is None:
                raise AppExceptionResponse.bad_request("Прицеп не найден")
            trailer_id = trailer.id
            trailer_info = get_vehicle_information(trailer)

        schedule_history_dto = ScheduleHistoryCDTO.from_orm(schedule_history)
        schedule_dto = ScheduleCDTO.from_orm(schedule)

        current_time = datetime.now()

        if not dto.is_passed:
            schedule_dto.is_active = False
            schedule_dto.is_canceled = True
            schedule_dto.canceled_at = current_time
            schedule_dto.canceled_by = userRDTO.id
            schedule_dto.cancel_reason = dto.cancel_reason

            schedule_history_dto.is_passed = False
            schedule_history_dto.cancel_reason = dto.cancel_reason
            schedule_history_dto.canceled_at = current_time
            schedule_history_dto.end_at = current_time

        else:
            initial_weight_dto = InitialWeightCDTO(
                history_id=schedule_history.id,
                order_id = schedule.order_id,
                zakaz = schedule.zakaz,
                vehicle_id = schedule.vehicle_id,
                vehicle_info = vehicle_info,
                trailer_id = trailer_id,
                trailer_info = trailer_info,
                responsible_id = userRDTO.id,
                responsible_name = userRDTO.name,
                responsible_iin = userRDTO.iin,
                vehicle_tara_kg = dto.vehicle_tara_kg,
                measured_at = current_time
            )
            schedule_history_new = ScheduleHistoryModel(
                schedule_id=schedule.id,
                operation_id=TableConstantsNames.LoadingEntryOperationId,
            )
            await initialWeightRepo.create(obj=InitialWeightModel(**initial_weight_dto.dict()))
            await scheduleRepo.create(obj=schedule_history_new)

            schedule_dto.vehicle_tara_kg = dto.vehicle_tara_kg
            schedule_dto.current_operation_id = TableConstantsNames.LoadingEntryOperationId

            schedule_history_dto.is_passed = True
            schedule_history_dto.end_at = current_time
        await self.update(obj=schedule, dto=schedule_dto)
        order = await orderRepo.get(id=schedule.order_id)
        if order is not None:
            await scheduleRepo.calculate_order(order=order, orderRepo=orderRepo)
        return await self.update(obj=schedule_history, dto=schedule_history_dto)

    #Весовщик первичное


    #Проверка на погрузке
    async def process_kpp_loading_request(self,
                            schedule_id,
                            userRDTO:UserRDTOWithRelations,
                            scheduleRepo:ScheduleRepository,
                            ):
        schedule = await scheduleRepo.get_first_with_filter(filters=[
            and_(
                ScheduleModel.id == schedule_id,
                ScheduleModel.is_active == True,
                ScheduleModel.current_operation_id == TableConstantsNames.LoadingEntryOperationId
            )
        ])
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        schedule_history = await self.get_first_with_filters(
            filters=[{"schedule_id": schedule_id}, {"operation_id": TableConstantsNames.LoadingEntryOperationId}])
        if schedule_history is None:
            schedule_history = ScheduleHistoryModel(
                schedule_id=schedule.id,
                operation_id=TableConstantsNames.LoadingEntryOperationId,
            )
            schedule_history = await self.create(obj=schedule_history)
        if schedule_history.responsible_id is not None:
            raise AppExceptionResponse.bad_request("Заявка уже принята в обработку")
        schedule_history_dto = ScheduleHistoryCDTO.from_orm(schedule_history)
        schedule_history_dto.responsible_id = userRDTO.id
        schedule_history_dto.responsible_name = userRDTO.name
        schedule_history_dto.responsible_iin = userRDTO.iin
        schedule_history_dto.start_at = datetime.now()
        return await self.update(obj=schedule_history, dto=schedule_history_dto)


    async def confirm_or_deny_loading_entry(self,
                            schedule_history_id,
                            answer:ScheduleHistoryEnterFactoryDTO,
                            userRDTO:UserRDTOWithRelations,
                            scheduleRepo:ScheduleRepository,
                            orderRepo:OrderRepository
                            ):
        schedule_history = await self.get_first_with_filter(filters=[
            and_(
                self.model.id == schedule_history_id,
                self.model.responsible_id == userRDTO.id,
                self.model.is_passed == None
            )
        ])
        if schedule_history is None:
            raise AppExceptionResponse.bad_request("Этап не найден")
        schedule:ScheduleModel = await scheduleRepo.get(id=schedule_history.schedule_id)
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        schedule_dto = ScheduleCDTO.from_orm(schedule)
        schedule_history_dto = ScheduleHistoryCDTO.from_orm(schedule_history)
        schedule_history_dto.is_passed = answer.is_passed
        schedule_history_dto.cancel_reason = answer.cancel_reason
        schedule_history_dto.end_at = datetime.now()
        if not answer.is_passed:
            schedule_history_dto.canceled_at = datetime.now()
            schedule_dto.is_active = False
            schedule_dto.is_canceled = True
            schedule_dto.cancel_reason = answer.cancel_reason
            schedule_dto.canceled_by = userRDTO.id
        else:
            schedule_dto.current_operation_id = TableConstantsNames.LoadingOperationId
            schedule_dto.is_used = True
            new_schedule_history_model = ScheduleHistoryModel(
                schedule_id=schedule.id,
                operation_id=TableConstantsNames.InitialWeightOperationId,
            )
            await self.create(obj=new_schedule_history_model)

        await scheduleRepo.update(obj=schedule,dto=schedule_dto)
        order = await orderRepo.get(id=schedule.order_id)
        if order is not None:
            await scheduleRepo.calculate_order(order=order, orderRepo=orderRepo)
        return await self.update(obj=schedule_history,dto=schedule_history_dto)
    #Проверка на погрузке

    #Погрузка
    async def accept_loading_request(self,
                            schedule_id,
                            userRDTO:UserRDTOWithRelations,
                            scheduleRepo:ScheduleRepository,
                            ):
        schedule = await scheduleRepo.get_first_with_filter(filters=[
            and_(
                ScheduleModel.id == schedule_id,
                ScheduleModel.is_active == True,
                ScheduleModel.current_operation_id == TableConstantsNames.LoadingOperationId
            )
        ])
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        schedule_history = await self.get_first_with_filters(
            filters=[{"schedule_id": schedule_id}, {"operation_id": TableConstantsNames.LoadingOperationId}])
        if schedule_history is None:
            schedule_history = ScheduleHistoryModel(
                schedule_id=schedule.id,
                operation_id=TableConstantsNames.LoadingOperationId,
            )
            schedule_history = await self.create(obj=schedule_history)
        if schedule_history.responsible_id is not None:
            raise AppExceptionResponse.bad_request("Заявка уже принята в обработку")
        schedule_history_dto = ScheduleHistoryCDTO.from_orm(schedule_history)
        schedule_history_dto.responsible_id = userRDTO.id
        schedule_history_dto.responsible_name = userRDTO.name
        schedule_history_dto.responsible_iin = userRDTO.iin
        schedule_history_dto.start_at = datetime.now()
        return await self.update(obj=schedule_history, dto=schedule_history_dto)

    async def confirm_or_deny_loading(self,
                            schedule_history_id,
                            answer:ScheduleHistoryEnterFactoryDTO,
                            userRDTO:UserRDTOWithRelations,
                            scheduleRepo:ScheduleRepository,
                            orderRepo:OrderRepository
                            ):
        schedule_history = await self.get_first_with_filter(filters=[
            and_(
                self.model.id == schedule_history_id,
                self.model.responsible_id == userRDTO.id,
                self.model.is_passed == None
            )
        ])
        if schedule_history is None:
            raise AppExceptionResponse.bad_request("Этап не найден")
        schedule:ScheduleModel = await scheduleRepo.get(id=schedule_history.schedule_id)
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        schedule_dto = ScheduleCDTO.from_orm(schedule)
        schedule_history_dto = ScheduleHistoryCDTO.from_orm(schedule_history)
        schedule_history_dto.is_passed = answer.is_passed
        schedule_history_dto.cancel_reason = answer.cancel_reason
        schedule_history_dto.end_at = datetime.now()
        if not answer.is_passed:
            schedule_history_dto.canceled_at = datetime.now()
            schedule_dto.is_active = False
            schedule_dto.is_canceled = True
            schedule_dto.cancel_reason = answer.cancel_reason
            schedule_dto.canceled_by = userRDTO.id
        else:
            schedule_dto.current_operation_id = TableConstantsNames.FinalWeightOperationId
            schedule_dto.is_used = True
            new_schedule_history_model = ScheduleHistoryModel(
                schedule_id=schedule.id,
                operation_id=TableConstantsNames.FinalWeightOperationId,
            )
            await self.create(obj=new_schedule_history_model)

        await scheduleRepo.update(obj=schedule,dto=schedule_dto)
        order = await orderRepo.get(id=schedule.order_id)
        if order is not None:
            await scheduleRepo.calculate_order(order=order, orderRepo=orderRepo)
        return await self.update(obj=schedule_history,dto=schedule_history_dto)

    #Погрузка





