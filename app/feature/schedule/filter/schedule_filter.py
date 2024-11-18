from typing import Optional

from fastapi import Query
from sqlalchemy import or_, and_
from datetime import datetime, date, time, timedelta

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_filter import BaseFilter
from app.domain.models.order_model import OrderModel
from app.domain.models.schedule_model import ScheduleModel
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class ScheduleFilter(BaseFilter):
    def __init__(self,
                 per_page: int = Query(default=20, gt=0, example=20, description="Количество элементов на страницу"),
                 page: int = Query(default=1, ge=1, example=1, description="Номер страницы"),
                 search: Optional[str] = Query(default=None, max_length=255, min_length=3,
                                               description="Поисковый запрос по заказу, владельцу, иину владельца, имени водителя, иину водителя,"
                                                           "полным наименованием организации, бин организации,"
                                                           "инофрмации транспорту или прицепу, "
                                                           "причинам отказа и отвественному лицу"),
                 start_at: Optional[date] = Query(default=None, description="Начать искать с"),
                 end_at: Optional[date] = Query(default=None, description="Начать искать до"),
                 is_active: Optional[bool] = Query(default=None, description="Заказ активен?"),
                 is_used: Optional[bool] = Query(default=None, description="Находится ли он на территории?"),
                 is_canceled: Optional[bool] = Query(default=None, description="Отменен ли?"),
                 is_executed: Optional[bool] = Query(default=None, description="Успешно ли завершен?"),
                 ):
        super().__init__(per_page, page, search)
        self.per_page = per_page
        self.page = page
        self.search = search
        self.start_at = start_at
        self.end_at = end_at
        self.is_active = is_active
        self.is_used = is_used
        self.is_canceled = is_canceled
        self.is_executed = is_executed
        self.model = ScheduleModel

    def apply(self) -> list:
        filters = []
        if self.search:
            filters.append(or_(
                self.model.zakaz.like(f"%{self.search}%"),
                self.model.owner_name.like(f"%{self.search}%"),
                self.model.owner_iin.like(f"%{self.search}%"),
                self.model.driver_name.like(f"%{self.search}%"),
                self.model.driver_iin.like(f"%{self.search}%"),
                self.model.organization_full_name.like(f"%{self.search}%"),
                self.model.organization_bin.like(f"%{self.search}%"),
                self.model.vehicle_info.like(f"%{self.search}%"),
                self.model.trailer_info.like(f"%{self.search}%"),
                self.model.responsible_name.like(f"%{self.search}%"),
                self.model.cancel_reason.like(f"%{self.search}%"),
            )
            )
        if self.start_at != None:
            start_at = datetime.combine(self.start_at, time(0, 0, 0))
            filters.append(and_(self.model.start_at >= start_at))
        if self.end_at != None:
            end_at = datetime.combine(self.end_at, time(23, 59, 59))
            filters.append(and_(self.model.start_at <= end_at))

        if self.is_active != None:
            filters.append(and_(self.model.is_active == self.is_active))

        if self.is_used != None:
            filters.append(and_(self.model.is_used == self.is_used))

        if self.is_canceled != None:
            filters.append(and_(self.model.is_canceled == self.is_canceled))

        if self.is_executed != None:
            filters.append(and_(self.model.is_executed == self.is_executed))

        return filters


class ScheduleClientScheduledFilter():
    def __init__(self,
                 scheduled_at: date = Query(description="Поиск в день"),
                 order_id: Optional[int] = Query(default=None, description="Идентификатор заказа")
                 ):
        self.scheduled_at = scheduled_at
        self.order_id = order_id
        self.model = ScheduleModel

    def apply(self, userRDTO: UserRDTOWithRelations) -> list:
        filters = []
        start_at = datetime.combine(self.scheduled_at, time(0, 0, 0))
        end_at = datetime.combine(self.scheduled_at, time(23, 59, 59))
        filters.append(and_(self.model.start_at <= end_at, self.model.start_at >= start_at))
        if userRDTO.user_type.value == TableConstantsNames.UserLegalTypeValue:
            organization_ids = [organization.id for organization in userRDTO.organizations]
            filters.append(and_(self.model.organization_id.in_(organization_ids)))
        else:
            filters.append(and_(or_(self.model.owner_id == userRDTO.id, self.model.driver_id == userRDTO.id)))

        if self.order_id is not None:
            filters.append(and_(self.model.order_id == self.order_id))

        return filters


class ScheduleClientFromToFilter:
    def __init__(self,
                 start_at: date = Query(default=date.today(), description="Начать искать с"),
                 end_at: date = Query(default=date.today(), description="Начать искать до"),
                 order_id: Optional[int] = Query(default=None, description="Идентификатор заказа")
                 ):
        self.start_at = start_at
        self.end_at = end_at
        self.order_id = order_id

        self.model = ScheduleModel

    def apply(self) -> list:
        if self.start_at >= self.end_at:
            raise AppExceptionResponse.bad_request("Дата начала должна быть больше даты конца")
        date_list = []
        start_date = datetime.combine(self.start_at, time(0, 0, 0))
        end_date = datetime.combine(self.end_at, time(0, 0, 0))
        current_date = start_date
        while current_date <= end_date:
            date_list.append((current_date,
                              datetime.combine(date(current_date.year, current_date.month, current_date.day),
                                               time(23, 59, 59))))
            current_date += timedelta(days=1)

        return date_list
