from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


from app.shared.database_constants import TableConstantsNames


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

class ScheduleHistoryAnswerDTO(BaseModel):
    operation_value:str = Field(..., description="Значение операции")
    next_operation_value:Optional[str] = Field(None, description="Значение операции")
    is_passed:bool =  Field(..., description="Пройдено ли")
    cancel_reason: Optional[str] = Field(None, max_length=1000, description="Причина отмены")
    vehicle_id:Optional[int] = Field(..., description="Идентификатор транспорта в кг")
    vehicle_tara_kg: Optional[int] = Field(..., description="Вес тары транспорта в кг", gt=500)
    trailer_id: Optional[int] = Field(..., description="Идентификатор прицепа в кг")
    trailer_tara_kg: Optional[int] = Field(..., description="Вес прицепа в кг", gt=100)
    vehicle_brutto_kg: Optional[int] = Field(..., description="Вес брутто транспорта в кг", gt=500)

    @model_validator(mode='after')
    def check_is_passed_and_vehicle_tara_kg(self):
        operation_value = self.operation_value
        is_passed = self.is_passed
        vehicle_tara_kg = self.vehicle_tara_kg
        vehicle_id = self.vehicle_id
        vehicle_brutto_kg = self.vehicle_brutto_kg
        next_operation_value = self.next_operation_value
        if operation_value == TableConstantsNames.InitialWeightOperationName:
            if is_passed:
                if vehicle_tara_kg is None or vehicle_id is None:
                    raise ValueError('Вес тары обязателен если транспорт проходит первичное взвешивание')
        if operation_value == TableConstantsNames.FinalWeightOperationName:
            if is_passed:
                if vehicle_brutto_kg is None:
                    raise ValueError('Вес брутто обязателен если транспорт проходит контрольное взвешивание')
            if not is_passed:
                if next_operation_value not in TableConstantsNames.RELOAD_OPERATIONS:
                    raise ValueError('Обязательно укажите следующую операцию если транспорт не проходит контрольное взвешивание')
        return self

