from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.shared.database_constants import TableConstantsNames


class ScheduleHistoryDTO(BaseModel):
    id: int

    class Config:
        from_attributes = True  # Для работы с объектами SQLAlchemy напрямую


class ScheduleHistoryCDTO(BaseModel):
    schedule_id: int | None = Field(None, description="ID расписания")
    operation_id: int | None = Field(None, description="ID операции")
    responsible_id: int | None = Field(None, description="ID ответственного")
    responsible_name: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Имя ответственного"
    )
    responsible_iin: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="ИИН ответственного"
    )

    is_passed: bool | None = Field(None, description="Пройдено ли")
    start_at: datetime | None = Field(None, description="Время начала")
    end_at: datetime | None = Field(None, description="Время окончания")
    canceled_at: datetime | None = Field(None, description="Время отмены")
    cancel_reason: str | None = Field(None, max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Причина отмены")

    model_config = {"from_attributes": True}


class ScheduleHistoryRDTO(ScheduleHistoryDTO):
    schedule_id: int | None = Field(None, description="ID расписания")
    operation_id: int | None = Field(None, description="ID операции")
    responsible_id: int | None = Field(None, description="ID ответственного")
    responsible_name: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="Имя ответственного"
    )
    responsible_iin: str | None = Field(
        None, max_length=TableConstantsNames.STANDARD_LENGTH_STRING, description="ИИН ответственного"
    )

    is_passed: bool | None = Field(None, description="Пройдено ли")
    start_at: datetime | None = Field(None, description="Время начала")
    end_at: datetime | None = Field(None, description="Время окончания")
    canceled_at: datetime | None = Field(None, description="Время отмены")
    cancel_reason: str | None = Field(None, max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Причина отмены")

    class Config:
        from_attributes = True


class ScheduleHistoryAnswerDTO(BaseModel):
    operation_value: str = Field(..., description="Значение операции")
    next_operation_value: str | None = Field(None, description="Значение операции")
    is_passed: bool = Field(..., description="Пройдено ли")
    cancel_reason: str | None = Field(None, max_length=TableConstantsNames.STANDARD_TEXT_LENGTH_MAX, description="Причина отмены")
    vehicle_id: int | None = Field(..., description="Идентификатор транспорта в кг")
    vehicle_tara_kg: int | None = Field(
        ..., description="Вес тары транспорта в кг", gt=500
    )
    trailer_id: int | None = Field(..., description="Идентификатор прицепа в кг")
    trailer_tara_kg: int | None = Field(..., description="Вес прицепа в кг", gt=100)
    vehicle_brutto_kg: int | None = Field(
        ..., description="Вес брутто транспорта в кг", gt=500
    )

    @model_validator(mode="after")
    def check_is_passed_and_vehicle_tara_kg(self):
        operation_value = self.operation_value
        is_passed = self.is_passed
        vehicle_tara_kg = self.vehicle_tara_kg
        vehicle_id = self.vehicle_id
        vehicle_brutto_kg = self.vehicle_brutto_kg
        next_operation_value = self.next_operation_value
        if operation_value == TableConstantsNames.InitialWeightOperationName:
            if is_passed and (vehicle_tara_kg is None or vehicle_id is None):
                msg = "Вес тары обязателен если транспорт проходит первичное взвешивание"
                raise ValueError(msg)
        if operation_value == TableConstantsNames.FinalWeightOperationName:
            if is_passed:
                if vehicle_brutto_kg is None:
                    msg = "Вес брутто обязателен если транспорт проходит контрольное взвешивание"
                    raise ValueError(msg)
            if not is_passed:
                if next_operation_value not in TableConstantsNames.RELOAD_OPERATIONS:
                    msg = "Обязательно укажите следующую операцию если транспорт не проходит контрольное взвешивание"
                    raise ValueError(msg)
        return self
