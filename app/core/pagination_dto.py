# Generic тип для модели данных
from typing import Generic, TypeVar

from pydantic import BaseModel

from app.feature.employee_request.dtos.employee_request_dto import (
    EmployeeRequestWithRelationDTO,
)
from app.feature.order.dtos.order_dto import OrderRDTOWithRelations
from app.feature.organization_employee.dtos.organization_employee_dto import (
    OrganizationEmployeeRDTOWithRelations,
)
from app.feature.schedule.dtos.schedule_dto import ScheduleRDTOWithRelation
from app.feature.vehicle.dtos.vehicle_dto import VehicleWithRelationsDTO
from app.shared.relation_dtos.user_organization import (
    OrganizationRDTOWithRelations,
    UserRDTOWithRelations,
)


T = TypeVar("T")


class Pagination(Generic[T]):
    current_page: int
    last_page: int
    total_pages: int
    total_items: int
    items: list[T]

    def __init__(
        self, items: list[T], total_pages: int, total_items: int, per_page: int, page: int
    ) -> None:
        self.items = items
        self.total_pages = total_pages
        self.total_items = total_items
        self.current_page = page
        self.last_page = (total_pages + per_page - 1) // per_page


class BasePageModel(BaseModel):
    current_page: int
    last_page: int
    total_pages: int
    total_items: int


class PaginationUserRDTOWithRelations(BasePageModel):
    items: list[UserRDTOWithRelations]


class PaginationOrganizationRDTOWithRelations(BasePageModel):
    items: list[OrganizationRDTOWithRelations]


class PaginationOrganizationEmployeeRDTOWithRelations(BasePageModel):
    items: list[OrganizationEmployeeRDTOWithRelations]


class PaginationVehicleWithRelationsDTO(BasePageModel):
    items: list[VehicleWithRelationsDTO]


class PaginationOrderRDTOWithRelations(BasePageModel):
    items: list[OrderRDTOWithRelations]


class PaginationEmployeeRequestWithRelationDTO(BasePageModel):
    items: list[EmployeeRequestWithRelationDTO]


class PaginationScheduleRDTOWithRelations(BasePageModel):
    items: list[ScheduleRDTOWithRelation]
