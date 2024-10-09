from datetime import datetime,date
from typing import Optional

from fastapi import Query
from sqlalchemy import or_, and_

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_filter import BaseFilter
from app.domain.models.act_weight_model import ActWeightModel


class ActWeightFilter(BaseFilter):
    def __init__(self,
                 per_page: int = Query(default=20, gt=0, example=20, description="Количество элементов на страницу"),
                 page: int = Query(default=1, ge=1, example=1, description="Номер страницы"),
                 search: Optional[str] = Query(default=None, max_length=255, min_length=3,
                                               description="Поисковый запрос по номеру заказа, информации о транспорте или прицепу,"
                                                           "имени, иину ответственного, по весу тары, брутто или нетто"),
                 vehicle_id: Optional[int] = Query(default=None, description="Идентификатор транспорта"),
                 trailer_id: Optional[int] = Query(default=None, description="Идентификатор прицепа"),
                 history_id: Optional[int] = Query(default=None, description="Идентификатор истории"),
                 order_id: Optional[int] = Query(default=None, description="Идентификатор заказа"),
                 start_at:Optional[date] = Query(default=None,description="Период с",lt=date.today()),
                 end_at:Optional[date] = Query(default=None,description="Период до",le=date.today()),
                 ):
        super().__init__(per_page, page, search)
        self.per_page = per_page
        self.page = page
        self.search = search
        self.vehicle_id = vehicle_id
        self.trailer_id = trailer_id
        self.history_id = history_id
        self.order_id = order_id
        self.start_at = start_at
        self.end_at = end_at
        self.model = ActWeightModel

    def apply(self) -> list:
        filters = []
        if self.search:
            filters.append(or_(
                self.model.zakaz.like(f"%{self.search}%"),
                self.model.vehicle_info.like(f"%{self.search}%"),
                self.model.trailer_info.like(f"%{self.search}%"),
                self.model.responsible_name.like(f"%{self.search}%"),
                self.model.responsible_iin.like(f"%{self.search}%"),
                self.model.vehicle_tara_kg.like(f"%{self.search}%"),
                self.model.vehicle_netto_kg.like(f"%{self.search}%"),
                self.model.vehicle_brutto_kg.like(f"%{self.search}%"),
            )
            )

        if self.history_id:
            filters.append(and_(
                self.model.history_id == self.history_id
            ))
        if self.order_id:
            filters.append(and_(
                self.model.order_id == self.order_id
            ))
        if self.vehicle_id:
            filters.append(and_(
                self.model.vehicle_id == self.vehicle_id
            ))
        if self.trailer_id:
            filters.append(and_(
                self.model.trailer_id == self.trailer_id
            ))

        if self.start_at and self.end_at:
            if self.start_at > self.end_at:
                raise AppExceptionResponse.bad_request("Дата начала не может быть больше даты окончания")
            filters.append(and_(
                self.model.measured_at >= self.start_at,
                self.model.measured_at <= self.end_at
            ))
        
        return filters
