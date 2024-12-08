from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.feature.organization.dtos.organization_dto import OrganizationRDTO
from app.feature.user.dtos.user_dto import UserRDTO
from app.shared.database_constants import TableConstantsNames


class EmployeeRequestRDTO(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор")

    organization_id: int = Field(..., description="ID организации")
    organization_full_name: str = Field(
        ..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Полное название организации"
    )
    organization_bin: str = Field(..., max_length=256, description="БИН организации")

    owner_id: int | None = Field(None, description="ID владельца (автор запроса)")
    owner_name: str = Field(
        ..., max_length=256, description="Имя владельца (автор запроса)"
    )

    employee_id: int = Field(..., description="ID сотрудника")
    employee_name: str = Field(..., max_length=256, description="Имя сотрудника")
    employee_email: EmailStr = Field(..., description="Email сотрудника")

    status: bool | None = Field(default=None, description="Решение сотрудника")

    requested_at: datetime = Field(description="Дата подачи заявки")
    decided_at: datetime | None = Field(default=None, description="Дата подачи заявки")

    created_at: datetime = Field(..., description="Дата и время создания")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления")

    class Config:
        from_attributes = True


class EmployeeRequestFromOrganizationCDTO(BaseModel):
    organization_id: int = Field(..., description="ID организации")
    employee_id: int = Field(..., description="ID сотрудника")


class EmployeeRequestFromEmployeeCDTO(BaseModel):
    status: bool = Field(description="Решение сотрудника")


class EmployeeRequestWithRelationDTO(EmployeeRequestRDTO):
    organization: OrganizationRDTO | None = None
    owner: UserRDTO | None = None
    employee: UserRDTO | None = None

    class Config:
        from_attributes = True
