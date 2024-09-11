from typing import Optional

from fastapi import Query
from sqlalchemy import and_

from app.core.base_filter import BaseFilter
from app.domain.models.organization_employee_model import OrganizationEmployeeModel


class OrganizationEmployeeFilter(BaseFilter):
    def __init__(self,
                 per_page: int = Query(default=20, gt=0, example=20, description="Количество элементов на страницу"),
                 page: int = Query(default=1, ge=1, example=1, description="Номер страницы"),
                 search: Optional[str] = Query(default=None, max_length=255, min_length=3,
                                               description="Поисковый запрос по имени, телефону, почте, иину"),
                 employee_id: Optional[int] = Query(default=None, gt=0, description="Введите id работника"),
                 organization_id: Optional[int] = Query(default=None, gt=0, description="Введите id организации")):
        super().__init__(per_page, page, search)
        self.per_page = per_page
        self.page = page
        self.search = search
        self.employee_id = employee_id
        self.organization_id = organization_id
        self.model = OrganizationEmployeeModel

    def apply(self) -> list:
        filters = []
        if self.employee_id:
            filters.append(and_(self.model.employee_id == self.employee_id))
        if self.organization_id:
            filters.append(and_(self.model.organization_id == self.organization_id))
        return filters