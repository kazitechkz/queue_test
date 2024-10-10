from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, BaseModel

from app.feature.organization.dtos.organization_dto import OrganizationRDTO
from app.feature.user.dtos.user_dto import UserRDTO


class EmployeeRequestRDTO(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор")

    organization_id: int = Field(..., description="ID организации")
    organization_full_name: str = Field(..., max_length=256, description="Полное название организации")
    organization_bin: str = Field(..., max_length=256, description="БИН организации")

    owner_id: Optional[int] = Field(None, description="ID владельца (автор запроса)")
    owner_name: str = Field(..., max_length=256, description="Имя владельца (автор запроса)")

    employee_id: int = Field(..., description="ID сотрудника")
    employee_name: str = Field(..., max_length=256, description="Имя сотрудника")
    employee_email: EmailStr = Field(..., description="Email сотрудника")

    status:Optional[bool] = Field(default=None,description="Решение сотрудника")

    requested_at: datetime = Field(description="Дата подачи заявки")
    decided_at: Optional[datetime] = Field(default=None,description="Дата подачи заявки")

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
    organization:Optional[OrganizationRDTO] = None
    owner:Optional[UserRDTO] = None
    employee:Optional[UserRDTO] = None

    class Config:
        from_attributes = True