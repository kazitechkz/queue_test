from typing import Optional

from fastapi import Query
from sqlalchemy import or_, and_

from app.core.base_filter import BaseFilter
from app.domain.models.employee_request import EmployeeRequestModel
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class EmployeeRequestFilter(BaseFilter):
    def __init__(self,
                 per_page: int = Query(default=20, gt=0, example=20, description="Количество элементов на страницу"),
                 page: int = Query(default=1, ge=1, example=1, description="Номер страницы"),
                 search: Optional[str] = Query(default=None, max_length=255, min_length=3,
                                               description="Поисковый запрос по компании (наименование или БИН), владельцу, сотруднику (имени или почте)"),
                 status: Optional[bool] = Query(default=None,
                                                description="Если True - заявку приняли, False - Заявку отменили, None - Заявку не просмотрели")
                 ):
        super().__init__(per_page, page, search)
        self.per_page = per_page
        self.page = page
        self.search = search
        self.status = status
        self.model = EmployeeRequestModel

    def apply(self, userDTO: UserRDTOWithRelations) -> list:
        filters = []
        if self.search:
            filters.append(and_(
                    or_(
                        self.model.organization_full_name.like(f"%{self.search}%"),
                        self.model.organization_bin.like(f"%{self.search}%"),
                        self.model.owner_name.like(f"%{self.search}%"),
                        self.model.employee_name.like(f"%{self.search}%"),
                        self.model.employee_email.like(f"%{self.search}%"),
                    )
                )
            )
        if self.status is not None:
            filters.append(
                and_(
                    self.model.status == self.status
                )
            )
        if userDTO.user_type == TableConstantsNames.UserLegalTypeValue:
            organization_ids = [organization.id for organization in userDTO.organizations]
            filters.append(and_(self.model.organization_id.in_(organization_ids)))
        else:
            filters.append(and_(self.model.employee_id == userDTO.id))

        return filters
