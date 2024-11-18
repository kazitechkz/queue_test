from datetime import datetime, date, time, timezone
from typing import Optional, List

from pydantic import Field, BaseModel, model_validator, field_validator

from app.feature.operation.dtos.operation_dto import OperationRDTO
from app.feature.order.dtos.order_dto import OrderRDTO


class ScheduleDTO(BaseModel):
    id: int

    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")

    class Config:
        from_attributes = True


class ScheduleRDTO(ScheduleDTO):
    order_id: Optional[int] = Field(None, description="ID заказа")
    zakaz: Optional[str] = Field(None, max_length=20, description="Заказ")

    owner_id: Optional[int] = Field(None, description="ID владельца")
    owner_name: str = Field(..., max_length=256, description="Имя владельца")
    owner_iin: str = Field(..., max_length=256, description="ИИН владельца")

    driver_id: Optional[int] = Field(None, description="ID водителя")
    driver_name: str = Field(..., max_length=256, description="Имя водителя")
    driver_iin: str = Field(..., max_length=256, description="ИИН водителя")

    organization_id: Optional[int] = Field(None, description="ID организации")
    organization_full_name: Optional[str] = Field(None, max_length=256, description="Полное название организации")
    organization_bin: Optional[str] = Field(None, max_length=256, description="БИН организации")

    vehicle_id: Optional[int] = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(..., max_length=1000, description="Информация о транспортном средстве")

    trailer_id: Optional[int] = Field(None, description="ID прицепа")
    trailer_info: Optional[str] = Field(None, max_length=1000, description="Информация о прицепе")

    workshop_schedule_id: Optional[int] = Field(None, description="ID расписания мастерской")
    current_operation_id: Optional[int] = Field(None, description="Текущая операция")

    start_at: datetime = Field(..., description="Время начала")
    end_at: datetime = Field(..., description="Время окончания")

    rescheduled_start_at: Optional[datetime] = Field(default=None, description="Время начала перенос")
    rescheduled_end_at: Optional[datetime] = Field(default=None, description="Время окончания перенос")

    loading_volume_kg: int = Field(..., description="Объем загрузки в кг")
    vehicle_tara_kg: Optional[int] = Field(None, description="Тара транспортного средства в кг")
    vehicle_brutto_kg: Optional[int] = Field(None, description="Брутто транспортного средства в кг")
    vehicle_netto_kg: Optional[int] = Field(None, description="Нетто транспортного средства в кг")

    responsible_id: Optional[int] = Field(None, description="ID ответственного")
    responsible_name: Optional[str] = Field(None, max_length=256, description="Имя ответственного")

    is_active: bool = Field(..., description="Активно ли расписание")
    is_used: bool = Field(..., description="Использовано ли расписание")
    is_canceled: bool = Field(..., description="Отменено ли расписание")
    is_executed: bool = Field(..., description="Выполнено ли расписание")
    executed_at: Optional[datetime] = Field(None, description="Время выполнения")

    canceled_by: Optional[int] = Field(None, description="Кто отменил")
    cancel_reason: Optional[str] = Field(None, max_length=1000, description="Причина отмены")
    canceled_at: Optional[datetime] = Field(None, description="Время отмены")

    current_operation: OperationRDTO

    class Config:
        from_attributes = True


class ScheduleCDTO(BaseModel):
    order_id: Optional[int] = Field(None, description="ID заказа")
    zakaz: Optional[str] = Field(None, max_length=20, description="Заказ")

    owner_id: Optional[int] = Field(None, description="ID владельца")
    owner_name: str = Field(..., max_length=256, description="Имя владельца")
    owner_iin: str = Field(..., max_length=256, description="ИИН владельца")

    driver_id: Optional[int] = Field(None, description="ID водителя")
    driver_name: str = Field(..., max_length=256, description="Имя водителя")
    driver_iin: str = Field(..., max_length=256, description="ИИН водителя")

    organization_id: Optional[int] = Field(None, description="ID организации")
    organization_full_name: Optional[str] = Field(None, max_length=256, description="Полное название организации")
    organization_bin: Optional[str] = Field(None, max_length=256, description="БИН организации")

    vehicle_id: Optional[int] = Field(None, description="ID транспортного средства")
    vehicle_info: str = Field(..., max_length=1000, description="Информация о транспортном средстве")

    trailer_id: Optional[int] = Field(None, description="ID прицепа")
    trailer_info: Optional[str] = Field(None, max_length=1000, description="Информация о прицепе")

    workshop_schedule_id: Optional[int] = Field(None, description="ID расписания мастерской")
    current_operation_id: Optional[int] = Field(None, description="Текущая операция")

    start_at: datetime = Field(..., description="Время начала")
    end_at: datetime = Field(..., description="Время окончания")

    rescheduled_start_at: Optional[datetime] = Field(default=None, description="Время начала перенос")
    rescheduled_end_at: Optional[datetime] = Field(default=None, description="Время окончания перенос")

    loading_volume_kg: int = Field(..., description="Объем загрузки в кг")
    vehicle_tara_kg: Optional[int] = Field(None, description="Тара транспортного средства в кг")
    vehicle_brutto_kg: Optional[int] = Field(None, description="Брутто транспортного средства в кг")
    vehicle_netto_kg: Optional[int] = Field(None, description="Нетто транспортного средства в кг")

    responsible_id: Optional[int] = Field(None, description="ID ответственного")
    responsible_name: Optional[str] = Field(None, max_length=256, description="Имя ответственного")

    is_active: Optional[bool] = Field(True, description="Активно ли расписание")
    is_used: Optional[bool] = Field(False, description="Использовано ли расписание")
    is_canceled: Optional[bool] = Field(False, description="Отменено ли расписание")
    is_executed: Optional[bool] = Field(False, description="Выполнено ли расписание")
    executed_at: Optional[datetime] = Field(None, description="Время выполнения")

    canceled_by: Optional[int] = Field(None, description="Кто отменил")
    cancel_reason: Optional[str] = Field(None, max_length=1000, description="Причина отмены")
    canceled_at: Optional[datetime] = Field(None, description="Время отмены")

    @model_validator(mode='after')
    def check_dates_and_times(self):
        start_at = self.start_at
        end_at = self.end_at
        if start_at and end_at and end_at <= start_at:
            raise ValueError('Время окончания работы должна быть больше даты начала')
        return self

    class Config:
        from_attributes = True


class ScheduleIndividualCDTO(BaseModel):
    order_id: int = Field(description="ID заказа")
    workshop_schedule_id: int = Field(description="Шаблон расписания цеха")
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    start_at: time = Field(description="Начало бронирования")
    end_at: time = Field(description="Конец бронирования")
    vehicle_id: Optional[int] = Field(None, description="ID транспортного средства")
    trailer_id: Optional[int] = Field(None, description="ID прицепа")
    booked_quan_t: float = Field(description="Общая масса бронирования в тоннах", ge=1)

    @model_validator(mode='after')
    def check_dates_and_times(self):
        start_at = self.start_at
        end_at = self.end_at
        if start_at and end_at and end_at <= start_at:
            raise ValueError('Время окончания работы должна быть больше даты начала')
        return self


class ScheduleLegalCDTO(BaseModel):
    organization_id: int = Field(description="ID организации")
    order_id: int = Field(description="ID заказа")
    driver_id: int = Field(description="ID водителя"),
    workshop_schedule_id: int = Field(description="Шаблон расписания цеха")
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    start_at: time = Field(description="Начало бронирования")
    end_at: time = Field(description="Конец бронирования")
    vehicle_id: Optional[int] = Field(None, description="ID транспортного средства")
    trailer_id: Optional[int] = Field(None, description="ID прицепа")
    booked_quan_t: float = Field(description="Общая масса бронирования в тоннах")

    @model_validator(mode='after')
    def check_dates_and_times(self):
        start_at = self.start_at
        end_at = self.end_at
        if start_at and end_at and end_at <= start_at:
            raise ValueError('Время окончания работы должна быть больше даты начала')
        return self

    @field_validator('scheduled_data')
    def validate_scheduled_data(cls, v):
        if v < date.today():
            raise ValueError('Время начала работы должна быть больше чем текущее')
        return v

    class Config:
        from_attributes = True


class ScheduleSpaceDTO(BaseModel):
    workshop_schedule_id: int = Field(description="Уникальный идентификатор бронирования")
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    start_at: time = Field(description="Начало бронирования")
    end_at: time = Field(description="Конец бронирования")
    free_space: int = Field(title="Кол-во свободных мест", description="Кол-во свободных мест")


class ScheduleCalendarDTO(BaseModel):
    scheduled_at: date = Field(description="Дата бронирования")
    total: int = Field(description="Общее количество бронирований")
    total_active: int = Field(description="Общее количество активных бронирований")
    total_canceled: int = Field(description="Количество отменненых бронирований")
    total_executed: int = Field(description="Количество выполненых бронирований")


class RescheduleAllDTO(BaseModel):
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    minute: int = Field(description="Перенос в минутах", gt=0, le=120)


class ScheduleCancelDTO(BaseModel):
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    cancel_reason: Optional[str] = Field(None, max_length=1000, description="Причина отмены")


class RescheduleOneDTO(BaseModel):
    scheduled_data: date = Field(description="Дата бронирования", ge=date.today())
    start_at: time = Field(description="Начало бронирования")
    end_at: time = Field(description="Конец бронирования")

    @model_validator(mode='after')
    def check_dates_and_times(self):
        start_at = self.start_at
        end_at = self.end_at
        if start_at and end_at and end_at <= start_at:
            raise ValueError('Время окончания работы должна быть больше даты начала')
        return self


class ScheduleCancelOneDTO(BaseModel):
    cancel_reason: Optional[str] = Field(None, max_length=1000, description="Причина отмены")


class ScheduleRDTOWithRelation(ScheduleRDTO):
    current_operation: Optional[OperationRDTO] = None
    # order: Optional[OrderRDTO] = None
    # pass
