from typing import Optional, List

from fastapi import Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime

from starlette import status

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.core.schedule_core import get_vehicle_information
from app.domain.models.act_weight_model import ActWeightModel
from app.domain.models.baseline_weights_model import BaselineWeightModel
from app.domain.models.initial_weight_model import InitialWeightModel
from app.domain.models.order_model import OrderModel
from app.domain.models.schedule_history_model import ScheduleHistoryModel
from app.domain.models.schedule_model import ScheduleModel
from app.feature.act_weight.act_weight_repository import ActWeightRepository
from app.feature.act_weight.dtos.act_weight_dto import ActWeightCDTO
from app.feature.baseline_weight.baseline_weight_repository import BaselineWeightRepository
from app.feature.baseline_weight.dtos.baseline_weight_dto import BaselineWeightCDTO
from app.feature.initial_weight.dtos.initial_weight_dto import InitialWeightCDTO
from app.feature.initial_weight.initial_weight_repository import InitialWeightRepository
from app.feature.operation.operation_repository import OperationRepository
from app.feature.order.order_repository import OrderRepository
from app.feature.schedule.dtos.schedule_dto import ScheduleCDTO, ScheduleRDTO
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.schedule_history.dtos.schedule_history_dto import ScheduleHistoryAnswerDTO, ScheduleHistoryCDTO
from app.feature.user.user_repository import UserRepository
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class ScheduleHistoryRepository(BaseRepository[ScheduleHistoryModel]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(ScheduleHistoryModel, db)

    # Получить заявку
    async def take_request(
            self, schedule_id,
            userRDTO: UserRDTOWithRelations,
            scheduleRepo: ScheduleRepository,
            operationRepo: OperationRepository,
    ):
        schedule = await scheduleRepo.get_first_with_filter(filters=[
            and_(
                ScheduleModel.id == schedule_id,
                ScheduleModel.is_active == True,
            )
        ])
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")
        if schedule.responsible_id is not None:
            raise AppExceptionResponse.bad_request(
                f"Расписание уже взято в обработку сотрудником: {schedule.responsible_name}")

        operation = await operationRepo.get(id=schedule.current_operation_id)
        if operation is None:
            raise AppExceptionResponse.bad_request("Этап не найден")

        if userRDTO.role.value != operation.role_value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Отказано в доступе",
            )
        schedule_history = await self.get_first_with_filters(
            filters=[{"schedule_id": schedule_id}, {"operation_id": operation.id}])
        if schedule_history is not None:
            if schedule_history.responsible_id is not None:
                return schedule_history

        if operation.value == TableConstantsNames.EntryOperationName:
            if schedule.rescheduled_start_at == None or schedule.rescheduled_end_at == None:
                if (schedule.start_at > datetime.now() or schedule.end_at < datetime.now()):
                    raise AppExceptionResponse.bad_request("Нельзя заявиться на текущее расписание")
            else:
                if (schedule.rescheduled_start_at > datetime.now() or schedule.rescheduled_end_at < datetime.now()):
                    raise AppExceptionResponse.bad_request("Нельзя заявиться на текущее расписание")

        return await self._take_responisbibility(
            schedule=schedule,
            operation_id=operation.id,
            userRDTO=userRDTO,
            scheduleRepo=scheduleRepo,
            schedule_history_model=schedule_history)

    async def accept_or_cancel(
            self,
            schedule_id: int,
            dto: ScheduleHistoryAnswerDTO,
            userRDTO: UserRDTOWithRelations,
            userRepo: UserRepository,
            scheduleRepo: ScheduleRepository,
            initialWeightRepo: InitialWeightRepository,
            actWeightRepo: ActWeightRepository,
            orderRepo: OrderRepository,
            operationRepo: OperationRepository,
            baseLineWeightRepo: BaselineWeightRepository
    ):

        schedule = await scheduleRepo.get_first_with_filter(filters=[
            and_(
                ScheduleModel.id == schedule_id,
                ScheduleModel.is_active == True,
                ScheduleModel.responsible_id != None
            )
        ])
        if schedule is None:
            raise AppExceptionResponse.bad_request("Расписание не найдено")

        operation = await operationRepo.get(id=schedule.current_operation_id)
        if operation is None:
            raise AppExceptionResponse.bad_request("Этап не найден")
        if operation.value != dto.operation_value:
            raise AppExceptionResponse.bad_request("Код операции не совпадает")
        if userRDTO.role.value != operation.role_value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Отказано в доступе",
            )
        schedule_history = await self.get_first_with_filter(filters=[
            and_(
                self.model.schedule_id == schedule_id,
                self.model.responsible_id == userRDTO.id,
                self.model.operation_id == operation.id,
                self.model.is_passed == None
            )
        ])
        if schedule_history is None:
            raise AppExceptionResponse.bad_request("Этап расписания не найден или уже принят")

        if (
                not dto.is_passed or operation.value == TableConstantsNames.ReLoadingExitOperationName) and operation.value not in [
            TableConstantsNames.FinalWeightOperationName, TableConstantsNames.ReLoadingEntryExitOperationName,
            TableConstantsNames.ReLoadingEntryWeightOperationName, TableConstantsNames.ReLoadingWeightOperationName]:
            return await self._cancel_schedule(
                cancel_reason=dto.cancel_reason,
                userDTO=userRDTO,
                schedule=schedule,
                scheduleHistory=schedule_history,
                scheduleRepo=scheduleRepo,
                orderRepo=orderRepo,
            )
        else:
            vehicle_tara_kg = None
            vehicle_brutto_kg = None
            is_passed = dto.is_passed
            next_id = operation.next_id
            total_weight = (dto.vehicle_tara_kg or 0) + (dto.trailer_tara_kg or 0)
            print(f"total_weight: {total_weight}")
            if not dto.is_passed:
                if operation.value == TableConstantsNames.FinalWeightOperationName:
                    next_operation = await operationRepo.get_filtered(filters={"value": dto.next_operation_value})
                    if next_operation is None:
                        raise AppExceptionResponse.bad_request("Этап не найден")
                    next_id = next_operation.id
                if operation.value == TableConstantsNames.ExitCheckOperationName:
                    next_operation = await operationRepo.get_filtered(
                        filters={"value": TableConstantsNames.ReLoadingEntryExitOperationName})
                    if next_operation is None:
                        raise AppExceptionResponse.bad_request("Этап не найден")
                    next_id = next_operation.id
            is_last = False
            if operation.value == TableConstantsNames.InitialWeightOperationName:
                if dto.vehicle_id is not None:
                    await self._create_base_line_weight(
                        schedule=schedule,
                        repo=baseLineWeightRepo,
                        tara_weight=dto.vehicle_tara_kg
                    )
                if dto.trailer_id is not None:
                    await self._create_base_line_weight(
                        schedule=schedule,
                        repo=baseLineWeightRepo,
                        tara_weight=dto.trailer_tara_kg,
                        is_trailer=True
                    )
                await self._create_initial_weight_schedule(
                    schedule=schedule,
                    schedule_history=schedule_history,
                    initialWeightRepo=initialWeightRepo,
                    userRDTO=userRDTO,
                    vehicle_tara_kg=total_weight,
                )
            if operation.value == TableConstantsNames.FinalWeightOperationName and is_passed:
                vehicle_brutto_kg = dto.vehicle_brutto_kg
                actual_weight = vehicle_brutto_kg - schedule.vehicle_tara_kg
                if actual_weight > schedule.loading_volume_kg:
                    raise AppExceptionResponse.bad_request("Вес превышает указанный объем загрузки")
                await self._create_act_weight_schedule(
                    schedule=schedule,
                    schedule_history=schedule_history,
                    actWeightRepo=actWeightRepo,
                    userRDTO=userRDTO,
                    vehicle_brutto_kg=vehicle_brutto_kg)
            if operation.value == TableConstantsNames.ExitCheckOperationName and is_passed:
                is_last = True
            results = await self._accept_and_create_next_schedule_base(
                schedule=schedule,
                scheduleHistory=schedule_history,
                scheduleRepo=scheduleRepo,
                orderRepo=orderRepo,
                next_operation_id=next_id,
                userRDTO=userRDTO,
                is_last=is_last,
                is_passed=is_passed,
                vehicle_tara_kg=total_weight,
                vehicle_brutto_kg=vehicle_brutto_kg,
            )
            # Автоматически создает первичное взвешивание если есть
            if operation.value == TableConstantsNames.EntryOperationName:
                veh_ids = [schedule.vehicle_id] + ([schedule.trailer_id] if schedule.trailer_id is not None else [])
                baseline_total_weight = await self._check_base_line_weight(ids=veh_ids, repo=baseLineWeightRepo)
                if baseline_total_weight is not None:
                    next_schedule_history = results[-1]
                    if next_schedule_history is not None:
                        digitalUserRDTO = await userRepo.get_admin()
                        next_schedule_history = await self._take_responisbibility(
                            schedule=schedule,
                            operation_id=next_schedule_history.operation_id,
                            userRDTO=digitalUserRDTO,
                            scheduleRepo=scheduleRepo,
                            schedule_history_model=next_schedule_history
                        )
                        await self._create_initial_weight_schedule(
                            schedule=schedule,
                            schedule_history=next_schedule_history,
                            initialWeightRepo=initialWeightRepo,
                            userRDTO=digitalUserRDTO,
                            vehicle_tara_kg=baseline_total_weight,
                        )
                        schedule = await scheduleRepo.get_first_with_filter(filters=[
                            and_(
                                ScheduleModel.id == schedule_id,
                                ScheduleModel.is_active == True,
                                ScheduleModel.responsible_id != None
                            )
                        ])
                        await self._accept_and_create_next_schedule_base(
                            schedule=schedule,
                            scheduleHistory=next_schedule_history,
                            scheduleRepo=scheduleRepo,
                            orderRepo=orderRepo,
                            next_operation_id=TableConstantsNames.LoadingEntryOperationId,
                            userRDTO=digitalUserRDTO,
                            is_last=False,
                            is_passed=True,
                            vehicle_tara_kg=baseline_total_weight,
                            vehicle_brutto_kg=vehicle_brutto_kg,
                        )

            return results[0]

    async def _take_responisbibility(
            self,
            schedule: ScheduleModel,
            operation_id: int,
            userRDTO: UserRDTOWithRelations,
            scheduleRepo: ScheduleRepository,
            schedule_history_model: Optional[ScheduleHistoryModel] = None,
    ) -> ScheduleHistoryModel:
        current_datetime = datetime.now()
        if schedule_history_model is None:
            schedule_history_model = ScheduleHistoryModel(
                schedule_id=schedule.id,
                operation_id=operation_id,
            )
            schedule_history_model = await self.create(obj=schedule_history_model)
        schedule_history_dto = ScheduleHistoryCDTO.from_orm(schedule_history_model)
        schedule_history_dto.responsible_id = userRDTO.id
        schedule_history_dto.responsible_name = userRDTO.name
        schedule_history_dto.responsible_iin = userRDTO.iin
        schedule_history_dto.start_at = current_datetime
        # Меняем расписание
        schedule_dto = ScheduleCDTO.from_orm(schedule)
        schedule_dto.responsible_id = userRDTO.id
        schedule_dto.responsible_name = userRDTO.name
        await scheduleRepo.update(obj=schedule, dto=schedule_dto)
        # Сохраняняем историю вьезда и отправляем фронту
        return await self.update(obj=schedule_history_model, dto=schedule_history_dto)

    async def _cancel_schedule(
            self,
            cancel_reason: Optional[str],
            userDTO: UserRDTOWithRelations,
            schedule: ScheduleModel,
            scheduleHistory: ScheduleHistoryModel,
            scheduleRepo: ScheduleRepository,
            orderRepo: OrderRepository,
    ) -> ScheduleHistoryModel:
        # Меняем Расписание и отменяем
        schedule_dto = ScheduleCDTO.from_orm(schedule)
        schedule_history_dto = ScheduleHistoryCDTO.from_orm(scheduleHistory)
        current_datetime = datetime.now()
        # Отменяем состояние Расписания
        schedule_dto.canceled_at = current_datetime
        schedule_dto.canceled_by = userDTO.id
        schedule_dto.cancel_reason = cancel_reason
        schedule_dto.is_active = False
        schedule_dto.is_used = False
        schedule_dto.is_executed = False
        schedule_dto.is_canceled = True
        # Отменяем историю расписания
        schedule_history_dto.cancel_reason = cancel_reason
        schedule_history_dto.canceled_at = current_datetime
        schedule_history_dto.end_at = current_datetime
        schedule_history_dto.is_passed = False
        # Обновляем расписание и историю расписания
        await scheduleRepo.update(obj=schedule, dto=schedule_dto)
        # Пересчитаем заказ
        order = await orderRepo.get(id=schedule.order_id)
        if order is not None:
            await scheduleRepo.calculate_order(order=order, orderRepo=orderRepo)
        # Сохраняем информацию о изменении в истории расписания
        return await self.update(obj=scheduleHistory, dto=schedule_history_dto)

    async def _accept_and_create_next_schedule_base(
            self,
            schedule: ScheduleModel,
            scheduleHistory: ScheduleHistoryModel,
            scheduleRepo: ScheduleRepository,
            orderRepo: OrderRepository,
            is_last: bool,
            is_passed: bool,
            userRDTO: UserRDTOWithRelations,
            next_operation_id: Optional[int] = None,
            vehicle_tara_kg: Optional[int] = None,
            vehicle_brutto_kg: Optional[int] = None,
    ) -> List[ScheduleHistoryModel]:
        results = []
        new_schedule_history = None
        # Меняем Расписание и принимаем
        schedule_dto = ScheduleCDTO.from_orm(schedule)
        schedule_history_dto = ScheduleHistoryCDTO.from_orm(scheduleHistory)
        current_datetime = datetime.now()
        # Принимаем состояния Расписания
        schedule_history_dto.is_passed = True
        schedule_history_dto.end_at = current_datetime
        # Меняем schedule
        if next_operation_id is not None:
            schedule_dto.current_operation_id = next_operation_id
            schedule_dto.is_used = True
            schedule_dto.responsible_id = None
            schedule_dto.responsible_name = None
            if vehicle_tara_kg is not None and vehicle_tara_kg > 0:
                schedule_dto.vehicle_tara_kg = vehicle_tara_kg
            if vehicle_brutto_kg is not None:
                schedule_dto.vehicle_brutto_kg = vehicle_brutto_kg
            if is_last:
                schedule_dto.is_active = False
                schedule_dto.is_used = False
                schedule_dto.is_executed = True
                schedule_dto.executed_at = current_datetime
                new_schedule_history_dto = ScheduleHistoryModel(
                    schedule_id=schedule.id,
                    operation_id=next_operation_id,
                    responsible_id=userRDTO.id,
                    responsible_name=userRDTO.name,
                    responsible_iin=userRDTO.iin,
                    is_passed=is_passed,
                    start_at=current_datetime,
                    end_at=current_datetime
                )
            else:
                new_schedule_history_dto = ScheduleHistoryModel(
                    schedule_id=schedule.id,
                    operation_id=next_operation_id
                )
                # Пересчитаем заказ
            new_schedule_history = await self.create(obj=new_schedule_history_dto)
            await scheduleRepo.update(obj=schedule, dto=schedule_dto)
            order = await orderRepo.get(id=schedule.order_id)
            if order is not None:
                await scheduleRepo.calculate_order(order=order, orderRepo=orderRepo)
        old_schedule_history = await self.update(obj=scheduleHistory, dto=schedule_history_dto)
        results.append(old_schedule_history)
        if new_schedule_history is not None:
            results.append(new_schedule_history)
        return results

    async def _create_base_line_weight(self,
                                       repo: BaselineWeightRepository,
                                       schedule: ScheduleModel,
                                       tara_weight: int,
                                       is_trailer: bool = False
                                       ):
        car_id = schedule.vehicle_id
        car_info = schedule.vehicle_info
        if is_trailer is True:
            car_id = schedule.trailer_id
            car_info = schedule.trailer_info
        base_weight_dto = BaselineWeightCDTO(
            vehicle_id=car_id,
            vehicle_info=car_info,
            vehicle_tara_kg=tara_weight,
            measured_at=datetime.now()
        )
        model = await repo.get_with_filter(
            filters=[and_(repo.model.vehicle_id == car_id)]
        )
        if model is None:
            return await repo.create(obj=BaselineWeightModel(**base_weight_dto.dict()))
        if model.vehicle_tara_kg != tara_weight:
            return await repo.update(obj=model, dto=base_weight_dto)

    async def _create_initial_weight_schedule(
            self,
            schedule: ScheduleModel,
            schedule_history: ScheduleHistoryModel,
            initialWeightRepo: InitialWeightRepository,
            userRDTO: UserRDTOWithRelations,
            vehicle_tara_kg: int,
    ) -> InitialWeightModel:

        current_time = datetime.now()
        initial_weight_dto = InitialWeightCDTO(
            history_id=schedule_history.id,
            order_id=schedule.order_id,
            zakaz=schedule.zakaz,
            vehicle_id=schedule.vehicle_id,
            vehicle_info=schedule.vehicle_info,
            trailer_id=schedule.trailer_id,
            trailer_info=schedule.trailer_info,
            responsible_id=userRDTO.id,
            responsible_name=userRDTO.name,
            responsible_iin=userRDTO.iin,
            vehicle_tara_kg=vehicle_tara_kg,
            measured_at=current_time
        )
        return await initialWeightRepo.create(obj=InitialWeightModel(**initial_weight_dto.dict()))

    async def _create_act_weight_schedule(
            self,
            schedule: ScheduleModel,
            schedule_history: ScheduleHistoryModel,
            actWeightRepo: ActWeightRepository,
            userRDTO: UserRDTOWithRelations,
            vehicle_brutto_kg: int,
    ) -> ActWeightModel:
        current_time = datetime.now()
        act_weight_dto = ActWeightCDTO(
            history_id=schedule_history.id,
            order_id=schedule.order_id,
            zakaz=schedule.zakaz,
            vehicle_id=schedule.vehicle_id,
            vehicle_info=schedule.vehicle_info,
            trailer_id=schedule.trailer_id,
            trailer_info=schedule.trailer_info,
            responsible_id=userRDTO.id,
            responsible_name=userRDTO.name,
            responsible_iin=userRDTO.iin,
            vehicle_brutto_kg=vehicle_brutto_kg,
            vehicle_tara_kg=schedule.vehicle_tara_kg,
            measured_at=current_time
        )
        return await actWeightRepo.create(obj=ActWeightModel(**act_weight_dto.dict()))

    async def _check_base_line_weight(
            self,
            ids: List[int],
            repo: BaselineWeightRepository,
    ):
        # Получение всех базовых весов для указанных ids
        base_line_weights = await repo.get_vehicle_trailer_weights(ids=ids)

        # Если base_line_weights пуст, возвращаем None
        if not base_line_weights:
            return None

        # Извлекаем все vehicle_id из base_line_weights
        available_ids = {base_line_weight.vehicle_id for base_line_weight in base_line_weights}

        # Проверяем, содержатся ли все элементы из ids в available_ids
        if not set(ids).issubset(available_ids):
            return None

        # Вычисляем общий вес
        total_weight = sum(base_line_weight.vehicle_tara_kg for base_line_weight in base_line_weights)

        return total_weight
