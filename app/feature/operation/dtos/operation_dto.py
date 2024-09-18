from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OperationDTO(BaseModel):
    id: int

    created_at: datetime = Field(..., description="Дата и время создания")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления")

    class Config:
        from_attributes = True


class OperationRDTO(OperationDTO):
    title: str = Field(..., max_length=255, description="Название операции")
    value: str = Field(..., max_length=255, description="Уникальное значение операции")
    role_id: Optional[int] = Field(None, description="ID роли, связанной с операцией")
    role_value: str = Field(..., max_length=255, description="Значение роли")
    is_first: bool = Field(False, description="Является ли операция первой")
    is_last: bool = Field(False, description="Является ли операция последней")
    prev_id: Optional[int] = Field(None, description="ID предыдущей операции")
    next_id: Optional[int] = Field(None, description="ID следующей операции")
    can_cancel: bool = Field(..., description="Можно ли отменить операцию")

class OperationCDTO(BaseModel):
    title: str = Field(..., max_length=255, description="Название операции")
    value: str = Field(..., max_length=255, description="Уникальное значение операции")
    role_id: Optional[int] = Field(None, description="ID роли, связанной с операцией")
    role_value: str = Field(..., max_length=255, description="Значение роли")
    is_first: bool = Field(False, description="Является ли операция первой")
    is_last: bool = Field(False, description="Является ли операция последней")
    prev_id: Optional[int] = Field(None, description="ID предыдущей операции")
    next_id: Optional[int] = Field(None, description="ID следующей операции")
    can_cancel: bool = Field(..., description="Можно ли отменить операцию")
