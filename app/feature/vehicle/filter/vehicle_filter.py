from operator import and_

from fastapi import Query
from sqlalchemy import or_

from app.core.base_filter import BaseFilter
from app.domain.models.vehicle_model import VehicleModel
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class VehicleFilter(BaseFilter):
    def __init__(
        self,
        per_page: int = Query(
            default=20, gt=0, example=20, description="Количество элементов на страницу"
        ),
        page: int = Query(default=1, ge=1, example=1, description="Номер страницы"),
        search: str | None = Query(
            default=None, max_length=255, min_length=3, description="Поисковый запрос"
        ),
        category_id: int | None = Query(default=None, gt=0, description="Категория ТС"),
        color_id: int | None = Query(default=None, gt=0, description="Цвет ТС"),
        region_id: int | None = Query(default=None, gt=0, description="Место жительства"),
        owner_id: int | None = Query(
            default=None, gt=0, description="Владелец (физическое лицо) ТС"
        ),
        organization_id: int | None = Query(
            default=None, gt=0, description="Владелец (юридическое лицо) ТС"
        ),
    ) -> None:
        super().__init__(per_page, page, search)
        self.per_page = per_page
        self.page = page
        self.search = search
        self.category_id = category_id
        self.color_id = color_id
        self.region_id = region_id
        self.owner_id = owner_id
        self.organization_id = organization_id
        self.model = VehicleModel

    def apply(self) -> list:
        filters = []
        if self.search:
            filters.append(
                or_(
                    self.model.document_number.like(f"%{self.search}%"),
                    self.model.registration_number.like(f"%{self.search}%"),
                    self.model.car_model.like(f"%{self.search}%"),
                    self.model.vin.like(f"%{self.search}%"),
                    self.model.note.like(f"%{self.search}%"),
                    self.model.deregistration_note.like(f"%{self.search}%"),
                )
            )
        if self.category_id:
            filters.append(and_(self.model.category_id == self.category_id))
        if self.color_id:
            filters.append(and_(self.model.color_id == self.color_id))
        if self.region_id:
            filters.append(and_(self.model.region_id == self.region_id))
        if self.owner_id:
            filters.append(and_(self.model.owner_id == self.owner_id))
        if self.organization_id:
            filters.append(and_(self.model.organization_id == self.organization_id))
        return filters


class OwnVehicleFilter:
    def __init__(self) -> None:
        self.model = VehicleModel

    def apply(self, userDTO: UserRDTOWithRelations):
        filters = []
        if userDTO.user_type.value == TableConstantsNames.UserIndividualTypeValue:
            filters.append(self.model.owner_id == userDTO.id)
        elif userDTO.user_type.value == TableConstantsNames.UserLegalTypeValue:
            # Извлекаем все owner_id из userDTO.organizations
            owner_ids = [org.id for org in userDTO.organizations]

            # Проверяем, что список owner_ids не пустой
            if owner_ids:
                # Добавляем фильтр для organization_id
                filters.append(self.model.organization_id.in_(owner_ids))
            else:
                pass
        return filters
