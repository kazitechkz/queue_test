import datetime

from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.workshop_schedule_model import WorkshopScheduleModel


class WorkshopScheduleRepository(BaseRepository[WorkshopScheduleModel]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(WorkshopScheduleModel, db)


    async def get_active(self,workshop_sap_id:str,schedule_date:datetime.date = datetime.date.today()):
        return await self.get_first_with_filter(filters=[
            and_(
                self.model.date_start <= schedule_date,
                self.model.date_end >= schedule_date,
                self.model.is_active == True,
                self.model.workshop_sap_id == workshop_sap_id
            )
        ])


    async def get_schedule(self,workshop_sap_id:str,schedule_date:datetime.date):
        active_schedule = await self.get_active(workshop_sap_id=workshop_sap_id)
        if active_schedule is None:
            raise AppExceptionResponse.not_found("Активное расписание не найдено")
        schedule = []
        # Преобразуем start_time, end_time и current_time в datetime для удобной работы
        current_time_dt = datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.now().time())
        start_time_dt = datetime.datetime.combine(datetime.datetime.today(), active_schedule.start_at)
        end_time_dt = datetime.datetime.combine(datetime.datetime.today(), active_schedule.end_at)

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
                adjusted_start_time = start_time_dt + datetime.timedelta(
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
            service_end_time = current_time_dt + datetime.timedelta(minutes=active_schedule.car_service_min)

            if service_end_time.time() > active_schedule.end_at:
                break

            # Добавляем в расписание интервал работы
            schedule.append(f"{current_time_dt.time()} - {service_end_time.time()}")

            # Добавляем перерыв
            current_time_dt = service_end_time + datetime.timedelta(minutes=active_schedule.break_between_service_min)

        return schedule