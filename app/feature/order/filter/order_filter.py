from abc import ABC
from typing import Optional, List

from fastapi import Query
from sqlalchemy import and_

from app.core.base_filter import BaseFilter
from app.domain.models.order_model import OrderModel
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class OrderFilter(BaseFilter):
    def __init__(self,
                 per_page: int = Query(default=20, gt=0, example=20, description="Количество элементов на страницу"),
                 page: int = Query(default=1, ge=1, example=1, description="Номер страницы"),
                 search: Optional[str] = Query(default=None, max_length=255, min_length=3,
                                               description="Поисковый запрос по имени, телефону, почте, иину"),
                 status_id: List[int] = Query(default=[], description="Статус заказа")
                 ):
        super().__init__(per_page, page, search)
        self.per_page = per_page
        self.page = page
        self.search = search
        self.status_id = status_id
        self.model = OrderModel

    def apply(self, userDTO: UserRDTOWithRelations) -> list:
        filters = []
        if userDTO.role.value == TableConstantsNames.RoleClientValue:
            if userDTO.user_type.value == TableConstantsNames.UserIndividualTypeValue:
                filters.append(and_(self.model.owner_id == userDTO.id))
            elif userDTO.user_type.value == TableConstantsNames.UserLegalTypeValue:
                # Извлекаем все owner_id из userDTO.organizations
                owner_ids = [org.id for org in userDTO.organizations]

                # Проверяем, что список owner_ids не пустой
                if owner_ids:
                    # Добавляем фильтр для organization_id
                    filters.append(and_(self.model.organization_id.in_(owner_ids)))
                else:
                    print("Список owner_ids пуст!")

        if self.status_id:
            filters.append(and_(self.model.status_id.in_(self.status_id)))
        return filters


class DetailOrderFilter:
    def __init__(self, order_id: int = Query(description="Идентификатор заказа")):
        self.model = OrderModel
        self.order_id = order_id

    def apply(self, userDTO: UserRDTOWithRelations):
        filters = []

        if userDTO.role.value == TableConstantsNames.RoleClientValue:
            if userDTO.user_type.value == TableConstantsNames.UserIndividualTypeValue:
                filters.append(and_(self.model.owner_id == userDTO.id))
            elif userDTO.user_type.value == TableConstantsNames.UserLegalTypeValue:
                # Извлекаем все owner_id из userDTO.organizations
                owner_ids = [org.id for org in userDTO.organizations]

                # Проверяем, что список owner_ids не пустой
                if owner_ids:
                    # Добавляем фильтр для organization_id
                    filters.append(and_(self.model.organization_id.in_(owner_ids)))
                else:
                    print("Список owner_ids пуст!")

        if self.order_id:
            filters.append(and_(self.model.id == self.order_id))
        return filters


class OrderFiltersForPaymentDocuments(BaseFilter):
    def __init__(self,
                 per_page: int = Query(default=20, gt=0, example=20, description="Количество элементов на страницу"),
                 page: int = Query(default=1, ge=1, example=1, description="Номер страницы")
                 ):
        super().__init__(per_page, page)
        self.per_page = per_page
        self.page = page
        self.model = OrderModel

    def apply(self):
        filters = [and_(self.model.status_id == 9)]
        return filters

