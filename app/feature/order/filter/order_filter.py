from typing import Optional

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
                 status_id: int = Query(default=1, description="Статус заказа")
                 ):
        super().__init__(per_page, page, search)
        self.per_page = per_page
        self.page = page
        self.search = search
        self.status_id = status_id
        self.model = OrderModel

    def apply(self, userDTO: UserRDTOWithRelations) -> list:
        filters = []
        if userDTO.user_type.value == TableConstantsNames.UserIndividualTypeValue:
            filters.append(and_(self.model.owner_id == userDTO.id))
        elif userDTO.user_type.value == TableConstantsNames.UserLegalTypeValue:
            # Извлекаем все owner_id из userDTO.organizations
            owner_ids = [1]

            # Проверяем, что список owner_ids не пустой
            if owner_ids:
                filters.append(and_(self.model.organization_id.in_(owner_ids)))
        if self.status_id:
            filters.append(and_(self.model.status_id == self.status_id))
        return filters
