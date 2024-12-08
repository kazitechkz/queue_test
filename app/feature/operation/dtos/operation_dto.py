from datetime import datetime

from pydantic import BaseModel, Field

from app.feature.role.dtos.role_dto import RoleRDTO
from app.shared.database_constants import TableConstantsNames


class OperationDTO(BaseModel):
    id: int

    created_at: datetime = Field(..., description="Дата и время создания")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления")

    class Config:
        from_attributes = True


class OperationRDTO(OperationDTO):
    title: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Название операции")
    value: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Уникальное значение операции")
    role_id: int | None = Field(None, description="ID роли, связанной с операцией")
    role_value: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Значение роли")
    is_first: bool = Field(False, description="Является ли операция первой")
    is_last: bool = Field(False, description="Является ли операция последней")
    prev_id: int | None = Field(None, description="ID предыдущей операции")
    next_id: int | None = Field(None, description="ID следующей операции")
    can_cancel: bool = Field(..., description="Можно ли отменить операцию")

    class Config:
        from_attributes = True


class OperationCDTO(BaseModel):
    title: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Название операции")
    value: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Уникальное значение операции")
    role_id: int | None = Field(None, description="ID роли, связанной с операцией")
    role_value: str = Field(..., max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Значение роли")
    is_first: bool = Field(False, description="Является ли операция первой")
    is_last: bool = Field(False, description="Является ли операция последней")
    prev_id: int | None = Field(None, description="ID предыдущей операции")
    next_id: int | None = Field(None, description="ID следующей операции")
    can_cancel: bool = Field(..., description="Можно ли отменить операцию")

    class Config:
        from_attributes = True


class OperationWithRelationRDTO(OperationRDTO):
    role: RoleRDTO | None = None
    prev_operation: OperationRDTO | None = None
    next_operation: OperationRDTO | None = None

    class Config:
        from_attributes = True
