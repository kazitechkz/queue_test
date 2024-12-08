from fastapi import Query
from sqlalchemy import and_, or_

from app.core.base_filter import BaseFilter
from app.domain.models.organization_model import OrganizationModel


class OrganizationFilter(BaseFilter):
    def __init__(
        self,
        per_page: int = Query(
            default=20, gt=0, example=20, description="Количество элементов на страницу"
        ),
        page: int = Query(default=1, ge=1, example=1, description="Номер страницы"),
        search: str | None = Query(
            default=None,
            max_length=255,
            min_length=3,
            description="Поисковый запрос по имени, телефону, почте, иину",
        ),
        owner_id: int | None = Query(
            default=None, gt=0, description="Введите владельца компании"
        ),
        type_id: int | None = Query(
            default=None, gt=0, description="Введите тип организации"
        ),
    ) -> None:
        super().__init__(per_page, page, search)
        self.per_page = per_page
        self.page = page
        self.search = search
        self.owner_id = owner_id
        self.type_id = type_id
        self.model = OrganizationModel

    def apply(self) -> list:
        filters = []
        if self.search:
            filters.append(
                or_(
                    self.model.email.like(f"%{self.search}%"),
                    self.model.phone.like(f"%{self.search}%"),
                    self.model.bin.like(f"%{self.search}%"),
                    self.model.bik.like(f"%{self.search}%"),
                    self.model.kbe.like(f"%{self.search}%"),
                    self.model.full_name.like(f"%{self.search}%"),
                    self.model.short_name.like(f"%{self.search}%"),
                    self.model.address.like(f"%{self.search}%"),
                )
            )
        if self.owner_id:
            filters.append(and_(self.model.owner_id == self.owner_id))
        if self.type_id:
            filters.append(and_(self.model.type_id == self.type_id))
        return filters
