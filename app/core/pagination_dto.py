# Generic тип для модели данных
from typing import List, Generic, TypeVar

from pydantic import BaseModel

from app.feature.employee_request.dtos.employee_request_dto import EmployeeRequestWithRelationDTO
from app.feature.order.dtos.order_dto import OrderRDTOWithRelations
from app.feature.organization_employee.dtos.organization_employee_dto import OrganizationEmployeeRDTOWithRelations
from app.feature.schedule.dtos.schedule_dto import ScheduleRDTOWithRelation
from app.feature.vehicle.dtos.vehicle_dto import VehicleWithRelationsDTO
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations, OrganizationRDTOWithRelations

T = TypeVar('T')


class Pagination(Generic[T]):
    current_page: int
    last_page: int
    total_pages: int
    total_items: int
    items: List[T]

    def __init__(self, items: List[T], total_pages: int, total_items: int, per_page: int, page: int):
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
    items: List[UserRDTOWithRelations]


class PaginationOrganizationRDTOWithRelations(BasePageModel):
    items: List[OrganizationRDTOWithRelations]


class PaginationOrganizationEmployeeRDTOWithRelations(BasePageModel):
    items: List[OrganizationEmployeeRDTOWithRelations]


class PaginationVehicleWithRelationsDTO(BasePageModel):
    items: List[VehicleWithRelationsDTO]


class PaginationOrderRDTOWithRelations(BasePageModel):
    items: List[OrderRDTOWithRelations]


class PaginationEmployeeRequestWithRelationDTO(BasePageModel):
    items: List[EmployeeRequestWithRelationDTO]


class PaginationScheduleRDTOWithRelations(BasePageModel):
    items: List[ScheduleRDTOWithRelation]
