from pydantic import BaseModel, Field

from app.feature.organization.dtos.organization_dto import OrganizationRDTO
from app.feature.user.dtos.user_dto import UserRDTO


class OrganizationEmployeeDTO(BaseModel):
    id: int


class OrganizationEmployeeCDTO(BaseModel):
    organization_id: int = Field(description="Идентификатор организации", gt=0)
    employee_id: int = Field(description="Идентификатор Работника", gt=0)

    class Config:
        from_attributes = True


class OrganizationEmployeeRDTO(OrganizationEmployeeDTO):
    organization_id: int
    employee_id: int

    class Config:
        from_attributes = True


class OrganizationEmployeeRDTOWithRelations(OrganizationEmployeeRDTO):
    organization: OrganizationRDTO
    employee: UserRDTO
