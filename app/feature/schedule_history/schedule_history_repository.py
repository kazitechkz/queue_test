import datetime

from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.schedule_history_model import ScheduleHistoryModel
from app.domain.models.schedule_model import ScheduleModel
from app.feature.operation.operation_repository import OperationRepository
from app.feature.order.order_repository import OrderRepository
from app.feature.schedule.dtos.schedule_dto import ScheduleCDTO, ScheduleRDTO
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryEnterFactoryDTO, ScheduleHistoryCDTO
from app.feature.user.dtos.user_dto import UserRDTOWithRelations
from app.shared.database_constants import TableConstantsNames


class ScheduleHistoryRepository(BaseRepository[ScheduleHistoryModel]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(ScheduleHistoryModel, db)

    async def enter_factory_take_request(self,
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

    async def enter_factory_pass_request(self,
                            schedule_history_id,
                            answer:ScheduleHistoryEnterFactoryDTO,
                            userRDTO:UserRDTOWithRelations,
                            scheduleRepo:ScheduleRepository,
                            orderRepo:OrderRepository
                            ):
        schedule_history = await self.get_first_with_filter(filters=[
            and_(
                self.model.id == schedule_history_id,
                self.model.responsible_id <= userRDTO.id,
                self.model.is_passed == None
            )
        ])
        if schedule_history is None:
            raise AppExceptionResponse.bad_request("Этап не найден")
        schedule:ScheduleModel = await scheduleRepo.get(id=schedule_history.schedule_id)
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        schedule_dto:ScheduleCDTO = ScheduleRDTO.from_orm(schedule)
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
            schedule_dto.current_operation_id = 2
            schedule_dto.is_used = True
            schedule_history_model = ScheduleHistoryModel(
                schedule_id=schedule.id,
                operation_id=TableConstantsNames.InitialWeightOperationId,
            )
            await scheduleRepo.create(obj=schedule_history)
        order = await orderRepo.get(id=schedule.order_id)
        await scheduleRepo.update(obj=schedule,dto=schedule_dto)
        await scheduleRepo.calculate_order(order=order,orderRepo=orderRepo)
        return await self.update(obj=schedule_history,dto=schedule_history_dto)

