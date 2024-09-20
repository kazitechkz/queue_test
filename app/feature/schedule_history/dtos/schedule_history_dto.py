from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class ScheduleHistoryDTO(BaseModel):
    id: int

    class Config:
        from_attributes = True  # Для работы с объектами SQLAlchemy напрямую

class ScheduleHistoryCDTO(BaseModel):
    schedule_id: Optional[int] = Field(None, description="ID расписания")
    operation_id: Optional[int] = Field(None, description="ID операции")
    responsible_id: Optional[int] = Field(None, description="ID ответственного")
    responsible_name: Optional[str] = Field(None, max_length=256, description="Имя ответственного")
    responsible_iin: Optional[str] = Field(None, max_length=256, description="ИИН ответственного")

    is_passed: Optional[bool] = Field(None, description="Пройдено ли")
    start_at: Optional[datetime] = Field(None, description="Время начала")
    end_at: Optional[datetime] = Field(None, description="Время окончания")
    canceled_at: Optional[datetime] = Field(None, description="Время отмены")
    cancel_reason: Optional[str] = Field(None, max_length=1000, description="Причина отмены")

    class Config:
        from_attributes = True

class ScheduleHistoryRDTO(ScheduleHistoryDTO):
    schedule_id: Optional[int] = Field(None, description="ID расписания")
    operation_id: Optional[int] = Field(None, description="ID операции")
    responsible_id: Optional[int] = Field(None, description="ID ответственного")
    responsible_name: Optional[str] = Field(None, max_length=256, description="Имя ответственного")
    responsible_iin: Optional[str] = Field(None, max_length=256, description="ИИН ответственного")

    is_passed: Optional[bool] = Field(None, description="Пройдено ли")
    start_at: Optional[datetime] = Field(None, description="Время начала")
    end_at: Optional[datetime] = Field(None, description="Время окончания")
    canceled_at: Optional[datetime] = Field(None, description="Время отмены")
    cancel_reason: Optional[str] = Field(None, max_length=1000, description="Причина отмены")

    class Config:
        from_attributes = True

class ScheduleHistoryEnterFactoryDTO(BaseModel):
    is_passed:bool =  Field(..., description="Пройдено ли")
    cancel_reason: Optional[str] = Field(None, max_length=1000, description="Причина отмены")

class ScheduleHistoryInitialWeightDTO(BaseModel):
    is_passed:bool =  Field(..., description="Пройдено ли")
    cancel_reason: Optional[str] = Field(None, max_length=1000, description="Причина отмены")
    vehicle_tara_kg: Optional[int] = Field(..., description="Вес тары транспорта в кг",gt=1000)

    @model_validator(mode='after')
    def check_is_passed_and_vehicle_tara_kg(self):
        is_passed = self.is_passed
        vehicle_tara_kg = self.vehicle_tara_kg
        if is_passed:
            if vehicle_tara_kg is None:
                raise ValueError('Вес тары обязателен если транспорт проходит на следующий уровень')
        return self